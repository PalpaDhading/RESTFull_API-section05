import sqlite3
import datetime
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Site(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('street',
            type =str,
            required = True,
            help ="This field can't be left blank "
        )
    parser.add_argument('city',
            type =str,
            required = True,
            help ="This field can't be left blank "
        )
    parser.add_argument('state',
            type =str,
            required = True,
            help ="This field can't be left blank "
        )

    def get(self, siteName):
        site = Site.find_by_name(siteName)
        if site:
            return site.json()
        return {'message': "Site {} not found".format(sitename)}, 404

    def post(self, sitename):
        data = Site.parser.parse_args()
        if Site.find_by_name(sitename):
            return {'message': "A cell site with name '{}' already exists.".format(sitename)}, 400

        site = SiteModel(sitename,data['street'],data['city'],data['state'])

        try:
            site.save_to_db()
        except:
            return {"message": "An error occurred creating the {} site.".format(sitename)}, 500

        return site.json(), 201

    def put(self, sitename):
        data = Site.parser.parse_args()

        site = Site.find_by_name(sitename)

        if site:
            site.street = data['street']
            site.city = data['city']
            site.state = data['state']

        else:
            site = SiteModel(sitename,data['street'],data['city'],data['state'])

        site.save_to_db()

        return site.json()

    @classmethod
    def delete(self, sitename):
        site = Site.find_by_name(sitename)
        if site:
            site.delete_from_db()

        return {'message': "Site {} deleted".format(sitename)}

    @classmethod
    def find_by_name(cls,siteName):
        connection = sqlite3.connect('Digitallog.db')
        cursor = connection.cursor()

        query = "SELECT * FROM sitesdata WHERE siteName = ? "
        result = cursor.execute(query, (siteName,))
        row = result.fetchone()
        connection.close ()
        if row:
            return {'Sites':{'siteName': row[0],\
                    'street':row[1],'city':row[2],'state ':row[3]}
                    }

    @classmethod
    def insert(cls,siteDetails):
        connection = sqlite3.connect('Digitallog.db')
        cursor = connection.cursor()
        query = "INSERT INTO sitesdata VALUES(?,?,?,?)"
        cursor.execute(query, (siteDetails['siteName'],\
                             siteDetails['street'],siteDetails['city'],siteDetails['state']
                             ))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls,siteDetails):
        connection = sqlite3.connect('Digitallog.db')
        cursor = connection.cursor()
        query = "UPDATE sitesdata SET street=?,city=?,state=?
        WHERE siteName=?"
        cursor.execute(query, (siteDetails['street'],siteDetails['city'],siteDetails['state'],\
                             siteItem['siteName']
                             ))

        connection.commit()
        connection.close ()

    @classmethod
    def delete(self,siteName):
        connection = sqlite3.connect('Digitallog.db')
        cursor = connection.cursor()
        query = "DELETE FROM sitesdata WHERE siteName=?"
        cursor.execute(query,(siteName,))

        connection.commit()
        connection.close ()
        return {'message':" Site name -'{}'deleted".format(siteName)}


class SiteList(Resource):
    def get(self):
        return {'SiteList': list(map(lambda x: x.json(), SiteModel.query.all()))}
