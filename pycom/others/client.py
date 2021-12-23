
import socket,threading,binascii




connexions = {}

def assign(data, mode = 1):
  data = data.encode('Utf8')
  data = bytearray(data)
  data.insert(0,mode)
  return data

class Emission(threading.Thread) :
    def __init__(self,client):
      threading.Thread.__init__(self)
      self.client = client
    def run(self) :
        name = input("login :")
        name = assign(name,2)
        while 1:
          message_emis = input()
          self.client.send(message_emis.encode('Utf8'))

class Reception(threading.Thread) :
    def __init__(self,client):
      threading.Thread.__init__(self)
      self.client = client
    def run(self) :
        while 1:
          data = self.client.recv()
          ident = data[0]
          content = data[1:].decode("utf8") 
          text = content.decode('Utf8')  
          if ident == 1 :
            print(text)
          

if __name__ == "__main__":
  HEX = input("server : ")
  ip = socket.inet_ntoa(binascii.unhexlify(HEX.split("%")[1]))
  hash = socket.inet_ntoa(binascii.unhexlify(HEX.split("%")[1]))
  hash = assign(hash,3)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((ip, 9999))
  s.send(hash)
  PASSWORD = input("key :")
  while True:
    s.listen(10)
    print( "En écoute...")
    (clientsocket , (ip, port)) = s.accept()
    ServerThread = connexions(ip, port, clientsocket,)
    ServerThread.name(ip + ":" + port)
    connexions[ServerThread.getName()] = clientsocket
    ServerThread.start()

  ThreadEmission = Emission(s,hash)
  ThreadReception = Reception(s)
  ThreadEmission.name("ThreadEmission")
  ThreadReception.name("ThreadReception")
  ThreadEmission.start()
  ThreadReception.start()
  




        
        

