import mysql.connector as sql
import getpass
import re
from difflib import SequenceMatcher as SeqMatch
class Connector:
    
    def __init__(self):
        """Initialize Connector()."""
        
        #self.username = input("Username: ")
        #self.password = getpass.getpass()
        self.username = 'chris'
        self.password = 'mysql'
        self.cursor=''
        self.__connect()
        
    def __connect(self):
        """Connect to mysql like database."""
        while True:
            try:
                self.session = sql.connect(user=self.username,
                                           password=self.password,
                                           database='USDA_Nutrition')
                self.cursor = self.session.cursor()
                break
            except:
                print("Oops! Username or password are invalid. Please Try again...")
                print("Press control-d to exit.")
                self.username = input("Username: ")
                self.password = getpass.getpass()
    
    def foodSearch(self,search):
        """Return 25 most relevant ingredients from database based on search terms.
        
        Keyword arguments:
        search -- string to search for (e.g. 'salted butter')
        """
        
        #split string on certain non text characters
        seaList = re.split('[ ,.;:]',search)
        while(seaList.count('')):
            seaList.remove('')
 
        if not seaList:
            return
        
        sqlstring = "select * from Food_Description where Ldes like '%{}%'".format(seaList[0])
        
        if(len(seaList) > 1):
            for word in range(1,len(seaList)):
                sqlstring.join(' and Ldes like "%{}%"'.format(seaList[word]))
                 
        self.cursor.execute(sqlstring)
        res = self.cursor.fetchall()

        #sort search results by relevance
        res = sorted(res,key=lambda row: SeqMatch(None,res[2],*seaList).ratio(),reverse=True)
        
        return res[:25]
    
    def nutData(self, dbNum):
        """Return the nutrition data for an ingredient.
        
        Keyword arguments:
        dbNum -- database number as a string (e.g. '01001' = Butter, salted)
        """
        
        self.cursor.execute('select * from Nutrition_Data where DBnum={}'.format(dbNum))
        return self.cursor.fetchall()

    def defSearch(self,nut=None):
        """Return nutrient weight unit and definition.
        
        Keyword arguments:
        nut -- nutrient number as a string (e.g. '203' = protein),
            to show all nutrients exclude this.
        """
        if not nut:
            self.cursor.execute('select Units, Nutr_Desc from Nutrient_Definition')
            return self.cursor.fetchall()
        
        self.cursor.execute('select Units, Nutr_Desc from Nutrient_Definition where Nutr_Num={}'.format(nut))
        return self.cursor.fetchall()

    def wgSearch(self,dbNum):
        """Return known volumes and weights for an ingredient.
        
        Keyword arguments:
        dbNum -- database number as a string (e.g. '01001' = Butter, salted)
        """
        
        self.cursor.execute('select Amount, Unit, Grams from Weight where DBnum={}'.format(dbNum))
        return self.cursor.fetchall()

    def fgSearch(self):
        """Return chosen food group number and description that is searchable in database.
        
        Returns:
        returns a tuple ('food group #', 'food group description')
        """
        
        self.cursor.execute('select * from Food_Group')
        res = self.cursor.fetchall()
        for row in range(0,len(res)):
            print(str(row+1) + ': ' + res[row][1])
            
        choice = int(input("What food group would you like to see? "))-1
        
        return res[choice]
