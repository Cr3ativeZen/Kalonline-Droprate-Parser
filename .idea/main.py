from Parser import Parser
from Parser import Switch
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import pyodbc
import os
import re


#p = Parser()
#
# p.InsertIntoTableItemList(1,"qweqwdqwd")
# p.InsertIntoTableItemList(4,"fweferf")
# p.InsertIntoTableItemList(7,"wffgwgw")

#p.SELECTFROM("ItemTable")


#p.CREATETABLE("ItemTable","ID","NAME","IMAGE","int","varchar(255)","varchar(255)")



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
    #p.MainMethod()
    s= Switch(0)
    f = float()



    with open('initmonster.txt', 'r') as file:
        data = file.read()

    return render_template('index.html',p=p,data=data,s=s,f=f,icon_names = p.itemiconsdictionary)



@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)


p = Parser()


print(p.IGGroup_item)
for i in p.IGGroup_item.get('1000'):
    print(i)