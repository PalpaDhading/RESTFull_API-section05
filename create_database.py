import sqlite3

connection = sqlite3.connect('Digitallog.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,\
                username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS itemsdata (itemName text,dateandtime text,\
                itemLocation  text, itemCondition text,symptomDetails text,\
                resolutionDetails text,currentstatus text,DateofResolution text,\
                currentRSSI float,currentVSWR float,currentSQIDVoltage float,\
                otherOpportunityDetails text)"

create_table = "CREATE TABLE IF NOT EXISTS sitesdata(siteName text,street text,\
                city  text, state text)"

cursor.execute(create_table)

connection.commit()
connection.close()
