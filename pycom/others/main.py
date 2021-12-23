import socket,threading,os,hashlib

### Globals
clients = {}


def log (logs,mode = 'l') :
    if mode == 'l' :
       with open("./logs/log.log",'a',encoding='Utf8') as logfile:
           logfile.write(logs)
    elif mode == 'd' :
        with open("./logs/debug.log",'a',encoding='Utf8') as logfile:
            logfile.write(logs)

        
class client(threading.Thread) :
    ###Init socket
    def __init__(self, ip, port, client,password):
        threading.Thread.__init__(self)
        self.auth = 0
        self.ip = ip
        self.port = port
        self.client = client
        self.name = ip
        self.key = hashlib.sha256(password.encode('Utf8'))
        if self.client.recv(4096) == self.key :
            self.auth = 1
        log(" • "+str(os.popen('date').read()))
        log("[+] Nouveau thread pour %s %s" % (self.ip, self.port ) + "\n")
    def run(self):
        print("Connexion de %s %s" % (self.ip, self.port, ))
        data = 'data'
        ident = 1
        while data and ident and self.auth:
          try :
            data = self.client.recv(4096)
            ident = data[0]
            content = data[1:].decode("utf8") 
            text = content.decode('Utf8')  
            if ident == 1 : 
                msg = self.name + "> " + text
                for cle in clients :
                    clients[cle].send(msg.encode('Utf8'))
            elif ident == 2 :
                self.name = text
            log(self.name + " > " + str(ident) + " : " + str(text) + "\n")
          except Exception as e:
              print("A terrible error go fix it now !!!")
              print("->")
              print(str(e))
        print("connection %s %s closed !" % (self.ip, self.port ))
        log("[-] connection %s %s closed !" % (self.ip, self.port ))

        

if __name__ == '__main__' :
  ### Initialisation
   PASSWORD = "200489"
   s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   s.bind(('',9999))
   log("--------------- \n: New Session : \n--------------- \n\n")
   while True:
     s.listen(10)
     print( "En écoute...")
     (clientsocket , (ip, port)) = s.accept()
     ServerThread = client(ip, port, clientsocket,PASSWORD)
     ServerThread.name(ip + ":" + port)
     clients[ServerThread.getName()] = clientsocket
     ServerThread.start()
