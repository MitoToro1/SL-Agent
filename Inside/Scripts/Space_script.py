# Funcs: (* - optional)
# Create Named Space (folder: folder (files_sources), links_toUse.txt, context_db.db)
# Remove named space
# Change name of the space*

try:
    import os
    import shutil
    import sys
    from pathlib import Path
    from time import sleep

    #stuff to successfully import module from the neighbor folder
    neighbor_folder = Path(__file__).parent.parent
    sys.path.append(str(neighbor_folder))

    from DB_script import DataBase
    from Parsers.TXT_Parser import create_txt


except Exception as e:
    print(f"---[] Space_script.py imports couldn't load!\n Error:{e}")
#global vars
Master_folder_path = Path(__file__).parent.parent.parent
Spaces_folder_path = Master_folder_path / 'Spaces'

def create_space(SpaceName:str):
    '''
    Function for creating spaces (folders, containing - Folder with source-files, txt with links to use, sqlite db file)
    
    Spaces will be created in Spaces folder in Master folder of the program
    '''
    try:
        #create folder with given name and folder inside it with source files
        os.makedirs(Spaces_folder_path/"{}/Source Files".format(SpaceName)) 
        #create txt (links to use) file inside space folder
        create_txt(Spaces_folder_path/'{}'.format(SpaceName), 'Links To Use.txt')
        #create DB for the space
        DB = DataBase(Spaces_folder_path / SpaceName)
        DB.DB_init()
        print('--[] New space ({}) is created!'.format(SpaceName) )
        return Spaces_folder_path / SpaceName
    except Exception as e: 
        remove_space(SpaceName)
        print(f"---[] Couldn't create new space :(\nError: {e}")


def remove_space(ToRemoveName):
    '''
    Function for deleting spaces by given name
    '''
    try:
        shutil.rmtree(Spaces_folder_path/'{}'.format(ToRemoveName))
        print('---[] The space', ToRemoveName, 'was removed!' )
    except Exception as e:
        print("-[!]- Couldn't remove the space ({})!\nError:{}".format(ToRemoveName,e))

def change_spaceName(oldName, newName):
    '''
    Function for changing name of the space
    '''
    a_amount = 10 # amount of attempts
    for attempts in range(1,a_amount+1):
        try:
            oldNameP = Spaces_folder_path/oldName
            newNameP = Spaces_folder_path / newName
            os.rename(oldNameP, newNameP)
            print('-[] Space '+oldName+' was renamed to '+newName)
            break
        except PermissionError:
            print(f"[TRY {attempts}/{a_amount}] Couldn't change space name, retrying...")
            sleep(0.5)
            if attempts == a_amount:
                print("-[!]- Sorry! Couldn't rename the space!\nPermission Error: Windows Defender or Antivirus don't let to rename the space...\nTry again later or run the program with administrator privilliges")


def empty_Space(toEmpty):
    '''
    Function for making space folder empty (empty txt, source files folder, database)
    '''
    remove_space(toEmpty)
    create_space(toEmpty)
    print('--[] Space', toEmpty, 'was cleared!')

def testing_grounds():
    '''
    Function for testing.
    
    well - works as intended, 
    fine - needs more testing, 
    bad - doesn't work, 
    wrong - not like intented
    '''
    # remove_space('test2') # works fine 
    # create_space('test2') # works fine 
    # change_spaceName("Hola", "Popa") #works fine? depends on individual Windows Defender

# testing_grounds()