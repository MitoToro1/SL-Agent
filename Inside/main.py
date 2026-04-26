# Funcs: (* - optional)
# choose space and chat
# or don't choose space at all (incognito mode?)
# use RAG.py for getting context-based conversation
#should have (atleast simple) UI

#TODO:
#Beta:
#LLM_interact.py -> DB_script.py -> Space_script.py -> RAG.py -> Simple UI (chat, space creation, space deletion, check request history) -> Github release
#Also need logo :)


#Full Version:
##Web_crawler (gives info from web to RAG) -> Github commit
##Parsers -> Each one: github commit (except TXT_Parser, it is already implemented)
##Remove chat requests/answers (remove from DB, remove from chats visually, maybe animation of removal like in Tg) -> Github commit
##Regenerate answers (replace content of DB_i saving same id, generate new answers given same context as for the previous one) -> Github commit
##Better UI -> Github commit
##Incognito mode (doesn't save in spaces) + ability to get chats into selected space -> Github commit



#TODO (#WIP):
# fix Database contents look like: <Scripts.DB_script.Request object at 0x00000280FEE65C70>
# UI
# PDF_Parser
# Web_crawler.py + RAG web_search
# DB_script's functions are not fully done

try:
    import os
    import sys
    from pathlib import Path
    from time import sleep

    #stuff to fix "Space_script's imports doesn't load. Can't find DB_script"
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/Scripts')
    
    #for functionality
    from LLM.RAG import compile_answer
    from Scripts.Space_script import create_space, remove_space, change_spaceName, empty_Space
    from Scripts.DB_script import DataBase

    #for UI
    from pprint import pprint #just for the developer needs

    print("---[]  Imports are loaded successfully!")
except Exception as e:
    print(f"---[] Main imports couldn't load!\nError:{e}")


print(compile_answer("название для морских львов на латыни", r'C:\Users\User\Desktop\SL-Agent\Spaces\test').content)
# change_spaceName('old_space', 'test')

a = DataBase(Path('C:\\Users\\User\\Desktop\\SL-Agent\\Spaces\\test'))
print("=== DATABASE CONTENTS ===")
pprint(a.DB_view())
print("=== DATABASE CONTENTS ===")
