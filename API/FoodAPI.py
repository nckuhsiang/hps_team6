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
output:
    foods([Food]): the list of the searching result
"""
def food_search(name):
    url = "https://platform.fatsecret.com/rest/server.api"
    token = get_token()
    options = {
        "method":"foods.search",
        "format":"json",
        "search_expression":name,
        "max_results": 50
    }
    headers = {
        "Authorization":"Bearer "+ token
    }
    response = (requests.post(url,data=options, headers=headers).json())["foods"]["food"]
    # print(response)
    food_list = []
    for item in response:
        description = item["food_description"]
        #remove item that per uint is not g
        tmp = description.split(" - ")
        if(tmp[0][-1] != "g"): continue
        #get food info
        info = nums_from_string.get_nums(description)
        food = Food(item["food_name"],info[0],info[1],info[2],info[3],info[4],item["food_url"])
        food_list.append(food)
    return food_list

if __name__ == "__main__":
    name = "apple"
    foods = food_search(name)
    for food in foods:
        print(food.name,food.calories,food.fat,food.carbs,food.protein)