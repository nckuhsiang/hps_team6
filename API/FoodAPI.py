import requests
import nums_from_string

"""
input:
    None
output:
    token(string):token that use to access api
"""
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

class Food:
    def __init__(self,name,per,calories,fat,carbs,protein,url):
        self.name = name
        self.per = per #unit:g
        self.calories = calories #unit:kcal
        self.fat = fat #unit:g
        self.carbs = carbs #unit:g
        self.protein = protein #unit:g
        self.url = url
        
"""
input:
    name(String): the name of the food that user want to search
    num(int): the maximum number of searching result, 1 <= num <= 50
output:
    foods([Food]): 
        return the list of the searching result
        if food is not exist return empty list
        else if error ouccur return None
"""
def get_foods(name,num):
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
    res = (requests.post(url,data=options, headers=headers).json())["foods"]
    food_list = []
    try:
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
                food = Food(item["food_name"],info[0],info[1],info[2],info[3],info[4],item["food_url"])
                food_list.append(food)
        else:
            print(name + "is not exist")
    except:
        print(res["error"]['message'])
        return None
    if(not food_list): #check food_list still have data after filter
        print(name + "is not exist")  
    return food_list


if __name__ == "__main__":
    name = "chewing gum"
    foods = get_foods(name,50)
    print(foods)
    for food in foods:
        print(food.name,food.per,food.calories,food.fat,food.carbs,food.protein,food.url)