
import mysql.connector

import json

mydb = mysql.connector.connect(            
            user='corona',
            password='corona',
            database='test'
        )
mycursor = mydb.cursor()

class db:
    def __init__(self):
        pass

    def insertmapCoordinate(b):
        sql = ("""INSERT INTO mapCoordinate (bbox1, bbox2, bbox3, bbox4) VALUES (%s,%s,%s,%s) """)
        # OUTPUT Inserted.mapid
        val=(b[0],b[1],b[2],b[3])
        mycursor.execute(sql, val)
        mydb.commit()
        
        return mycursor.lastrowid

    def insertCoordinate(b):
        sql = ("""INSERT INTO coordinate (x, y) VALUES (%s,%s) """)

        val=(b[0],b[1])
        mycursor.execute(sql, val)
        mydb.commit()
        
        return mycursor.lastrowid

    def insertDistrict(districtid,name,nepaliname,code,province,centroidcoordinate,bbox):
        sql = ("""INSERT INTO district (`districtid`,`name`,`nepali-name`,`code`,`province`,`centroid-coordinate`,`bbox`) VALUES (%s,%s,%s,%s,%s,%s,%s) """)

        val=(districtid, name,nepaliname,code,province,centroidcoordinate,bbox)
        mycursor.execute(sql, val)
        mydb.commit()
        
        return mycursor.lastrowid

    def insertMunicipality(municipalityid,bboxkey,name,nepaliname,code,typ,centroidkey):
        sql = ("""INSERT INTO municipality (`municipalityid`,`bbox`,`name`,`nepali-name`,`code`,`type`,`centroid-coordinate`) VALUES (%s,%s,%s,%s,%s,%s,%s) """)

        val=(municipalityid,bboxkey,name,nepaliname,code,typ,centroidkey)
        mycursor.execute(sql, val)
        mydb.commit()
        
        return mycursor.lastrowid
    
    def insertLocation(municipalityid,districtid):
        sql = ("""INSERT INTO location (`municipality-id`,`district-id`) VALUES (%s,%s) """)

        val=(municipalityid,districtid)
        mycursor.execute(sql, val)
        mydb.commit()
        
        return True
    
    def insertStatus(status,isreinfected,typ,deadon,reportedon,recoveredon):
        sql = ("""INSERT INTO status (`status`,`is-reinfected`,`type`,`deadon`,`reportedon`,`recoveredon`) VALUES (%s,%s,%s,%s,%s,%s) """)

        val=(status,isreinfected,typ,deadon,reportedon,recoveredon)
        mycursor.execute(sql, val)
        mydb.commit()
        
        return mycursor.lastrowid
    
    def searchLocation(municipality):
        sql = ("SELECT locationid FROM location WHERE `municipality-id` = %s")

        val=(municipality,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()

        mydb.commit()
        
        return myresult[0][0]
    
    def insertIndividual(id2,value,gender,age,occupation,createddate,modifieddate,locationid,statusid,coordinateid):

        sql = ("""INSERT INTO individual (`id2`,`value`,`gender`,`age`,`occupation`,`created-date`,`modified-date`,`location-id`,`status-id`,`coordinate-id`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """)

        val=(id2,value,gender,age,occupation,createddate,modifieddate,locationid,statusid,coordinateid)
        mycursor.execute(sql, val)
        mydb.commit()
        
        return True

    def readIndividualid():
        sql = ("SELECT id2 FROM individual")

        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        mydb.commit()
        
        return myresult

    def readIndividual():
        sql = ("SELECT individual.gender,individual.age,individual.occupation,individual.`created-date`,individual.`modified-date`, status.`status`,status.`is-reinfected`,status.type,status.reportedon,status.recoveredon,location.`district-id`,location.`municipality-id`,coordinate.x,coordinate.y \
                FROM individual \
                INNER JOIN status ON individual.`status-id` = status.statusid \
                INNER JOIN location ON individual.`location-id` = location.locationid \
                INNER JOIN coordinate ON individual.`coordinate-id` = coordinate.coordinateid;")

        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        mydb.commit()
        return (json.dumps(myresult))
    def readIndividualnon():
        sql = ("SELECT individual.gender,individual.age,individual.occupation,individual.`created-date`,individual.`modified-date`, status.`status`,status.`is-reinfected`,status.type,status.reportedon,status.recoveredon,location.`district-id`,location.`municipality-id`,coordinate.x,coordinate.y \
                FROM individual \
                INNER JOIN status ON individual.`status-id` = status.statusid \
                INNER JOIN location ON individual.`location-id` = location.locationid \
                INNER JOIN coordinate ON individual.`coordinate-id` = coordinate.coordinateid;")

        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        mydb.commit()
        return (myresult)
    def readDistrict():
        sql = ("SELECT district.districtid,district.name,district.code,district.province,coordinate.x,coordinate.y, mapCoordinate.bbox1,mapCoordinate.bbox2,mapCoordinate.bbox3,mapCoordinate.bbox4\
                FROM district \
                INNER JOIN coordinate ON district.`centroid-coordinate` = coordinate.coordinateid \
                INNER JOIN mapCoordinate ON district.bbox = mapCoordinate.mapid ")

        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        mydb.commit()
        return (json.dumps(myresult))
    def readDistrictnon():
        sql = ("SELECT district.districtid,district.name,district.code,district.province,coordinate.x,coordinate.y, mapCoordinate.bbox1,mapCoordinate.bbox2,mapCoordinate.bbox3,mapCoordinate.bbox4\
                FROM district \
                INNER JOIN coordinate ON district.`centroid-coordinate` = coordinate.coordinateid \
                INNER JOIN mapCoordinate ON district.bbox = mapCoordinate.mapid ")

        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        mydb.commit()
        return (myresult)
    
    def readMun():
        sql = ("SELECT municipality.municipalityid,municipality.name,municipality.code,municipality.type,coordinate.x,coordinate.y, mapCoordinate.bbox1,mapCoordinate.bbox2,mapCoordinate.bbox3,mapCoordinate.bbox4\
                FROM municipality \
                INNER JOIN coordinate ON municipality.`centroid-coordinate` = coordinate.coordinateid \
                INNER JOIN mapCoordinate ON municipality.bbox = mapCoordinate.mapid ")

        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        mydb.commit()
        return (json.dumps(myresult))
    
    # def insertuser(username,email,password):

    #     sql = ("""INSERT INTO user (username,password,email) VALUES (%s,%s,%s) """)

    #     val=(username,password,email)
    #     mycursor.execute(sql, val)
    #     mydb.commit()
        
    #     return True
    # def checkemail(username,email):

    #     sql = ("""SELECT username,email FROM user WHERE username=%s or email=%s """)

    #     val=(username,email)
    #     mycursor.execute(sql, val)
    #     myresult = mycursor.fetchall()
    #     mydb.commit()
        
    #     return myresult
    # def checklogin(username,password):

    #     sql = ("""SELECT username,password FROM user WHERE username=%s and password=%s """)

    #     val=(username,password)
    #     mycursor.execute(sql, val)
    #     myresult = mycursor.fetchall()
    #     mydb.commit()
        
    #     return myresult

    def deletepro():
        
        sql = ("DELETE FROM province")
        mycursor.execute(sql)
        mydb.commit()
        return True

    def insertprovince(provinceid,provincename,code,infectednum,population):
        sql = ("""INSERT INTO province (`provinceid`,`provincename`,`code`,`infected-num`,`population`) VALUES (%s,%s,%s,%s,%s) """)
    
        val=(provinceid,provincename,code,infectednum,population)
        mycursor.execute(sql, val)
        mydb.commit()
        
        return True
    
    def readProvince():
        sql = ("SELECT * FROM province")

        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        mydb.commit()
        
        return (json.dumps(myresult))

    def readgender():
        sql = ("select count(id) from individual group by gender")
        mycursor.execute(sql)
        r = mycursor.fetchall()
        mydb.commit()
        return (json.dumps(r))

    def readoccupation():
        sql = ("select count(id) from individual group by occupation")
        mycursor.execute(sql)
        r = mycursor.fetchall()
        mydb.commit()
        return (json.dumps(r))

    def readage():
        sql = ("select age,count(age) from individual group by age")
        mycursor.execute(sql)
        r = mycursor.fetchall()
        mydb.commit()
        return (json.dumps(r))
