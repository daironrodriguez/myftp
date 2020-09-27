
from socket import *
import re 
import sys 
serverName = sys.argv[1]
serverName2 = 'inet.cs.fiu.edu'
print(serverName)
serverPort = 21
user= 'USER '
password= 'PASS '
state = 0

while state != 230: 
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort)) 
    request = int(clientSocket.recv(2048).decode('utf-8').split()[0])
    if request == 220:
        print ("Socket successfully connected")
        ##log in 
        request = input('Enter UserName: ')
        clientSocket.send((user + request + '\r\n').encode('utf-8'))
        state = int(clientSocket.recv(2048).decode('utf-8').split()[0]) 
        if state == 331:
            print('User OK')
            request = input('Enter pasword: ')
            clientSocket.send((password + request + '\r\n').encode('utf-8'))
            state = int(clientSocket.recv(2048).decode('utf-8').split()[0])
    
            if state == 530:
                print("Try again, incorect credentials")
                clientSocket.close()
            else :
                print("Login successful")
        else:
            print ("Error connection the socket")

directory =''
request = ''
while request !='QUIT':

    request = input('myftp>'+directory)
    request = request.split()
    ##print(request)
    comand = request[0]

    if request[0] == 'ls':
        request = 'LIST'
    elif request[0] =='cd':
        request = 'CWD '+request[1]
    elif request[0] =='get':
        request = request[1]
    elif request[0] =='put':
        request = request[1]
    elif request[0] =='delete':
        request = request[1]
    elif request[0] =='quit':
        request = 'QUIT'
    else:
        request=request[0]

##pasive mode 
    if comand =='ls' or comand =='get' or comand =='put':
        code = 0
        clientSocket.send(('PASV\r\n').encode('utf-8'))
        while code!= 227:
            ports = clientSocket.recv(2048).decode('utf-8')
            ports = ports.split()
            ##print(ports)
            code = int(ports[0])
            ##print(int(ports[0]))

        if int(ports[0]) == 227:
            ports = ports[4].split('(',2)
            ports = ports[1].split(')',2)
            ports = ports[0].split(',',6)
            newPort = int(ports[4])*256 + int(ports[5])
            ##print(newPort)

            newSocket = socket(AF_INET, SOCK_STREAM)
            newSocket.connect((serverName,newPort)) 
            #print ("Socket successfully connected PASV mode")


    if comand =='delete':
        clientSocket.send(('PWD \r\n').encode('utf-8'))
        comandChanel = clientSocket.recv(2048).decode('utf-8')
        comandChanel = clientSocket.recv(2048).decode('utf-8')
        #print(request)
        comandChanel = comandChanel.split()[1].replace('"', "")
        directoryToDelete ='DELE '+ comandChanel +'/'+ request
        #print(directoryToDelete)
        request = directoryToDelete

    if comand =='get':
        clientSocket.send(('PWD \r\n').encode('utf-8'))
        comandChanel = clientSocket.recv(2048).decode('utf-8')
        #print(request)
        comandChanel = comandChanel.split()[1].replace('"', "")
        directoryToGet ='RETR '+ comandChanel +'/'+ request
        #print(directoryToGet)
        request = directoryToGet

    if comand =='put':
        clientSocket.send(('TYPE A\r\n').encode('utf-8'))
        comandChanel = clientSocket.recv(2048).decode('utf-8')
        #print(comandChanel)
        directoryToPut ='STOR '+ request
        #print(directoryToPut)
        request = directoryToPut




#send comand
    clientSocket.send((request+ '\r\n').encode('utf-8'))
    comandChanel = clientSocket.recv(2048).decode('utf-8')
    #print("Comand Response: "+comandChanel)
    responseCode = int(comandChanel.split()[0])
    #print(comandChanel)
    
#cd
    if comand =='cd':
        if responseCode != 250:
            comandChanel = clientSocket.recv(2048).decode('utf-8')
        clientSocket.send(('PWD \r\n').encode('utf-8'))
        comandChanel = clientSocket.recv(2048).decode('utf-8')
        comandChanel = comandChanel.split()[1].replace('"', "")
        directory = comandChanel +" % "
        print('Directory changed')
        ##print(comandChanel)

#ls get put
    if comand =='ls' or comand =='get' or comand =='put':
        if comand =='get' :
            bytestransferred = comandChanel.split()[8].replace('.', "").replace('(', "")
            comandChanel = clientSocket.recv(2048).decode('utf-8')
            #print(comandChanel)
            dataChanel = newSocket.recv(2048).decode('utf-8')
            print(dataChanel)
            print('Transfered: '+ bytestransferred+ " bytes")

        if comand !='put':
            dataChanel = newSocket.recv(2048).decode('utf-8')
            print(dataChanel)
        newSocket.close()

        if comand =='put' and responseCode == 150:
            #bytestransferred = comandChanel.split()[8].replace('.', "").replace('(', "")
            clientSocket.recv(2048).decode('utf-8')
            #print('Transfered: '+ bytestransferred + " bytes")
        print(comand + ' ran successfully')
        

#delete 
    if comand == 'delete' and responseCode == 250:
        print(comand + ' ran successfully')

##Data
    if comand =='quit':
        comandChanel = clientSocket.recv(2048).decode('utf-8')
        #print(comandChanel)
        clientSocket.close()
        print("Connection closed")





