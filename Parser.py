import re
import os
import pyodbc
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-UB327Q5;'
                      'Database=DropList;'
                      'trusted_source=yes;')
cursor = conn.cursor()
###

class Parser:
    def __init__(self):
        os.chdir(r'C:\Users\Mateusz\PycharmProjects\untitled')
        #self.ReCreateTables()


    def ReCreateTables(self):
        self.DROPTABLE("Items")
        self.DROPTABLE("Monsters")
        self.DROPTABLE("Groups")
        self.DROPTABLE("ItemGroups")
        self.DROPTABLE("Groups_Items")
        self.DROPTABLE("ItemGroups_Groups")
        self.DROPTABLE("Monsters_ItemGroups")

        self.EXECUTE("CREATE TABLE Items ("
                  "ID INTEGER PRIMARY KEY,"
                  "NAMEID INTEGER,"
                  "NAME varchar(255),"
                  "IMAGE varchar(255))")
        self.EXECUTE("CREATE TABLE Monsters ("
                  "ID INTEGER PRIMARY KEY,"
                  "NAMEID INTEGER,"
                  "NAME varchar(255))")
        self.EXECUTE("CREATE TABLE Groups ("
                  "ID INTEGER PRIMARY KEY)")
        self.EXECUTE("CREATE TABLE ItemGroups ("
                  "ID INTEGER PRIMARY KEY)")
        self.EXECUTE("CREATE TABLE Groups_Items ("
                  "ID INTEGER PRIMARY KEY IDENTITY,"
                  "IDGroup INTEGER,"
                  "IDItem INTEGER,"
                  "ItemDropChance FLOAT)")
        self.EXECUTE("CREATE TABLE ItemGroups_Groups ("
                  "ID INTEGER PRIMARY KEY IDENTITY,"
                  "IDItemGroup INTEGER,"
                  "IDGroup INTEGER,"
                  "GroupDropChance FLOAT)")
        self.EXECUTE("CREATE TABLE Monsters_ItemGroups ("
                  "ID INTEGER PRIMARY KEY IDENTITY,"
                  "IDMonster INTEGER,"
                  "IDItemGroup INTEGER,"
                  "Rolls INTEGER)")

        self.ItemTable()
        self.MonsterTable()
        self.ParseItemGroupIG()
        self.ParseItemGroupIM()


    def FindWordInLine(self,word,line):
        match = re.search(word,line,re.IGNORECASE)
        if match:
            return True
        else:
            return False


    def FindIntInLine(self,word,line):
        match = re.search(word +' (\d+)',line,re.IGNORECASE)
        if match:
            return int(match.group(1))


    def FindIndexAndNameInIItem(self):
        for line in open("InitItem.txt", encoding="utf8"):
            index = self.FindIntInLine('index',line)
            nameid = self.FindIntInLine('name',line)
            #image = self.FindBetweenQuotes("line")
            #print(image)
            if isinstance(nameid,int) and isinstance(index,int):
                self.INSERTINTO("Items","ID","NAMEID",str(index),str(nameid))




    def FindIndexAndNameInIMonster(self):
        for line in open("InitMonster.txt", encoding="utf8"):
            index = self.FindIntInLine('index',line)
            nameid = self.FindIntInLine('name', line)
            # image = self.FindBetweenQuotes(line)
            # print(line)
            if isinstance(nameid,int) and isinstance(index,int):
                self.INSERTINTO("Monsters", "ID", "NAMEID", str(index), str(nameid))









    def FindBetweenQuotes(self,line):
        #print(re.findall(r'\"(.+?)\"',line))
        string = re.findall(r'\"(.+?)\"',line)
        string = str(string).replace("\'","")
        string = str(string).replace("\"","")
        return  str(string).strip("['']")


    def MessageDatItemName(self):
        for line in open("message.txt", encoding='utf8'):
            if self.FindWordInLine('itemname',line):
                name = self.FindBetweenQuotes(line)
                nameid = self.FindIntInLine('itemname',line)
                if isinstance(nameid,int) and isinstance(name,str):
                    self.UPDATE("Items","NAMEID",str(nameid),"NAME",name)


    def MessageDatMonsterName(self):
        for line in open("message.txt", encoding='utf8'):
            if self.FindWordInLine('monstername',line):
                name = self.FindBetweenQuotes(line)
                nameid = self.FindIntInLine('monstername',line)
                if isinstance(nameid,int) and isinstance(name,str):
                    self.UPDATE("Monsters","NAMEID",str(nameid),"NAME",name)


    def ParseItemGroupIMInLine(self,line,index):
        #for str in line.split():
        #print(re.findall(r'(itemgroup (\d+) (\d+))', line))
        for string in re.findall(r'(itemgroup (\d+) (\d+))',line):
            #print(string[1] + " " + string[2])
            if isinstance(string[1], str) and isinstance(string[2], str) and isinstance(index,int):
                self.INSERTINTO("Monsters_ItemGroups","IDMonster","IDItemGroup","Rolls",str(index),string[1],string[2])

    def ParseItemGroupIM(self):
        for line in open("InitMonster.txt",encoding='utf8'):
            if self.FindWordInLine('index',line):
                index = self.FindIntInLine('index',line)
                self.ParseItemGroupIMInLine(line,index)


    def ParseItemGroupIGInLine(self,line):
        values = re.findall(r'((.+?) )',line)
        for stre in values:
            for s in stre:
                if s == '(item' and not self.FindWordInLine("money",line):
                    i = iter(values)
                    i.__next__()
                    i.__next__()
                    id = i.__next__()
                    id = str(id[0]).replace(")","")
                    query = "SELECT * FROM [DropList].[dbo].[Groups] WHERE ID = "+str(id)
                    #print(query)
                    cursor.execute(query)
                    if cursor.rowcount == 0:
                        self.INSERTINTO("Groups","ID",str(id))
                        i.__next__()
                        first = True
                        last_chance = 0
                        while True:
                            try:
                                value = i.__next__()
                                chance = re.findall('\d+',value[0])      #chance
                                if first == False:
                                    chance[0] = int(chance[0]) - int(last_chance)

                                value = i.__next__()
                                itemid = re.findall('\d+',value[0])      #id
                                new_index = str(id).replace(")","")
                                value3 = i.__next__()
                                self.INSERTINTO("Groups_Items","IDGroup","IDItem","ItemDropChance",str(new_index),str(itemid[0]),str(chance[0]))
                                first = False
                                last_chance = last_chance +int(chance[0])
                            except StopIteration:
                                self.INSERTINTO("Groups_Items", "IDGroup", "IDItem", "ItemDropChance", str(new_index),str(itemid[0]), str(chance[0]))
                                break


    def ParseItemGroupIGInLine2(self,line):
        values = re.findall(r'\b\d+\b',line)
        #print(values)
        flag = True


        if self.FindWordInLine("\(itemgroup",line):

            for stre in values:
                if flag == True:
                    #print(stre)
                    i = iter(values)

                    id = i.__next__()#id
                    #print("KEKW")
                    #print(id)
                    query = "SELECT * FROM [DropList].[dbo].[ItemGroups] WHERE ID = "+str(id)
                    cursor.execute(query)
                    if cursor.rowcount == 0:
                        self.INSERTINTO("ItemGroups","ID",str(id))

                    first = True
                    last_chance = 0
                    while True:
                        try:
                            chance = i.__next__()                    #chance
                            #print(chance)
                            if first == False:
                                chance = int(chance) - int(last_chance)

                            #print(chance)
                            groupID = i.__next__()
                            self.INSERTINTO("ItemGroups_Groups","IDItemGroup","IDGroup","GroupDropChance",str(id),str(groupID),str(chance))
                            first = False
                            last_chance = last_chance + int(chance)
                        except StopIteration:
                            flag = False
                            #self.INSERTINTO("ItemGroups_Groups","IDItemGroup","IDGroup","GroupDropChance",str(id),str(groupID),str(chance))
                            break



    def ParseItemGroupIG(self):
        for line in open("ItemGroup.txt"):
            if self.FindWordInLine('group',line):
                self.FindIntInLine('group',line)
                self.ParseItemGroupIGInLine(line)
                self.ParseItemGroupIGInLine2(line)
    #strip deletes the extra quotes from integer.


    def ItemTable(self):
        self.FindIndexAndNameInIItem()
        self.MessageDatItemName()

    def MonsterTable(self):
        self.FindIndexAndNameInIMonster()
        self.MessageDatMonsterName()


    def CREATETABLE(self, tablename, value1, value2, value3, value4, type1, type2, type3,type4):
        query = "CREATE TABLE " + tablename + " (" + str(value1) + " " + str(type1) + "," + str(value2) + " " + str(
            type2) + "," + str(value3) + " " + str(type3) +"," + str(value4) + " " + str(type4) + ");"
        #print(query)
        cursor.execute(query)
        conn.commit()

    def TRUNCATETABLE(self, tablename):
        query = "TRUNCATE TABLE " + tablename
        cursor.execute(query)
        conn.commit()


    def INSERTINTO(self,tablename, *argv):
        i =0
        query = "INSERT INTO "+tablename+"("
        for arg in argv:
            i = i + 1
            if i <= len(argv)/2:
                query = query + str(arg) +","


        query = query[:-1] + ") VALUES ("
        i = 0
        for arg in argv:
            i = i + 1
            if i > len(argv)/2 and i <= len(argv):
                query = query + str(arg) + ","

        query = query[:-1] + ")"
        # if len(argv) == 2:
        #     query = query[:-1]

        #print(query)

        cursor.execute(query)
        conn.commit()


    def UPDATE(self,tablename,column_where,value, *argv):
        flag = False
        query = "UPDATE "+tablename + " SET "
        for arg in argv:
            if flag == False:
                query = query+str(arg)+ " = "
                flag = True
            else:
                query = query+"\'" + str(arg) +"\'" + " ,"
                flag = False

        query = query[:-1]
        query = query + "WHERE " + column_where +" = " + str(value)

        #print(query)

        cursor.execute(query)
        conn.commit()


    def DELETEFROM(self,tablename):
        query = "DELETE FROM "+ tablename
        cursor.execute(query)
        conn.commit()


    def SELECTFROM(self,tablename):
        query = "SELECT * FROM "+tablename
        cursor.execute(query)

        row = cursor.fetchall()
        return row

    def SELECT(self,query):
        cursor.execute(query)
        row = cursor
        return row

    def EXECUTE(self,query):
        #print(query)
        cursor.execute(query)
        conn.commit()

    def DROPTABLE(self,tablename):
        query = "DROP TABLE "+ str(tablename)
        #print(query)
        cursor.execute(query)
        conn.commit()
