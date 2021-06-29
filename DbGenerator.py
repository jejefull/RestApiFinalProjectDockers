import requests
import os
import utils1.logging_api as logger # requires utils/loggin_api.py
import datetime
import pymssql
import json
import random
import traceback

dataBaseAddress='10.0.0.2' # ip sql docker data base
dataBasePassword='yourStrong(!)Password' #password sql docker data base

def UpdateUsers():
    i=0
    while True:
        url = "https://randomuser.me/api/"
        resp = requests.get(url)  # send to server to print all users
        customers = json.loads(resp.content)  # receive from server all users
        print(customers)
        fullName=customers['results'][0]['name']['first']+'_'+customers['results'][0]['name']['last']
        print(fullName)
        #create raidom name form url 
        id=random.randint(100000000, 999999999)
        #create raidom id 
        print(id)
        #create raidom password 
        password=random.randint(100000, 999999)
        print(password)
        try:
            with pymssql._mssql.connect(server=dataBaseAddress, user='sa', password=dataBasePassword, database='FLIGHTS') as conn:
                query = 'INSERT INTO dbo.USERS (full_name, password, real_id) ' + f"VALUES ('{fullName}', '{password}','{id}');"
                conn.execute_query(query)
            print('query: ', query)

        except Exception as e:
            tr = traceback.format_exc()
            logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
            return json.dumps({'Error': 'err'})
        if i==10:
            #create 10 users
            break
        i=i+1


def UpdateFlights():
    try:

        with pymssql._mssql.connect(server=dataBaseAddress, user='sa', password=dataBasePassword, database='FLIGHTS') as conn:
            query = 'INSERT INTO dbo.FLIGHTS (timestamp, remaining_seats, origin_country_id , dest_country_id) ' + f"VALUES ('{'2021-05-20 23:17'}','{'10'}','{'1'}','{'3'}');"
            conn.execute_query(query)
            query = 'INSERT INTO dbo.FLIGHTS (timestamp, remaining_seats, origin_country_id , dest_country_id) ' + f"VALUES ('{'2021-05-20 23:17'}','{'10'}','{'3'}','{'1'}');"
            conn.execute_query(query)
            query = 'INSERT INTO dbo.FLIGHTS (timestamp, remaining_seats, origin_country_id , dest_country_id) ' + f"VALUES ('{'2021-05-20 23:17'}','{'10'}','{'1'}','{'2'}');"
            conn.execute_query(query)
            #update 3 flights

    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error': 'err'})

def Updateticket():
    try:

        with pymssql._mssql.connect(server=dataBaseAddress,user='sa', password=dataBasePassword, database='FLIGHTS') as conn:
            query = 'INSERT INTO TICKETS (user_id, flight_id) ' + f"VALUES ('{'1'}','{'1'}');"
            print('query: ', query)
            conn.execute_query(query)
            #update ticket

    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error': 'err'})

def Updatecountries():
    try:
        with pymssql._mssql.connect(server=dataBaseAddress,user='sa', password=dataBasePassword, database='FLIGHTS') as conn:
            query = 'INSERT INTO COUNTRIES (name) ' + f"VALUES ('{'ISRAEL'}');"
            conn.execute_query(query)
            query = 'INSERT INTO COUNTRIES (name) ' + f"VALUES ('{'USA'}');"
            conn.execute_query(query)
            query = 'INSERT INTO COUNTRIES (name) ' + f"VALUES ('{'FRANCE'}');"
            conn.execute_query(query)
            #update 3 countries
    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error': 'err'})


def CreateDbTables():
    try:
        #create data base name and tables

        with pymssql._mssql.connect(server=dataBaseAddress,user='sa', password=dataBasePassword) as conn:
            query = 'CREATE DATABASE "FLIGHTS"'
            conn.execute_query(query)
        with pymssql._mssql.connect(server=dataBaseAddress,user='sa', password=dataBasePassword, database='FLIGHTS') as conn:
            query='CREATE TABLE [dbo].[TICKETS]([ticket_id] [int] IDENTITY(1,1) NOT NULL,[user_id] [int] NULL,[flight_id] [int] NULL,CONSTRAINT [PK_TICKETS] PRIMARY KEY CLUSTERED ([ticket_id] ASC))'
            conn.execute_query(query)
        with pymssql._mssql.connect(server=dataBaseAddress,user='sa', password=dataBasePassword, database='FLIGHTS') as conn:
            query='CREATE TABLE [dbo].[FLIGHTS]([flight_id] [int] IDENTITY(1,1) NOT NULL,[timestamp] [datetime] NULL,[remaining_seats] [int] NULL,[origin_country_id] [int] NULL,[dest_country_id] [int] NULL,CONSTRAINT [PK_FLIGHTS] PRIMARY KEY CLUSTERED([flight_id] ASC))'
            conn.execute_query(query)
        with pymssql._mssql.connect(server=dataBaseAddress,user='sa', password=dataBasePassword, database='FLIGHTS') as conn:
            query='CREATE TABLE [dbo].[USERS]([id_Al] [int] IDENTITY(1,1) NOT NULL,[full_name] [varchar](50) NULL,[password] [varchar](50) NULL,[real_id] [varchar](50) NULL,CONSTRAINT [PK_USERS] PRIMARY KEY CLUSTERED([id_Al] ASC))'
            conn.execute_query(query)
        with pymssql._mssql.connect(server=dataBaseAddress,user='sa', password=dataBasePassword, database='FLIGHTS') as conn:
            query='CREATE TABLE [dbo].[COUNTRIES]([code_al] [int] IDENTITY(1,1) NOT NULL,[name] [varchar](50) NULL,CONSTRAINT [PK_COUNTRIES] PRIMARY KEY CLUSTERED ([code_al] ASC))'
            conn.execute_query(query)
            print('query:',query)


    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error': 'err'})

def main():
    # docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=yourStrong(!)Password' -e 'MSSQL_PID=Express' -p 1433:1433 -d mcr.microsoft.com/mssql/server:2017-latest-ubuntu
    CreateDbTables()
    UpdateUsers()
    UpdateFlights()
    Updateticket()
    Updatecountries()


main()

