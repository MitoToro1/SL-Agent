#funcs (* - optional)
#func for getting text from txt as str
#func for creating an empty txt file

def parse_txt(filePath) -> str:
    '''
    Function for easy parsing of given txt file
    filePath is path to the txt file
    '''
    result = ''
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            result = f.read()
        return result
    except Exception as e:
        print(f"Couldn't parse the file ({filePath})!\n Error: {e}")

        
def create_txt(filePath, fileName):
    '''
    Function for easy creating txt file at the given path

    filePath should be pathlib Path
    '''
    with open(filePath/fileName, 'a+'): 1