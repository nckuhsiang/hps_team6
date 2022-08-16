import json
import socket
import requests
import nums_from_string

def get_token():
    url = "https://oauth.fatsecret.com/connect/token"
    client_ID = "ac2f660ad05f41a3b9f18b927e74c71f"
    client_secret = "67eddc79e83c4ea78c9d97d7189fffea"
    options = {
        
        "headers": { 'content-type': 'application/x-www-form-urlencoded'},
        "grant_type": "client_credentials",
        "scope":"basic",
        "json": True
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
    }
    auth = (client_ID,client_secret)
    response = requests.post(url, data=options,headers=headers,auth=auth).json()
    return response["access_token"]
        
def request_foods(name,num):
    url = "https://platform.fatsecret.com/rest/server.api"
    token = get_token()
    options = {
        "method":"foods.search",
        "format":"json",
        "search_expression":name,
        "max_results": num
    }
    headers = {
        "Authorization":"Bearer "+ token
    }
    response = requests.post(url,data=options, headers=headers).json()
    result = {"foods":[],"message":"success"}
    foods = []
    try:
        res = response["foods"]
        if "food" in res.keys(): #check for the presence of this food that user search
            if num == 1:
                items = [res["food"]]
            else:
                items = res["food"]
            for item in items:
                description = item["food_description"]
                #remove item that per uint is not g
                tmp = description.split(" - ")
                if(tmp[0][-1] != "g"): continue
                #get food info
                info = nums_from_string.get_nums(description)
                food = [item["food_name"],info[0],info[1],info[2],info[3],info[4],item["food_url"]]
                foods.append(food)
    except:
        result["message"] = response["error"]['message']
    if(not foods): #check food_list still have data after filter
        result["message"] = name + " is not exist"
    result["foods"] = foods
    return result

PORT = 8001
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', PORT))
server.listen(5)

while True:
    conn, addr = server.accept()
    print('connect ip:',addr)
    data = conn.recv(1024)
    data = json.loads(data)
    res = request_foods(data['name'],data["num"])
    data = json.dumps(res)
    conn.send(str(len(data)).encode())
    conn.sendall(data.encode())

