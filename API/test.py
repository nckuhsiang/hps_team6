import json
from flask import Flask, request
import nums_from_string
import requests
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

def request_foods(request):
    request_json = json.loads(request)
    name = request_json['name']
    num = request_json['num']
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
                food = { 
                    "name":item["food_name"],
                    "per":info[0],
                    "calories":info[1],
                    "fat":info[2],
                    "cabs":info[3],
                    "protein":info[4],
                    "url":item["food_url"]
                }
                result["foods"].append(food)
    except:
        print(response["error"]['message']) 
        result['message'] = "fail"
    if(not result): #check food_list still have data after filter
        print(name + " is not exist") 
        result['message'] = "fail"
    return result

if __name__ == "__main__":
    request = {"name":"apple","num":50}
    test = request_foods(request)
    print(test)
