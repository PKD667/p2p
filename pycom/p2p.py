import socket,threading,hashlib,binascii
from time import sleep,ctime

## 5468f789d3bbcdf709823f5ab83f0f1165f8c086cf92d34c54da372593c9eabb%7f000001%10011100001111

connexions = {}
queue = []
co_id = []

def log (logs,mode = 'l') :
    if mode == 'l' :
       with open("./logs/log.log",'a',encoding='Utf8') as logfile:
           logfile.write(ctime() + ":::" + logs)
    elif mode == 'd' :
        with open("./logs/debug.log",'a',encoding='Utf8') as logfile:
            logfile.write(ctime() + ":::" + logs)

def assign(data, mode = 1):
  data = data.encode('Utf8')
  data = bytearray(data)
  data.insert(0,mode)
  return data
          
class InThread(threading.Thread):
    def __init__(self,name) :
        threading.Thread.__init__(self)
        self.name = name
        
    def run(self):  
      global queue
      global connexions
      sleep(4)
      while 1 :
        things = input("> ")
        if things.split(":")[0] == "co":
              HEX = things.split(":")[1]
              port = int(HEX.split("%")[2],2)
              ip = socket.inet_ntoa(binascii.unhexlify(HEX.split("%")[1]))
              HEX = assign(HEX.split("%")[0] + '$' + self.name,128)
              s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
              s.connect((ip, port))
              log("socket connected to "+ip+":"+str(port))
              s.send(HEX)
              auth = s.recv(1024)
              if auth[0] == 64 :
                  clientname = auth[1:].decode('Utf8')
              else :
                  log("client is weird , louche.....")
              ServerThread = peer(s,clientname)
              ServerThread.setName(clientname)
              connexions[ServerThread.getName()] = s
              ServerThread.start()
              print("Connected to ",clientname)
        else :
            msg = NAME + "§" + things
            msg = assign(msg)        
            for cle in connexions :
                connexions[cle].send(msg)
           
        
class peer(threading.Thread) :
    ###Init socket
    def __init__(self, client,name):
        threading.Thread.__init__(self)
        self.client = client
        self.name = name
        log("[+] Nouveau thread pour %s " % ( name ) + "\n")
    def run(self):
        print("Connexion de %s " % (self.name))
        data = 'data'
        ident = 1
        while data and ident :
          try :
            data = self.client.recv(4096)
            ident = data[0]
            content = data[1:].decode("utf8") 
            sender = content.split('§')[0]
            text = content.split('§')[1]
            if ident == 1 : 
                msg = self.name + "> " + text
                print(msg)
                for cle in connexions :
                   if cle != sender :
                    connexions[cle].send(msg.encode('Utf8'))
            log(self.name + " > " + str(ident) + " : " + str(text) + "\n")
          except Exception as e:
              print("A terrible error go fix it now !!!")
              print("->")
              print(str(e))
        print("connection %s  closed !" % ( self.name))
        log("[-] connection %s  closed !" % (self.name))

if __name__ == '__main__' :
    PASSWORD = input("password :")
    NAME = input("name :")
    IP = ''
    PORT = int(input("port : "))
    key = hashlib.sha256(PASSWORD.encode('Utf8'))
    key = key.hexdigest()
    print("authentification : ",key +'%'+ binascii.hexlify(socket.inet_aton(input("ip :"))).decode("Utf8") +'%'+ str(bin(PORT)))
    InputThread = InThread(NAME)
    InputThread.start()
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((IP,PORT))
    log("--------------- \n: New Session : \n--------------- \n\n")
    while True:
       s.listen(10)
       print("En écoute... on ",IP,":",PORT)
       (clientsocket , (ip, port)) = s.accept()
       print(ip," client louche")
       login = clientsocket.recv(4096)
       print(login)
       print(login[0])
       print(login[1:].decode('Utf8').split('$')[0])
       if login[0] == 128 and login[1:].decode('Utf8').split('$')[0] == key :          
         clientname = login[1:].decode('Utf8').split('$')[1]
         print(clientname," is fully logged in ! Almost done .")
         clientsocket.send(assign(NAME,64))
       else :
           clientsocket.close()
           print("SUS!SUS!SUS!")
       ServerThread = peer(clientsocket,clientname)
       ServerThread.setName(clientname)
       connexions[ServerThread.getName()] = clientsocket
       ServerThread.start()