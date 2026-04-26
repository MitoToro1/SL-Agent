# Use DB_script.py and LLM_interact to get answer from LLM with dependce on the context
# From RAG to main should be imported funcs that give answers according to context of the given space and instructions from space (links and files)

try:
    from pathlib import Path
    import sys
    import os

    #stuff to successfully import module from the neighbor folder
    inside_folder = Path(__file__).parent.parent
    Master_folder = inside_folder.parent
    sys.path.append(str(inside_folder))

    #Parsers:
    from Parsers.TXT_Parser import create_txt, parse_txt
    from Parsers.DOC_Parser import create_doc, parse_doc
    from Parsers.DOCX_Parser import create_docx, parse_docx
    from Parsers.PDF_Parser import create_pdf, parse_pdf
    from Parsers.Image_Parser import create_jpeg, create_jpg, create_png, parse_png, parse_jpeg, parse_jpg
    #Image parser is not done, it should have parse_image function that must be instead of 3 different func. for each type
    from Parsers.CSV_Parser import create_csv, parse_csv
    from Parsers.Video_Parser import create_mp4, parse_mp4

    from Scripts.DB_script import DataBase, Request
    from LLM.LLM_interact import GIGA_Ask

except Exception as e:
    print(f"-[!]- Couldn't import needed modules in RAG! Error:\n {e}")


def parseEveryting(whatToParse) -> list:
    result = []
    file_list = [i.name for i in whatToParse.iterdir() if i.is_file()]
    f_extensions = {
        'v': 'csv',
        'c': 'doc',
        'x': 'docx',
        'f': 'pdf',
        't': 'txt',
        'g': 'jpeg, png, jpg',
        '4': 'mp4'
    }
    for i in file_list:
        extenstion = f_extensions[i[-1]]
    exec(f'result.append(parse_{extenstion})')
    return result

def is_folder_empty(filePath) -> bool:
    if not filePath.exists():
        return True
    return len(os.listdir(filePath)) == 0

def get_SpaceInfo(SpaceName) -> list:
    '''
    Function for getting information from space as list of str and list:
    [list(source_files_info[str(file1), str(file2), str(file3)]), str(database_info), str(links_to_use)]
    '''

    if SpaceName is None:
        return None
    
    else:
        spaces_folder = Master_folder / "Spaces"
        space = spaces_folder / SpaceName

        src_files = space / 'Source Files'

        links = space / 'Links To Use.txt'


        result_of_parsing = []

        if not is_folder_empty(src_files):
            result_of_parsing.append(parseEveryting(src_files))
        
        result_of_parsing.append(parse_txt(links))

        db_object = DataBase(space)
        result_of_parsing.append(str(db_object.DB_view()[:2000]))

        return result_of_parsing
            



#TODO: (only when Web_crawler.py will be ready)       
def get_InternetInfo(whatToFind) -> str:
    '''
    Searches for relevant information online and returns answer as string.
    '''
    #GigaChat looks at the question of the user and generates 10-50 search prompts to find relevant info
    #create empty_txt
    #then using seach engine func parses info from 10-50 websites and writes each result in temporary txt file (link - parsed info)
    #GigaChat is given all the info from the txt( as str using parse_txt ) and summarizes it (but leaving links be)
    #then function returns str of summarized web info
    try:
        #find something
        return "No Internet Info" 

    except Exception as e:
        print(f"During web-search an error occured!\nError:{e}")




def compile_answer(question2: str, space_path=None):
    '''
    Function for making answer according to Space and Internet information of the matter
    (It returns answer)
    space_path by default is None
    '''
    Internet_info = get_InternetInfo(question2)
    Context = get_SpaceInfo(space_path)

    Context_str = ''
    for i in Context:
        Context_str+=i
    Context_str = Context_str[:4000]

    answer = ":("
    try:
        if space_path != None:
            answer = GIGA_Ask(question=question2, additional_data='"ДАННАЯ ИНФОРМАЦИЯ":\n\n'+Internet_info+"\n\n Контекст вопроса:\n"+Context_str, instructions='Ты - персональный помощник по поиску информации, используй "ДАННАЯ ИНФОРМАЦИЯ" для того, чтобы ответить. Только, пожалуйста, не убирай ссылки из ответа')
            if type(answer) != str:
                db_manager = DataBase(space_path)
                print('---[] Question and Answer are added to the database')
                db_manager.DB_i_add(content2=question2, answ_or_resp2='QUESTION')
                db_manager.DB_i_add(content2=answer.content, answ_or_resp2='ANSWER')
        else:
            print('-[?]- No space found to use...')
            # print(e)
            answer = GIGA_Ask(question=question2, additional_data='"ДАННАЯ ИНФОРМАЦИЯ":\n\n'+Internet_info+"\n\n Контекст вопроса:\n", instructions='Ты - персональный помощник по поиску информации, используй "ДАННАЯ ИНФОРМАЦИЯ" для того, чтобы ответить. Только, пожалуйста, не убирай ссылки из ответа')
    except AttributeError: #no internet, therefore GIGA_Ask returns just a string, not needed datatype
        answer = ':('


    
    return answer








def testing_grounds():
    '''
    Function for testing.
    
    well - works as intended, 
    fine - needs more testing, 
    bad - doesn't work, 
    wrong - not like intented
    '''
    # print(inside_folder) #well
    # print(Master_folder) # well
    # print(is_folder_empty(inside_folder)) # well
    # print(is_folder_empty(inside_folder / 'Spaces')) # well
    # print(get_SpaceInfo('test')) #fine

# testing_grounds()
