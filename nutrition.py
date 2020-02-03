import mysqlx
import getpass
import re
from difflib import SequenceMatcher as SeqMatch
class Connector:
    
    def __init__(self):
        
        #self.username = input("Username: ")
        #self.password = getpass.getpass()
        self.username = "chris"
        self.password = "mysql"
        self.foodTable = ''
        self.nutTable = ''
        self.defTable = ''
        self.wgTable = ''
        self.fgTable = ''
        self.connect()
        
    def connect(self):
        
        while True:
            try:
                session = mysqlx.get_session({
                    'host': 'localhost', 'port': 33060, \
                    'user': self.username, \
                    'password': self.password})
                db = session.get_schema('USDA_Nutrition')
                self.foodTable = db.get_table('Food_Description')
                self.nutTable = db.get_table('Nutrition_Data')
                self.defTable = db.get_table('Nutrient_Definition')
                self.wgTable = db.get_table('Weight')
                self.fgTable = db.get_table('Food_Group')
                break
            except:
                print("Oops! Username or password are invalid. Please Try again...")
                print("Press control-c to exit.")
                self.__init__()
    
    def foodSearch(self,search):
        seaList = re.split('[ ,.;:]',search)
        while(seaList.count('')):
            seaList.remove('')
 
        res = self.foodTable.select()
        if not seaList:
            return
        if(len(seaList) > 1):
            whereString = 'Ldes like :' + seaList[0]
            
            for word in range(1,len(seaList)):
                whereString = whereString + ' and Ldes like :' + seaList[word]
            
            res.where(whereString)
                 
            for word in range(0,len(seaList)):
                res.bind(seaList[word],'%{}%'.format(seaList[word]))
        
        else:
            res.where('Ldes like :' + seaList[0])
            res.bind(seaList[0],'%{}%'.format(seaList[0]))
            
        res = res.execute().fetch_all()

        #sort search results by relevance
        res = sorted(res,key=lambda row: SeqMatch(None,row[2],*seaList).ratio(),reverse=True)
        
        return res[:25]
    
    def nutData(self, dbNum):
        res = self.nutTable.select().where('DBnum=:dbNum') \
                        .bind('dbNum','{}'.format(dbNum)) \
                        .execute() \
                        .fetch_all()
        
        return res

    def defSearch(self,nut):
        res = self.defTable.select('Units','Nutr_Desc').where('Nutr_Num=:nut') \
                    .bind('nut',nut) \
                    .execute() \
                    .fetch_one()
        
        return res

    def wgSearch(self,dbNum):
        res = self.wgTable.select('Amount','Unit','Grams').where('DBnum=:dbNum') \
                    .bind('dbNum',dbNum) \
                    .execute() \
                    .fetch_all()
        return res

    def fgSearch(self):
        res = self.fgTable.select() \
                    .execute() \
                    .fetch_all()
        
        for row in range(0,len(res)):
            print(str(row+1) + ': ' + res[row][1])
            
        choice = int(input("What food group would you like to see? "))-1
        
        return res[choice]
            

    def test(self,nut):
        food = nut.foodSearch()
        print(list(food))
        
        dbNum = nut.nutData('01001')
        for row in dbNum:
            print(list(row))
        
        defi = nut.defSearch('203')
        print(list(defi))
        
        wg = nut.wgSearch('01001')
        for row in wg:
            print(list(row))
            
        fg = nut.fgSearch()
        print(list(fg))

