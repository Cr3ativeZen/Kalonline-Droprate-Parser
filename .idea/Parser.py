import re
from enum import Enum
import pyodbc
## TO DO
## FRONT-END missing

class Switch(Enum):
    LOWER_THAN = 0
    HIGHER_THAN = 1


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-H8GTJHQ\SQLEXPRESS;'
                      'Database=DropList;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

class Parser:
    def __init__(self):
        self.DELETETABLE("IMItemGroup")
        self.DELETETABLE("ItemTable")
        self.DELETETABLE("MonsterTable")

        self.DELETETABLE("ItemGroup")
        self.initmonster = "InitMonster.txt"
        self.class_container = {}
        self.messagedat = "message.txt"
        self.itemgroup = "ItemGroup.txt"
        self.inititem = "InitItem.txt"
        self.monsternamedictionary = {}
        self.MonsterName()
        self.itemnamedictionary = {}
        self.ItemName()
        self.itemgroupdictionary = {}
        self.ItemGroup()
        self.IGGroup_item = {}
        self.IGGroup_money = {}
        self.IGGroup()
        self.itemiconsdictionary = {}
        self.ItemIcons()
        self.IMItemGroupRead()




    def MainMethod(self, keyword="index"):
        for line in open(self.initmonster):
            index = self.FindIndex(keyword, line)
            indexname = self.FindIndex("name",line)
            mobname = self.monsternamedictionary.get(indexname)
            if index != 0:
                self.class_container[str(index)] = self.IMItemGroup(line)
                for i in self.class_container[index]:
                    temp = self.itemgroupdictionary.get(str(i))
                    #print(temp)
                    print(mobname)
                    #print(self.class_container[index])
                    for x,y in temp.items():
                         temp_container = {}
                         temp_money_container = {}
                         temp_money_container = self.IGGroup_money.get(str(x))
                         temp_container = self.IGGroup_item.get(str(x))

                         print("------------------------------------------------")
                         for a,b in temp_container.items():
                                drop_rate = self.CalculateTotalDropRate(i, x, a, index, Switch.LOWER_THAN)
                                print(str(round(float(drop_rate * 100),5)) +"% " + str(a))






    # def GetIGValues(self,id,switchx):
    #     if switchx == "item":
    #         return self.IGGroup_item[id]
    #     elif switchx == "money":
    #         return self.IGGroup_money[id]

    def GetItemGroupChance(self,itemgroupID,groupID,switchx):
        group_chance = self.itemgroupdictionary.get(str(itemgroupID)).get(str(groupID))
        return self.Calculate(itemgroupID,switchx,self.itemgroupdictionary,group_chance)

    def GetItemDropChance(self,groupID,itemID,switchx):
        if switchx == Switch.LOWER_THAN:
            group_chance = self.IGGroup_item.get(str(groupID))
            return self.Calculate(groupID,switchx,self.IGGroup_item,group_chance[itemID])
        elif switchx == Switch.HIGHER_THAN:
            return self.Calculate(groupID,switchx,self.IGGroup_money)

    def GetTotalBagDrop(self,mobID,groupID):
        return self.class_container.get(str(mobID)).get(groupID)

    def CalculateTotalDropRate(self,itemgroupID,groupID,itemID,mobID,switchx):
        item_group_chance = self.GetItemGroupChance(itemgroupID,groupID,switchx)
        item_drop_chance = self.GetItemDropChance(groupID,itemID,switchx)
        #total_bag = self.GetTotalBagDrop(mobID,groupID)
        return float(item_group_chance) * float(item_drop_chance) #* float(total_bag)

    def Calculate(self,groupID,switchx,dict1 = {},chance = 0):
        element = 0
        temp = {}
        temp = dict1.get(str(groupID))
        if switchx == Switch.LOWER_THAN:
            for x, y in temp.items():
                if int(y) < int(chance):
                    element = int(y)
            if element == 0 and dict1 == self.IGGroup_item and self.IGGroup_money.get(groupID):
                 element = self.Calculate(groupID,Switch.HIGHER_THAN,self.IGGroup_money)
            return (int(chance) - int(element)) / 1000

        elif switchx == Switch.HIGHER_THAN:
            for x, y in temp.items():
                if int(y) > int(chance):
                    element = int(y)
            return (int(element))


    def IMItemGroupRead(self,line="",keyword="itemgroup"):
        for linew in open(self.initmonster):
            regex = r'\w+'
            list1 = re.findall(regex, linew)
            temp_container = {}
            counter = 0
            for i in list1:
                counter = counter + 1
                if i == keyword:
                    temp_container[list1[counter]] = list1[counter + 1]
                else:
                    pass
            if bool(temp_container):
                index = self.FindIndex("index",linew)
                print(str(index))
                for itemgroup_id,rolls in temp_container.items():
                    self.InsertIntoIMItemGroup(itemgroup_id,index,rolls)


    def IMItemGroup(self,line="",keyword="itemgroup"):
            regex = r'\w+'
            list1 = re.findall(regex, line)
            temp_container = {}
            counter = 0
            for i in list1:
                counter = counter + 1
                if i == keyword:
                    temp_container[list1[counter]] = list1[counter + 1]
            return temp_container

    def IGGroup(self,keyword="group"):
        for line in open(self.itemgroup):
            regex = r'\w+'
            list1 = re.findall(regex, line)
            index = self.FindIndex("index",line)

            if "index" in list1:
                check1 = list1.index("index") + 1
            else:
                check1 = 0
            if str(index) in list1:
                check2 = list1.index(str(index))
            else:
                check2 = -2

            temp_dic_money = {}
            temp_dic_item = {}

            if ("money" in list1 and str(index) in list1) and check1 == check2:
                pos = list1.index("money") + 1
                while pos + 1 < len(list1) and self.Is_int(list1[pos]) and self.Is_int(list1[pos+1]):
                    temp_dic_money[list1[pos + 1]] = list1[pos]
                    self.IGGroup_money[index] = temp_dic_money
                    pos += 2

            if ("item" in list1 and str(index)  in list1) and check1 == check2:
                pos = list1.index("item") + 1
                while pos + 1 < len(list1) and self.Is_int(list1[pos]) and self.Is_int(list1[pos+1]):
                    temp_dic_item[list1[pos + 1]] = list1[pos]
                    self.IGGroup_item[index] = temp_dic_item
                    self.InsertIntoItemGroup(list1[pos + 1],index,list1[pos])
                    pos += 2
        # print(self.IGGroup_money)
        # print(self.IGGroup_item)


    def FindIndex(self,keyword="",line=""):
            match = re.search(str(keyword) +" " + "(\d+)", line)
            if match:
                return match.group(1)
            else:
                return 0

    def MonsterName(self, keyword = "monstername"):
         for line in open(self.messagedat):
            index = self.FindIndex(keyword,line)
            if line[0] != ";":
                start = line.find("\"") + 1
                end = line.rfind("\"")
                if index != 0:
                    self.monsternamedictionary[index] = line[start:end]
                    self.InsertIntoMonsterTable(index,line[start:end])


    def ItemIcons(self,keyword = "Index"):
        for line in open(self.inititem,encoding="latin-1"):
            index = self.FindIndex(keyword, line)
            start = line.find("\"") + 1
            end = line.rfind("\"")
            if index != 0:
                self.itemiconsdictionary[index] = line[start:end] +".bmp"
                self.UpdateTableItemList(index,line[start:end]+".bmp")



    def ItemName(self, keyword = "itemname"):
         for line in open(self.messagedat,encoding="latin-1"):
            if line.find("itemname ") and line[0] != ";":
                index = self.FindIndex(keyword,line)
                start = line.find("\"") + 1
                end = line.rfind("\"")
                if index != 0:
                    self.itemnamedictionary[index] = line[start:end]
                    self.InsertIntoTableItemList(index, line[start:end])

    def ItemGroup(self, keyword="index"):
        for line in open(self.itemgroup):
            if line.find("itemgroup") and line[0] != ";":
                index = self.FindIndex(keyword,line)
                regex = r'\w+'
                list1 = re.findall(regex, line)
                temp_dic = {}
                i = 0
                while i < len(list1):
                    if list1[i] == "group":
                       i += 1
                       while i + 1 < len(list1) and self.Is_int(list1[i]) != 0:
                            temp_dic[list1[i+1]] = list1[i]
                            self.itemgroupdictionary[index] = temp_dic
                            i += 2
                    else:
                        i += 1



    def InsertIntoTableItemList(self,ID,NAME,tablename="ItemList"):
        NAME = NAME.replace('\'','')
        NAME = NAME.replace('\"','')

        query = "INSERT INTO ItemTable(ID, NAME) VALUES ("+str(ID)+', \''+ NAME +"\')"
        print(query)
        cursor.execute(query)
        conn.commit()

    def InsertIntoMonsterTable(self,ID,NAME,tablename="ItemList"):
        NAME = NAME.replace('\'','')
        NAME = NAME.replace('\"','')
        query = "INSERT INTO MonsterTable(ID, MonsterName) VALUES ("+str(ID)+', \''+ NAME +"\')"
        print(query)
        cursor.execute(query)
        conn.commit()

    def UpdateTableItemList(self,ID,IMAGE="",tablename="ItemList"):
        # IMAGE = IMAGE.replace('\'','')
        # IMAGE = IMAGE.replace('\"','')
        if len(IMAGE) > 20:
            return
        query = "UPDATE ItemTable SET IMAGE = \'"+ IMAGE +"\' WHERE ID = "+str(ID)
        print(query)
        cursor.execute(query)
        conn.commit()



    def InsertIntoIMItemGroup(self,mob_id,itemgroup_id,rolls):
        query = "INSERT INTO IMItemGroup(ID,Rolls,MonsterID) VALUES("+str(mob_id)+", "+str(rolls)+", "+str(itemgroup_id)+")"
        print(query)
        cursor.execute(query)
        conn.commit()


    def InsertIntoItemGroup(self,group_id,itemgroup_id,groupchance):
        query = "INSERT INTO ItemGroup(ID,ItemGroupID,GroupChance) VALUES("+str(group_id)+", "+str(itemgroup_id)+", "+str(groupchance)+")"
        print(query)
        cursor.execute(query)
        conn.commit()


    def SELECTFROM(self,tablename):
        query = "SELECT * FROM "+ tablename
        cursor.execute(query)

        for row in cursor:
            print(row)
    def DELETETABLE(self,tablename):
        query = "DELETE FROM "+tablename
        cursor.execute(query)
        conn.commit()


    def CREATETABLE(self,tablename,value1,value2,value3,type1,type2,type3):
        query = "CREATE TABLE " + tablename +" (" +str(value1) +" " + str(type1) + "," + str(value2) +" " + str(type2) + "," +str(value3) +" " + str(type3) + ");"
        print(query)
        cursor.execute(query)
        conn.commit()


    def EXECUTEQUERY(self,query=""):
        cursor.execute(query)
        conn.commit()

    def Is_int(self,s):
        try:
            int(s)
            return True
        except ValueError:
            return False