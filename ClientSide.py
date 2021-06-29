import requests
import json
import datetime
import traceback
import pymssql
import redis
import pika
import threading
import logging
from elasticsearch import Elasticsearch


#import utils1.logging_api as logger # requires utils/loggin_api.py
IpDockers='10.0.0.2'

url = "http://"+IpDockers+":5000/users"
url2 = "http://"+IpDockers+":5000/users/signin"
url3 = "http://"+IpDockers+":5000/flights"
url4 = "http://"+IpDockers+":5000/tickets"
url5 = "http://"+IpDockers+":5000/ticketsS"


def init_logger():
    logging.basicConfig(filename=r'C:\Users\jeremy\Documents\LOGFILE\TEST.log',level='DEBUG')



#    with open(r'C:\Users\jeremy\Documents\LOGFILE\user_conf.json') as json_file:
#        conf = json.load(json_file)
#        print('conf',conf["log_level"])
#        logger.init(f'{conf["log_file_location"]}'+
#                    f'{datetime.datetime.now().year}_'+
#                    f'{datetime.datetime.now().month}_' +
#                    f'{datetime.datetime.now().day}_' +
#                    f'{datetime.datetime.now().hour}_' +
#                    f'{datetime.datetime.now().minute}_' +
#                    f'{datetime.datetime.now().second}' + '.log'
#                    , conf["log_level"])
        #open log file and write



def newClient(new_cust):
    print("new_cust")

    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    print(new_cust)

    resp = requests.post(url2, data=json.dumps(new_cust), headers=headers)# send to the rest server the new user
    print("after request")
    res={}
    res = json.loads(resp.content)# receive from server result
    return res # return result

def showCustomer():
    cust_id = input("What's the cusgtomer id to get?")
    resp = requests.get(f'{url}/{cust_id}')# send to the server to print 1 user with id number
    if resp.status_code != 200:# if server return error
        print('Unexpected error')
        return
    customer1 = json.loads(resp.content)#receive from server the user
    if (customer1 == []):
        print('-- Not found --')#if result is empty,id user not in data base
    else:
        print(customer1)#print user

def showAllCustomers():
    resp = requests.get(url)#send to server to print all users
    if resp.status_code != 200:
        print('Unexpected error')
        return
    customers = json.loads(resp.content)#receive from server all users
    for c in customers:
        print(c)#print all users



def signIn(new_cust):
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    resp = requests.post(url2, data=json.dumps(new_cust), headers=headers)#send to server to chek if there is new_cust id in data base
    if resp.status_code != 200:
        return 2
    customer1 = json.loads(resp.content)

    if (customer1 == []):
        return 3#there is not user with this id number
    else:
        return customer1 #return the user who sign in

def showFlights():
    resp = requests.get(url3)# send to sever to print all flights the client can to buy
    if resp.status_code != 200:
        print('Unexpected error')
        return
    y = datetime.datetime.now()
    #create dictonary for hour and min now

    clockToCheck = {'timeNow': [y.strftime("%H"), y.strftime("%M")]}

    #    minToCheck = (str(datetime.datetime.now()).split()[1].split(':'))[1]

    r = redis.Redis(host=IpDockers,port="6379",password="")
    #connecting to redis docker


    if (r.get('printFlight') == None):#if it the first time and there is not database in redis
        resp = requests.get(url3)
        flight = json.loads(resp.content)
        flight.append(clockToCheck)#append to fdictonary flight the time now
        r.set('printFlight', json.dumps(flight))#set the new redis database
        result = json.loads(r.get('printFlight'))
        for c in result:
            if "timeNow" not in c:#prints all flights from dict redis but not timenow dict
                print('PLEASE PRESS ', c['ID'], 'FOR TICKET IN DATE:', c['DATE'], ' FROM', c['ORIGINE ID'], ' TO ',c['DESTINATION ID'], 'WITH', c['REMAINING SEAT'], 'PLACE REMAINDING')

    elif(abs((int(json.loads(r.get('printFlight'))[-1].get('timeNow')[1])) - (int(clockToCheck.get('timeNow')[1])))) < 9:
        #if time now < 10 mn time from redis database : user receive data from redis
        result = json.loads(r.get('printFlight'))
        print('res=',result)
        for c in result:
            if "timeNow" not in c:
                print('PLEASE PRESS ', c['ID'], 'FOR TICKET IN DATE:', c['DATE'], ' FROM', c['ORIGINE ID'], ' TO ',c['DESTINATION ID'], 'WITH', c['REMAINING SEAT'], 'PLACE REMAINDING')
    else:
        #if time now > 10 mn to time from redis database : redis refresh from sql and client receive from data from redis
        resp = requests.get(url3)  # send to sever to print all flights the client can to buy
        flight = json.loads(resp.content)  # server return all flights
        flight.append(clockToCheck)
        r.set('printFlight', json.dumps(flight))# set new redis database
        result = json.loads(r.get('printFlight'))#get the fresh database to client
        for c in result:
            if "timeNow" not in c:
                print('PLEASE PRESS ', c['ID'], 'FOR TICKET IN DATE:', c['DATE'], ' FROM', c['ORIGINE ID'], ' TO ',c['DESTINATION ID'], 'WITH', c['REMAINING SEAT'], 'PLACE REMAINDING')


def buyTicket(idClient):
    resp = requests.get(url4) #send to server to print flights
    showFlights() #print flights to buy
    resp1 = requests.get(url5) #sinvalid url

 #       return

    print('PLEASE PRESS 0 FOR EXIT')
    idFlight = input("What's flight you want to buy ?") # user need to choice ticket to buy
    if int(idFlight)==0 :
        return 1 #if user choice 0 , back to menu
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    new_Ticket = {}

    new_Ticket['user_id'] = idClient
    new_Ticket['flight_id'] = idFlight

    resp = requests.post(url4, data=json.dumps(new_Ticket), headers=headers) #send to server to add ticket
    #put an invalit url to test rabbitqm]
    if resp1.status_code != 200:
        flight = json.loads(resp.content)  # server return all flights
        res = json.dumps(flight)
        connection = pika.BlockingConnection(pika.ConnectionParameters(IpDockers))
        channel = connection.channel()
        #put the res dictionary 
        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='', routing_key='hello', body=res)
        connection.close()
        print('Unexpected error')
        
    if resp.status_code == 200:
        #extract the dict from the queue
        def start_consumer():
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=IpDockers))
            channel = connection.channel()
            channel.queue_declare(queue='hello')
            def callback(ch, method, properties, body):
                print(" [x] Received ", body)
            channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
            channel.start_consuming()
        consumer_thread = threading.Thread(target=start_consumer)
        consumer_thread.start()

        ticket1 = json.loads(resp.content)
        if ticket1 == []:
            return 2  # if user try to buy ticket not exist

#    ticket1 = json.loads(resp.content)
#   if ticket1==[]:
#        return 2 # if user try to buy ticket not exist
    printFlight(ticket1['flight_id']) #print ticket that client buy

def printFlight(flightId):
    resp = requests.get(f'{url3}/{flightId}') # send to server to print flights
    flight = json.loads(resp.content) #server return flight
    print('YOU BUY', 'TICKET FROM', flight[0]['ORIGINE ID'], ' TO ', flight[0]['DESTINATION ID'], ' DATE:',flight[0]['DATE'])


def printTicket(cust_id):
        resp = requests.get(f'{url4}/{cust_id}') #send to server to print tiket with id user
        if resp.status_code != 200:
            print('Unexpected error')
            return
        ticket = json.loads(resp.content)
        if (ticket == []): #if return empty , client have not tickets
            return ticket
        else:
            for c in ticket:
                #for all ticket send to server which flight user buy and return it
                flightId=c['FLIGHT ID']
                ticketId=c['TICKET ID']
                resp = requests.get(f'{url3}/{flightId}')
                flight = json.loads(resp.content)
                print('YOU BUY TICKET ID:',c['TICKET ID'],'FROM', flight[0]['ORIGINE ID'], ' TO ', flight[0]['DESTINATION ID'],' DATE:', flight[0]['DATE'])


def removeTicket(ticket_id):
    resp = requests.delete(f'{url4}/{ticket_id}') #send to server to delete ticket with id
    if resp.status_code != 200:
        print('Unexpected error')
        return
    ticket = json.loads(resp.content)
    if ticket==[]: #if ticket empy,bad choice
        print("******** you have input an invalid ticket id ********")
    elif ticket[0]['status']=='delete':
        return True #if server return true ,ticket is delete
    else:
        return False



def removeClient(idClient):
    resp = requests.delete(f'{url}/{idClient}')
    return json.loads(resp.content)
    # send to server to remove user with id

def updateCustomer(idClient):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    names_par = ['full_name', 'password', 'real_id']
    updated_cust = {}
    for par in names_par:
        value = input(f'Please insert {par}: ')
        updated_cust[par] = value
    # input the new user to update and create dictionry
    if not updated_cust['real_id'].isdigit() or len(updated_cust['real_id']) != 9:
        print("id is be 9 numbers")
        #check if id with 9 numbers

#    print('updated_cust: ',json.dumps(updated_cust))
    resp = requests.put(f'{url}/{idClient}', data=json.dumps(updated_cust), headers=headers) #send to server to update user
    return json.loads(resp.content) # server back


def guiFlights(idClient):
    while True:
        print('select what you want')
        print('1. Show all flights ')
        print('2. buy flights  ')
        print('3. print tickets you bought')
        print('4. delete ticket')
        print('5. remove user ')
        print('6. Update user')
        print('0. sign out')
        choice = input("What's your choice? ")
        if not choice.isdigit() or int(choice)>6:
            print('******** bad choice !!!!!!!!- try again ********')
        if choice == "0":
            break; # client want to exit to flight gui
        if choice == "1":
            showFlights() # send to showflight func
        if choice == "2":
            res=buyTicket(idClient) #send to buyticket funct with id user
            if res==2:
                print('******** bad Ticket Id choice !!!!!!!!- try again ********')

        if choice == "3":
            res=printTicket(idClient) #send to printticket function with id user
            if res ==[]: #if res is empty , user not buy ticket
                print(' ')
                print('******** you have not buy any ticket ********')
                continue
        if choice == "4":
            res=printTicket(idClient) # print to the user all tickets and he is need to choice whitch to remove
            if res ==[]:
                print(' ')
                print('******** you have not ticket to remove ********')
                continue

            choiceTicketDelte=input("choice Ticket Id to remove: ")
            res=removeTicket(choiceTicketDelte) #send the removeticket function the ticket user want to remove
            if res==True:
                print('******** the ticket is delete ********')
        if choice == "5":
            res=removeClient(idClient) # send to remove client functiom
            print('delete is ',res['status'])
            break
        if choice == "6":
            res=updateCustomer(idClient) #send to updateCustomer function
            print('update is ',res['status'])
            break


def main():
    init_logger()
#    logger.write_lo_log('**************** System started ...', 'INFO')
    logging.debug('**************** System started ...')
    x = '{ "debug":"**************** System started ..."}'
    #put log in dictionary
    res = json.loads(x)
    #send log to elastic
    es = Elasticsearch([{'host': IpDockers, 'port': 9200}], http_auth=('elastic', 'changeme'))
    # use elastic/changeme according to db
    es.indices.create(index='startingsystem', ignore=400)

    es.index(index='startingsystem', id=1, body=res)
    startingSystem_id_1 = es.get(index="startingsystem", id=1)


    while True:
        print('1. Suscribe')#
        print('2. Sign in')
        print('0. Exit')
#        print('3. Show all customers')
#        print('4. Show customer by id')
        choice = input("What's your choice? ")
        if not choice.isdigit() or int(choice)>2:# check if user enter a true value
            print('bad choice !!!!!!!!- try again')
            continue
        if choice == "0":
            break;#user quit
        if choice == "3":
            showAllCustomers()# function that prints all user (only for administrator)
        if choice == "4":
            showCustomer()# function print only 1 user (only for administator)
        if choice == "1":

            names_par = ['full_name', 'password', 'real_id']
            new_cust = {}
            cust = {}

            for par in names_par:
                value = input(f'Please insert {par}: ')
                new_cust[par] = value
                # input from user name ,password and real id and create a dictionary
            if not new_cust['real_id'].isdigit() or len(new_cust['real_id']) != 9: #check the real id is only 9 numbers. if not it is back to the menu
                print("id is be 9 numbers")
            else:
                res=newClient(new_cust)# sendind to newclient function and receive to res
                print("new client is add")



        if choice == "2":
            names_par = ['password', 'real_id']
            new_cust = {}

            for par in names_par:
                value = input(f'Please insert {par}: ')
                new_cust[par] = value
            #input from user password and id for signin

            if not new_cust['real_id'].isdigit() or len(new_cust['real_id']) != 9:# verif if 9 number
                print("id is be 9 numbers")
                continue
            else:
                res=signIn(new_cust)# send to signin function the dictionary and receive the result

            if res==3 :
                print("User not Found")# if signin fun rterurn 3: user enter id that not in database
            elif res==2 :
                print("Unexpected error")# if signin fun rterurn 2: there is an error
            else:
                print('*************************')
                print(f'** Welcome ',res["full_name"],' **')
                print('*************************')
                guiFlights(res["ID"])
                #print the use name and send to guiflight the id user


with open(r'C:\Users\jeremy\Documents\LOGFILE/user_conf.json') as json_file:
    conf = json.load(json_file)
    #open the configuration file
main()
