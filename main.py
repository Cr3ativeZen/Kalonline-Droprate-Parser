import pyodbc
from Parser import Parser
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
# conn = pyodbc.connect('SQL Server};Server=DESKTOP-UB327Q5;Database=kal_db;Trusted_Connection=yes;')
#
# cursor = conn.cursor()
p = Parser()
#p.ReCreateTables()





def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app


app = Flask(__name__)
Bootstrap(app)
@app.route('/')
@app.route('/home')

def home():
    create_app()
    p = Parser()

    f = float()
    select = p.SELECTFROM("Items")

    monsters = list(select)
    for row in monsters:
        print(row)
    return render_template('index.html',p=p,f=f,monsters = monsters,str = str)


@app.route('/<variable>', methods=['GET'])
def homepage(variable):
    p = Parser()
    f = float()
    select = p.SELECTFROM("Monsters")
    monsters = list(select)
    query = "SELECT i.NAME,ROUND(igg.GroupDropChance/100*gi.ItemDropChance/100 * mig.Rolls,7) AS dropchance,igg.IDItemGroup FROM Monsters_ItemGroups mig " \
            "INNER JOIN ItemGroups ig ON mig.IDItemGroup = ig.ID" \
            " INNER JOIN ItemGroups_Groups igg ON ig.ID = igg.IDItemGroup" \
            " INNER JOIN Groups g ON igg.IDGroup = g.ID" \
            " INNER JOIN Groups_Items gi ON g.ID = gi.IDGroup" \
            " INNER JOIN Items i ON gi.IDItem = i.ID" \
            " WHERE mig.IDMonster = "+str(variable) +" ORDER BY dropchance DESC"
    print(query)
    result = p.SELECT(query)
    return render_template('monster.html', p=p, f=f,monsters=monsters,ret = result)




if __name__ == "__main__":
    app.run()

# query = "SELECT i.NAME,ROUND(igg.GroupDropChance/100*gi.ItemDropChance/100 * mig.Rolls,7) AS dropchance FROM Monsters_ItemGroups mig " \
#         "INNER JOIN ItemGroups ig ON mig.IDItemGroup = ig.ID" \
#         " INNER JOIN ItemGroups_Groups igg ON ig.ID = igg.IDItemGroup" \
#         " INNER JOIN Groups g ON igg.IDGroup = g.ID" \
#         " INNER JOIN Groups_Items gi ON g.ID = gi.IDGroup" \
#         " INNER JOIN Items i ON gi.IDItem = i.ID"
# row = p.SELECT(query)
#
# for r in row:
#     print(r[1])
    #print(str(round(r[3] *(r[8]/1000*r[13]/1000),7)))