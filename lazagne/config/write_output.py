import ctypes
import getpass
import json
import logging
import os
import socket
import sys
import traceback
from time import gmtime, strftime
from platform import uname

from lazagne.config.users import get_username_winapi
from lazagne.config.winstructure import string_to_unicode, char_to_int, chr_or_byte, python_version
from .constant import constant

buffer_text = '';
def msg(text):
    global buffer_text;
    if text.startswith('[+]'): return 0
    buffer_text = '{0}\n{1}'.format(buffer_text,text)
print = msg
# --------------------------- Standard output functions ---------------------------

STD_OUTPUT_HANDLE = -11
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
tmp_user = None


class StandardOutput(object):

    # info option for the logging
    def print_title(self, title):
        t = u'------------------- ' + title + ' passwords -----------------\n'
        self.do_print(message=t, color='white', intensity=True)

    # debug option for the logging
    def title_info(self, title):
        t = u'------------------- ' + title + ' passwords -----------------\n'
        self.print_logging(function=logging.info, prefix='', message=t, color='white', intensity=True)

    def print_user(self, user, force_print=False):
        if logging.getLogger().isEnabledFor(logging.INFO) or force_print:
            self.do_print(u'\n########## User: {user} ##########\n'.format(user=user))


    def print_hex(self, src, length=8):
        N = 0
        result = b''
        while src:
            s, src = src[:length], src[length:]
            hexa = b' '.join([b"%02X" % char_to_int(x) for x in s])
            s = s.translate(self.FILTER)
            result += b"%04X   %-*s   %s\n" % (N, length * 3, hexa, s)
            N += length
        return result

    def try_unicode(self, obj, encoding='utf-8'):
        if python_version == 3:
            try:
                return obj.decode()
            except Exception:
                return obj
        try:
            if isinstance(obj, basestring):       # noqa: F821
                if not isinstance(obj, unicode):  # noqa: F821
                    obj = unicode(obj, encoding)  # noqa: F821
        except UnicodeDecodeError:
            return repr(obj)
        return obj

    # centralize print function
    def do_print(self, message='', color=False, intensity=False):
        # quiet mode => nothing is printed
        if constant.quiet_mode:
            return

        message = self.try_unicode(message)
        if color:
            self.print_without_error(message)
        else:
            self.print_without_error(message)

    def print_without_error(self, message):
        try:
            print(message.decode())
        except Exception:
            try:
                print(message)
            except Exception:
                print(repr(message))

    def print_logging(self, function, prefix='[!]', message='', color=False, intensity=False):
        if constant.quiet_mode:
            return

        try:
            msg = u'{prefix} {msg}'.format(prefix=prefix, msg=message)
        except Exception:
            msg = '{prefix} {msg}'.format(prefix=prefix, msg=str(message))

        if color:
            function(msg)
        else:
            function(msg)

    def print_output(self, software_name, pwd_found):
        if pwd_found:
            # Particular passwords representation
            to_write = []
            if software_name in ('Hashdump', 'Lsa_secrets', 'Mscache'):
                pwds = pwd_found[1]
                for pwd in pwds:
                    self.do_print(pwd)
                    if software_name == 'Lsa_secrets':
                        hex_value = self.print_hex(pwds[pwd], length=16)
                        to_write.append([pwd.decode(), hex_value.decode()])
                        self.do_print(hex_value)
                    else:
                        to_write.append(pwd)
                self.do_print()

            # Other passwords
            else:
                # Remove duplicated password
                pwd_found = [dict(t) for t in set([tuple(d.items()) for d in pwd_found])]

                # Loop through all passwords found
                for pwd in pwd_found:

                    # Detect which kinds of password has been found
                    pwd_lower_keys = {k.lower(): v for k, v in pwd.items()}
                    for p in ('password', 'key', 'hash'):
                        pwd_category = [s for s in pwd_lower_keys if p in s]
                        if pwd_category:
                            pwd_category = pwd_category[0]
                            break

                    write_it = False
                    passwd = None
                    try:
                        passwd_str = pwd_lower_keys[pwd_category]
                        # Do not print empty passwords
                        if not passwd_str:
                            continue

                        passwd = string_to_unicode(passwd_str)
                    except Exception:
                        pass

                    # No password found
                    if not passwd:
                        print_debug("FAILED", u'Password not found !!!')
                    else:
                        constant.nb_password_found += 1
                        write_it = True
                        print_debug("OK", u'{pwd_category} found !!!'.format(
                            pwd_category=pwd_category.title()))

                        # Store all passwords found on a table => for dictionary attack if master password set
                        if passwd not in constant.password_found:
                            constant.password_found.append(passwd)

                    pwd_info = []
                    for p in pwd:
                        try:
                            pwd_line = '%s: %s' % (p, pwd[p].decode())  # Manage bytes output (py 3)
                        except Exception:
                            pwd_line = '%s: %s' % (p, pwd[p])

                        pwd_info.append(pwd_line)
                        self.do_print(pwd_line)

                    self.do_print()

                    if write_it:
                        to_write.append(pwd_info)
        else:
            print_debug("INFO", "No passwords found\n")




def print_debug(error_level, message):
    # Quiet mode => nothing is printed
    if constant.quiet_mode:
        return

    # print when password is found
    if error_level == 'OK':
        constant.st.do_print(message='[+] {message}'.format(message=message), color='green')

    # print when password is not found
    elif error_level == 'FAILED':
        constant.st.do_print(message='[-] {message}'.format(message=message), color='red', intensity=True)

    elif error_level == 'CRITICAL' or error_level == 'ERROR':
        constant.st.print_logging(function=logging.error, prefix='[-]', message=message, color='red', intensity=True)

    elif error_level == 'WARNING':
        constant.st.print_logging(function=logging.warning, prefix='[!]', message=message, color='cyan')

    elif error_level == 'DEBUG':
        constant.st.print_logging(function=logging.debug, message=message, prefix='[!]')

    else:
        constant.st.print_logging(function=logging.info, message=message, prefix='[!]')