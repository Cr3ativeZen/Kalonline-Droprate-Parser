from Parser import Parser
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

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
    select = p.SELECTFROMMONSTERS()

    monsters = list(select)
    return render_template('index.html',p=p,f=f,monsters = monsters,str = str)


@app.route('/<variable>', methods=['GET'])
def homepage(variable):
    p = Parser()
    select = p.SELECTFROM("Monsters")
    monsters = list(select)
    query = "SELECT i.NAME,ROUND(igg.GroupDropChance/100*gi.ItemDropChance/100 * mig.Rolls,9) AS dropchance,igg.IDItemGroup FROM Monsters_ItemGroups mig " \
            "INNER JOIN ItemGroups ig ON mig.IDItemGroup = ig.ID" \
            " INNER JOIN ItemGroups_Groups igg ON ig.ID = igg.IDItemGroup" \
            " INNER JOIN Groups g ON igg.IDGroup = g.ID" \
            " INNER JOIN Groups_Items gi ON g.ID = gi.IDGroup" \
            " INNER JOIN Items i ON gi.IDItem = i.ID" \
            " WHERE mig.IDMonster = "+str(variable) +" ORDER BY dropchance ASC"
    if variable != 'favicon.ico':
        findmobnamequery = "SELECT NAME FROM Monsters WHERE ID ="+variable
        mobname = p.SELECT(findmobnamequery).fetchone()
        result = p.SELECT(query)

        return render_template('monster.html', p=p,str=str, float=float,monsters=monsters,ret = result,mobname = mobname)



if __name__ == "__main__":
    pass