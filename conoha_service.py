import requests
import json
import logging
import base64

host = "https://mail-hosting.tyo1.conoha.io/v1/emails"
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-Auth-Token': 'xxxxxx',
}


class ConohaAPI:

    def __init__(self):
        pass

    def generateMailAdress(self, email, passwd):
        data = {"domain_id": "xxxxxx",
            "email": email,
            "password": passwd
            }
        req = requests.post(host, headers=headers, data=data)
        if req.status_code == 200:
            res = json.loads(req.text)
            return res["email"]["email_id"]
        elif req.status_code == 409:
            print("Duplicate! plz try again with different email.")
        else:
            print("error")

    def getLastMailingMessage(self, email_id):
        getlist_host = host + "/" + email_id + "/messages"
        req = requests.get(getlist_host, headers=headers)
        if req.status_code == 200:
            res = json.loads(req.text)
            if not res["total_count"] == 0:
                msgid = str(res["messages"][0]["message_id"])
                getmsg_host = getlist_host + "/" + msgid
                req2 = requests.get(getmsg_host, headers=headers)
                res2 = json.loads(req2.text)
                msg = str(res2["message"]["message"])
                msg_decode = base64.b64decode(msg).decode('utf-8')
                return msg_decode
            else:
                print("message is none")
        elif req.status_code == 404:
            print("not found.")
        else:
            print("error")

    def deleteMailAdress(self, email_id):
        del_host = host + "/" + email_id
        req = requests.delete(del_host, headers=headers)
        if req.status_code == 204:
            print("delete success!")
        elif req.status_code == 404:
            print("not found")
        else:
            print("error")
