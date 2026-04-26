# Funcs: (* - optional)
# Initialize DB (name should be Context of {SPACE NAME})
# Remove DB
# Remake DB (*) - to clear context
# Add info to DB
# Remove info from DB (*) - id for each request
# Dynamic memory (*) - for better conversation quality (faster work, less memory usage)


# Dynamic memory:
# -every request is saved to the database
# -every request got lifepoints (default=100)
# -every X (default 3) new requests/hours (then default 12) got minus X (default 5) lifepoint 
# -every time new info added to DB it is sorted (From highest to lowest amount of lifepoints)
# -if lifepoints = 0, then request is deleted from the DB
# -lifepoints are added if LLM uses them in the info search (default 10)

#Ability to take info from other spaces for one time use.

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy import insert

import os
from pathlib import Path

from random import randint, choice

#errors v
class DB_ExistsError(Exception):
    '''
    DataBase Found. New one can't be created
    '''

class DB_DontExistError(Exception):
    '''
    DataBase hasn't been found. New one should be created
    '''

class NoAddingError(Exception):
    '''
    During Session couldn't add new element to the Database.
    The changes were rolledback and the session was closed.
    '''

class NotYetImplemented(Exception):
    '''
    Not yet implemented feature.
    '''

#errors ^


class Base(DeclarativeBase):
    pass

class Request(Base):
    
    '''
    Class for requests.

    Can be put in:
    id - int (id)
    content - str (content of the request)
    lifepoints - int (health of the request)
    answ_or_resp - str (Answer Or Response)

    defaults:
    id =  random number (16 digits)
    lifepoints = 100

    Need separation between Database and Request classes because:
    DB - got funcs for managing DB
    Request - table
    '''

    __tablename__ = "Requests"

    id: Mapped[str] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String())
    lifepoints: Mapped[int] = mapped_column(Integer(), default = 100)
    answ_or_resp: Mapped[str] = mapped_column(String())
    
def __repr__(self) -> str:
        return f'Request(id={self.id}, content={self.content}, lifepoints={self.lifepoints}, Answer/Response={self.answ_or_resp})'

#main DB class
class DataBase():

    '''
    Class for DataBase Manager.
    Need separation between Database and Request classes because:
    DB - got funcs for managing DB
    Request - objects of the class should be added to the DB (table)
    '''

    
    
    def __init__(self, SaveFilePath):
        self.path_to_save_db = Path(SaveFilePath)
        self.engine = create_engine(f"sqlite:///{self.path_to_save_db/'db.sqlite3'}", echo = False)
        self.Session = sessionmaker(self.engine)
        Base.metadata.create_all(self.engine)
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.special_symbols = [
            '!',  '#', '$', '%', '&',  '(', ')', '*', '+',  
            '-', '/', ';', '<', '=', '>', '?', 
            '@',  '^', '_', '|', '~'
                  ]


  
    def new_id(self) -> str:
        '''
        Generates unique ID for each request
        '''
        a = str(randint(1, 999))
        b = choice(self.letters) + choice(self.letters)
        c = str(randint(1, 999))
        d = choice(self.special_symbols)
        f = choice(self.letters)
        result = a+b+c+d+f
        return result


    def DB_ifExists(self):
        checking = os.path.normpath(os.path.join(self.path_to_save_db/"db.sqlite3"))
        if os.path.exists(checking):
            return True
        else:
            return False



    def DB_init(self):
        '''
        Initialize Database, if no base exists
        '''
        try:
            if self.DB_ifExists():
                raise DB_ExistsError()
            else:
                Request.metadata.create_all(self.engine)
                print('--[] The database has been created!')
        except DB_ExistsError as e:
            print(f"-[!]- The database arleady exists!\nError:{e}")
   
    def DB_remove(self):
        '''
        Remove Database, if one exists
        '''
        if self.DB_ifExists():
            os.remove(self.path_to_save_db / "db.sqlite3")
            print('The database has been deleted!')
        else:
            print("The database doesn't exist!")
            raise DB_DontExistError()

    def DB_remake(self):
        '''
        Remove and Initialize database, if one exists
        (basically for clearing all data)
        '''
        self.DB_remove()
        self.DB_init()
        print("---[] Database has been remade!") 

    def DB_i_add(self, content2:str, answ_or_resp2:str, lifepoints2:int=100):
        '''
        Add something to the table:
        ID | CONTENT | LIFEPOINTS | ANSWER/QUESTION 

        ID is always automatically generated!
        '''
        id2 = self.new_id()
        new_request = Request(
            id=id2,
            content=content2,
            answ_or_resp=answ_or_resp2,
            lifepoints=lifepoints2
        )

        with self.Session() as session:
            session.add(new_request)
            session.commit()
        # with Session() as session:
        #     try:
        #         session.add(whatToAdd) #try to add smth to the table
        #     except:
        #         session.rollback() #if cannot: cancel the changes, close the session
        #         raise NoAddingError #raise relevant error
        #     else:
        #         session.commit() #if added, then commit changes


    def DB_i_remove(self): #optional
        '''
        Remove something from the table by id
        '''
        raise NotYetImplemented

    def DB_view(self):
        '''
        Print (or return) out DB contains
        Function may be useful for seeing IDs 
        '''
        with self.Session() as session:
            statement = select(Request) #select all elements
            db_object = session.scalars(statement).all() #get scalars = get elements and return all of them
            
            res = '=== DATABASE ({len(db_objects)})'
            
            return db_object
        



def testing_grounds():
    '''
    function for testing.
    well - done and ready, 
    fine - needs futher testing, 
    bad - doesn't work, 
    wrong - not the thing intented
    '''
    test = DataBase()
    # a.DB_init() #works well
    # a.DB_remove() #works well
    # a.DB_remake() # works well
    # a.DB_view() #works fine
    # a.DB_i_add() #works well
    # a.DB_i_remove() #works bad
    
    test.DB_remake()
    test.DB_view()
    test.DB_i_add('something', 'smth2')
    test.DB_i_add('something2', 'shit')
    print(test.DB_view())
    a = test.DB_view

# testing_grounds()
