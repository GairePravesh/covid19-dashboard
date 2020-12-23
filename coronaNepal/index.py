from typing import Optional
# from fastapi import FastAPI

from flask import Flask, session
app = Flask(__name__)
# app.secret_key = "hello"
# app.permanent_session_lifetime = timedelta(minutes=5)

import requests

from db import db

# app = FastAPI()
database= db()

@app.route("/")
def read_root7():
    return {"Hello": "World"}


@app.route("/data")
def read_root6():
  # r = requests.get(env.DataAPI) 
  # data = r.json() 
  # return data
  db.insertmapCoordinate([1.1,2.1,3.1,4.1])

@app.route("/district")
def read_root5():
  r = requests.get(env.DistrictList)
  data = r.json() 

  for index in data:
    districtid=index["id"]
    bbox=index["bbox"]
    name=index["title_en"]
    code =index["code"]
    centroid=index["centroid"]["coordinates"]
    province=index["province"]

    bboxkey= db.insertmapCoordinate(bbox)
    # print(bboxkey)
    centroidkey= db.insertCoordinate(centroid)
    # print(centroidkey)

    db.insertDistrict(districtid, name,"",code,province,centroidkey,bboxkey)
    # break

  return "True"
  # db.insertmapCoordinate([1.1,2.1,3.1,4.1])

  


  # for x in data:
    # print(x)
  # print(insertsql)
  
  # return x
  # mycursor.close()


  # sql="select *from mapCoordinate"
  # mycursor.execute(sql)

  # print( mycursor.fetchall())

@app.route("/municipality")
def read_root4():
  r = requests.get(env.MunicipalityList)
  data = r.json() 

  for index in data:
    municipalityid=index["id"]
    bbox=index["bbox"]
    name=index["title_en"]
    code =index["code"]
    typ=index["type"]
    centroid=index["centroid"]["coordinates"]
    
    print(code)
    bboxkey= db.insertmapCoordinate(bbox)
    # print(bboxkey)
    centroidkey= db.insertCoordinate(centroid)
    # print(centroidkey)

    db.insertMunicipality(municipalityid,bboxkey,name,"",code,typ,centroidkey)
    # break

  return "True"

@app.route("/location")
def read_root3():
  r = requests.get(env.MunicipalityList)
  data = r.json() 

  for index in data:
    municipalityid=index["id"]
    districtid=index["district"]
    db.insertLocation(municipalityid,districtid)
    # break

  return "True"


@app.route("/individual")
def read_root2():
  r = requests.get(env.IndividualList)
  data = r.json() 

  for index in data:
    print (index)
    status=index["currentState"]
    isreinfected=True#index["isReinfected"]
    typ=index["type"]
    deadon= index["deathOn"]
    reportedon=index["reportedOn"]
    recoveredon=index["recoveredOn"]
    # print(status)
    # print(isreinfected)
    # print(typ)
    # print(deadon)
    # print(recoveredon)
    statusid= db.insertStatus(status,isreinfected,typ,deadon,reportedon,recoveredon)
    
    centroid=index["point"]["coordinates"]
    coordinateid= db.insertCoordinate(centroid)
    
    id2=index["id"]
    value=index["label"]
    gender=index["gender"]
    age=index["age"]
    occupation=index["occupation"]
    createdon=index["createdOn"]
    modifiedon=index["modifiedOn"]
    # statusid
    # centroidkey
    # print(index["municipality"])
    locationid=db.searchLocation(index["municipality"])
    
    print(id2)
    print(value)
    print(gender)
    print(age)
    print(occupation)
    print(createdon)
    print(modifiedon)
    print(locationid)

    db.insertIndividual(id2,value,gender,age,occupation,createdon,modifiedon,locationid,statusid,coordinateid)
    # break

  return "True"



@app.route("/individualcheck")
def read_root1():
  r = requests.get(env.IndividualList)
  data = r.json() 

  datatemp= db.readIndividualid()
  dataDB=[]
  for datum in datatemp:
    if datum[0]!= None:
      dataDB.append(datum[0])
  print(dataDB)
  cnt=0

  for index in data:
    # print (index)
    id2=index["id"]
    status=index["currentState"]
    isreinfected=True#index["isReinfected"]
    typ=index["type"]
    deadon= index["deathOn"]
    reportedon=index["reportedOn"]
    recoveredon=index["recoveredOn"]

    if (id2 in dataDB):
      print(id2)
      print("pass")
      continue
    
    print(status)
    print(isreinfected)
    print(typ)
    print(deadon)
    print(recoveredon)
    statusid= db.insertStatus(status,isreinfected,typ,deadon,reportedon,recoveredon)
    
    centroid=index["point"]["coordinates"]
    coordinateid= db.insertCoordinate(centroid)
    
    
    value=index["label"]
    gender=index["gender"]
    age=index["age"]
    occupation=index["occupation"]
    createdon=index["createdOn"]
    modifiedon=index["modifiedOn"]
    # statusid
    # centroidkey
    # print(index["municipality"])
    locationid=db.searchLocation(index["municipality"])
    
    print(id2)
    print(value)
    print(gender)
    print(age)
    print(occupation)
    print(createdon)
    print(modifiedon)
    print(locationid)

    db.insertIndividual(id2,value,gender,age,occupation,createdon,modifiedon,locationid,statusid,coordinateid)
    # break

  return "True"


# @app.get("/individualupdate")
# def read_root():
#   r = requests.get(env.IndividualList)
#   data = r.json() 

#   datatemp= db.readIndividualid()
#   dataDB=[]
#   for datum in datatemp:
#     if datum[0]!= None:
#       dataDB.append(datum[0])
#   print(dataDB)
  
#   for index in data:
#     print (index)
#     id2=index["id"] 
#     status=index["currentState"]
#     isreinfected=True#index["isReinfected"]
#     typ=index["type"]
#     deadon= index["deathOn"]
#     reportedon=index["reportedOn"]
#     recoveredon=index["recoveredOn"]
#     if (id2 in dataDB):
#       pass
#     else:
#       break
#     statusid= db.insertStatus(status,isreinfected,typ,deadon,reportedon,recoveredon)
    
#     centroid=index["point"]["coordinates"]
#     coordinateid= db.insertCoordinate(centroid)
    
    
#     value=index["label"]
#     gender=index["gender"]
#     age=index["age"]
#     occupation=index["occupation"]
#     createdon=index["createdOn"]
#     modifiedon=index["modifiedOn"]
#     # statusid
#     # centroidkey
#     # print(index["municipality"])
#     locationid=db.searchLocation(index["municipality"])
    
#     print(id2)
#     print(value)
#     print(gender)
#     print(age)
#     print(occupation)
#     print(createdon)
#     print(modifiedon)
#     print(locationid)

#     db.insertIndividual(id2,value,gender,age,occupation,createdon,modifiedon,locationid,statusid,coordinateid)
#     # break

#   return True


@app.route("/dataapi")
def read_data():
  a=db.readIndividual()
  return a

@app.route("/datadistrict")
def read_district():
  a=db.readDistrict()
  return a

@app.route("/dataMun")
def read_mun():
  a=db.readMun()
  return a


# @app.route("/adduser")
# def adduser():
#   if len( db.checkemail('znedrfii','sdf'))==0:
#     return "True"
#   else:
#     return "False"  
#   # db.insertuser("znerfii","znerfii.a1@gmail.com","database1")
#   return "True"

# def login():
#   if len( db.checklogin('znedrfii','database1'))==0:
#     session["user"] = user
#     session["key"] =
#   else:
#     return "False"  
@app.route("/dataprovince")
def readpro():
  return db.readProvince()
  
@app.route("/province")
def read_pro():
  db.deletepro()
  a= db.readIndividualnon()
  district=db.readDistrictnon()
  # print(district)
  p1=0
  p2=0
  p3=0
  p4=0
  p5=0
  p6=0
  p7=0
  # print(len(a))
  print(a[0][10])
  for data in a:
    if (data[5]!='active'):
      continue
    for dist in district:
      print(dist)
      if(dist[0]==data[10]):
        pro=dist[3]
        break 
    # print(data[6])
    if (pro==1):
      p1=p1+1
    elif (pro==2):
      p2=p2+1
    elif (pro==3):
      p3=p3+1
    elif (pro==4):
      p4=p4+1
    elif (pro==5):
      p5=p5+1
    elif (pro==6):
      p6=p6+1
    elif (pro==7):
      p7=p7+1
    
  db.insertprovince(1,"Province No. 1",'p1',p1,14534943)
  db.insertprovince(2,"Province No. 2",'p2',p2,5404145)
  db.insertprovince(3,"Bagmati Province",'p3',p3,5529452)
  db.insertprovince(4,"Gandaki Province",'p4',p4,2403757)
  db.insertprovince(5,"Lumbini Province",'p5',p5,4499272)
  db.insertprovince(6,"Karnali Province",'p6',p6,1570418)
  db.insertprovince(7,"Sudurpashchim Province",'p7',p7,2552517)
  
  return "True"


@app.route('/gender')
def gender():
  a = db.readgender()
  return a 

@app.route('/occupation')
def occupation():
  a = db.readoccupation()
  return a 

@app.route('/age')
def age():
  a = db.readage()
  return a 


if __name__ == "__main__":
    app.run(debug=True)

