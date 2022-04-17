"""
"""
import requests
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, connectWS
import json

TOKEN="mn4MKWtgPV5aUnzjxTLR43rACfqnITUo"
SESSIONSCHEMA="https"
SOCKETSCHEMA="wss"
APIURL="://tracker-gateway.hostcert.com.br"
RESTPATH="/api"
SOCKETPATH="/socket"
BASEURL = "{apiUrl}{restPath}".format(
            apiUrl=APIURL, restPath=RESTPATH)






REST_TOKEN="fdb50212d06aed3fe6a537a2d7cf739cff19d63f"


user_login = requests.post("http://localhost:8001/api-token-auth/",headers={
                    "contentType": "application/json; charset=utf-8",
                    "accept": "application/json; charset=utf-8",
                },json={
                    "username":"token_manager",
                    "password":"L7y3jLnfVWhcMwJ"
                })

if user_login.status_code == 200:
    REST_TOKEN=user_login.json().get('token',"fdb50212d06aed3fe6a537a2d7cf739cff19d63f")


class EchoClientProtocol(WebSocketClientProtocol):
    def onMessage(self, payload, isBinary):

        raw_data = json.loads(payload.decode('utf8'))
        if raw_data:
            try:
                create = requests.post("http://localhost:8001/rest-api/v1/equipamentos/updates/",headers={
                    "contentType": "application/json; charset=utf-8",
                    "accept": "application/json; charset=utf-8",
                    "Authorization":f"Bearer {REST_TOKEN}"
                },json={
                    "raw_data": raw_data
                })
                print(create.status_code)
            except Exception as e:
                print(e.__repr__())
                print("lost connection")
        
        else:
            print("sem data")
        
           

session = requests.Session()
sessionUrl = "{schema}{baseUrl}/session?token={userToken}".format(
        userToken=TOKEN, schema=SESSIONSCHEMA, baseUrl=BASEURL
    )
socketUrl =  "{schema}{baseUrl}{socketPath}".format(
        socketPath=SOCKETPATH,schema=SOCKETSCHEMA, baseUrl=BASEURL
    )
session.get(sessionUrl)
cookies = session.cookies.get_dict()
he={}
kie="; ".join(["%s=%s" %(i, j) for i, j in cookies.items()])

headers = {'Cookie': "; ".join(["%s=%s" %(i, j) for i, j in cookies.items()])}
factory = WebSocketClientFactory(socketUrl, headers=headers)
factory.protocol = EchoClientProtocol
connectWS(factory)
reactor.run()



