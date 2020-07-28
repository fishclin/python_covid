import flask
from flask import request, jsonify
import MySQLdb
import random
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def query_handle(query):
    db = MySQLdb.connect("localhost", "root", "", "covid")
    cursor = db.cursor()
    # If not such database, create one
    #try:
        #cursor.execute("USE mysql")
        #cursor.execute("CREATE TABLE tasks (id INT PRIMARY KEY AUTO_INCREMENT,title VARCHAR(64) NOT NULL,is_completed BOOLEAN, notify VARCHAR(64));")
    #except:
        #pass
    
    cursor.execute(query)
    return db, cursor


# week
@app.route('/t1/week')
def get_t1_week():

  tasks = []
  query =  "select @curRank := @curRank + 1 AS Rank, Province_State, Country_Region, Incidence_Rate from report_new, ( SELECT @curRank := 0 ) q where YEARWEEK(date_format(Last_Update,'%Y-%m-%d')) = YEARWEEK(now())-1 order by Incidence_Rate desc limit 10;"
  db, cursor = query_handle(query)
  results = cursor.fetchall()
  for row in results:
    task = {}
    task['Rank'] = row[0]
    task['Province_State'] = row[1]
    task['Country_Region'] = row[2]
    #task['Incidence_Rate'] = row[3]
    tasks.append(task)
  db.close()

  return jsonify(tasks), 200

# month
@app.route('/t1/month')
def get_t1_month():

  tasks = []
  query =  "select @curRank := @curRank + 1 AS Rank, Province_State, Country_Region, Incidence_Rate from report_new, ( SELECT @curRank := 0 ) q where DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(Last_Update) order by Incidence_Rate desc limit 10;"
  db, cursor = query_handle(query)
  results = cursor.fetchall()
  for row in results:
    task = {}
    task['Rank'] = row[0]
    task['Province_State'] = row[1]
    task['Country_Region'] = row[2]
    #task['Incidence_Rate'] = row[3]
    tasks.append(task)
  db.close()

  return jsonify(tasks), 200

# season
@app.route('/t1/season')
def get_t1_season():

  tasks = []
  query =  "select @curRank := @curRank + 1 AS Rank, Province_State, Country_Region, Incidence_Rate from report_new, ( SELECT @curRank := 0 ) q where QUARTER(Last_Update)=QUARTER(DATE_SUB(now(),interval 1 QUARTER)) order by Incidence_Rate desc limit 10;"
  db, cursor = query_handle(query)
  results = cursor.fetchall()
  for row in results:
    task = {}
    task['Rank'] = row[0]
    task['Province_State'] = row[1]
    task['Country_Region'] = row[2]
    #task['Incidence_Rate'] = row[3]
    tasks.append(task)
  db.close()

  return jsonify(tasks), 200

app.run(port=5001)
