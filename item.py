import sqlite3
import datetime
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('dateandtime',
        type=str,
        required=False,
        help="This field cannot be left blank!"
    )
    parser.add_argument('itemLocation',
        type =str,
        required = False,
        help ="This field can't be left blank "
        )
    parser.add_argument('itemCondition',
        type =str,
        required = False,
        help ="This field can't be left blank "
        )

    parser.add_argument('symptomDetails',
        type =str,
        required = False,
        help ="symptomType -This field can't be left blank "
        )
    parser.add_argument('resolutionDetails',
        type =str,
        required = False,
        help ="resolutionDetails -This field can't be left blank "
        )
    parser.add_argument('currentstatus',
        type =str,
        required = False,
        help ="currentstatus- This field can't be left blank "
        )
    parser.add_argument('DateofResolution',
        type =str,
        required = False,
        help ="Date of resolution - This field can't be left blank "
        )
    parser.add_argument('currentRSSI',
        type =float,
        required = False,
        help ="RSSI - This field needs decimal or integer value and can't be left blank "
        )
    parser.add_argument('currentVSWR',
        type =float,
        required = False,
        help ="VSWR - This field needs decimal or integer value and can't be left blank "
        )
    parser.add_argument('currentSQIDVoltage',
        type =float,
        required = False,
        help ="Voltage- This field needs decimal or integer value and can't be left blank "
        )
    parser.add_argument('otherOpportunityDetails',
        type =str,
        required = False,
        help ="Opportunity - This field can't be left blank "
        )
    parser.add_argument('siteName',
        type=str,
        required= True,
        help="Every item needs a sitename."
    )

    @jwt_required()
    def get(self, itemName):
        siteItem = Item.find_by_name(itemName)
        if siteItem:
            return siteItem
        else :
            return {'message':'item of  the site not found'},404

    def post(self,itemName):
        if self.find_by_name(itemName):
            return {'message':"A site with this name '{}' already exists .".format(itemName)},400

        data = Item.parser.parse_args()
        #data = request.get_json()
        siteItem = {
                data['dateandtime'],itemName,data['itemLocation'],data['itemCondition'],data['symptomDetails'],data['resolutionDetails'],data['currentstatus'],data['DateofResolution'],\
                data['currentRSSI'],data['currentVSWR'],data['currentSQIDVoltage'],data['otherOpportunityDetails'],data['siteName']
    	     }
        try:
            self.insert(siteItem)
        except:
            return{"message":"An error occurred while inserting the site item!"},500 #internal server error
        return siteItem,201

    def put(self,itemName):
        data = Item.parser.parse_args()

        siteItem = Item.find_by_name(itemName)

        updated_siteItem = {'itemName':itemName,
                	'dateandtime':data['dateandtime'],'itemLocation':data['itemLocation'],'symptomDetails':data['symptomDetails'],\
                    'resolutionDetails':data['resolutionDetails'],'currentstatus':data['currentstatus'],'DateofResolution':data['DateofResolution'],\
                    'currentRSSI':data['currentRSSI'],'currentVSWR':data['currentVSWR'],'currentSQIDVoltage':data['currentSQIDVoltage'],\
                    'otherOpportunityDetails':data['otherOpportunityDetails']
            	     }

        if siteItem is None:
            try:
                self.insert(updated_siteItem)
            except:
                return {"message":"An error occured while inserting."},500
        else:
            try:
                self.update(updated_siteItem)
            except:
                return {"message":"An error occured while updating."},500

        return updated_siteItem

    @classmethod
    def find_by_name(cls,itemName):
        connection = sqlite3.connect('Digitallog.db')
        cursor = connection.cursor()
        query = "SELECT * FROM itemsdata WHERE itemName = ? "
        result = cursor.execute(query, (itemName,))
        row = result.fetchone()
        connection.close ()
        if row:
            return {'SiteItems':{'itemName': row[0],\
                    'dateandtime':row[1],'itemLocation':row[2],'itemCondition':row[3],'symptomDetails':row[4],\
                    'resolutionDetails':row[5],'currentstatus':row[6],'DateofResolution':row[7],\
                    'currentRSSI':row[8],'currentVSWR':row[9],'currentSQIDVoltage':row[10],\
                    'otherOpportunityDetails':row[11]
                    }}

    @classmethod
    def update(cls,siteItem):
        connection = sqlite3.connect('Digitallog.db')
        cursor = connection.cursor()
        query = "UPDATE itemsdata SET dateandtime=?,itemLocation=?,itemCondition=?,symptomDetails=?,\
        resolutionDetails =?, currentstatus=?,DateofResolution=?,\
        currentRSSI= ?, urrentVSWR=?, currentSQIDVoltage=?,\
        otherOpportunityDetails=?  WHERE itemName=?"
        cursor.execute(query, (siteItem['dateandtime'],siteItem['itemLocation'],siteItem['itemCondition'], siteItem['symptomDetails'],\
                             siteItem['resolutionDetails'],siteItem['currentstatus'],siteItem['DateofResolution'],\
                             siteItem['currentRSSI'],siteItem['currentVSWR'],siteItem['currentSQIDVoltage'],\
                             siteItem['otherOpportunityDetails'],\
                             siteItem['itemName']
                             ))

        connection.commit()
        connection.close ()

    @classmethod
    def delete(self,itemName):
        connection = sqlite3.connect('Digitallog.db')
        cursor = connection.cursor()
        query = "DELETE FROM itemsdata WHERE itemName=?"
        cursor.execute(query,(itemName,))

        connection.commit()
        connection.close ()
        return {'message':" Site item -'{}'deleted".format(itemName)}

    @classmethod
    def insert(cls,siteItem):
        connection = sqlite3.connect('itemData.db')
        cursor = connection.cursor()
        query = "INSERT INTO itemsdata VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(query, (siteItem['itemName'],\
                             siteItem['dateandtime'],siteItem['itemLocation'],siteItem['itemCondition'],siteItem['symptomDetails'],\
                             siteItem['resolutionDetails'],siteItem['currentstatus'],siteItem['DateofResolution'],\
                             siteItem['currentRSSI'],siteItem['currentVSWR'],siteItem['currentSQIDVoltage'],\
                             siteItem['otherOpportunityDetails']
                             ))
        connection.commit()
        connection.close()

class SiteItemList(Resource):
    def get(self):
        connection = sqlite3.connect('Digitallog.db')
        cursor = connection.cursor()
        query = "SELECT * FROM itemsdata"
        result = cursor.execute(query)
        itemList = []
        for row in result:
            itemList.append({'itemName': row[0],\
                    'dateandtime':row[1],'itemLocation':row[2],'itemCondition':row[3],'symptomDetails':row[4],\
                    'resolutionDetails':row[5],'currentstatus':row[6],'DateofResolution':row[7],\
                    'currentRSSI':row[8],'currentVSWR':row[9],'currentSQIDVoltage':row[10],\
                    'otherOpportunityDetails':row[11]
                    })

        connection.close ()
        return {'SiteItemList':itemList}
