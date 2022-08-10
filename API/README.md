Food API:
    get_token()
        get token that use to access get_foods API
        input:
            None
        output:
            token(string):token that use to access api

    get_foods(name,num)
        input:
            name(String): the name of the food that user want to search
            num(int): the maximum number of searching result, 1 <= num <= 50
        output:
            foods([Food]): 
                return the list of the searching result
                if food exist return empty list
                else if error ouccur return None

    get_daily_diet(account)
        input:
            account(string): user account
        ouput:
            data(tuple):(calories,fat,carbs,protein) 當日營養量, if account doesn't exist return None
    save_diet(food,account)
        input:
            food(tuple):(name,calories,fat,carbs,protein) user食用之食物名稱及其總營養量
            account(string): user account
        output:
            result(bool): success or fail


User API:

    checkAccount(account)
        check if account exist or not
        input:
            account(string)
        output:
            result(bool): true,account can be created. otherwise false

    createUser(account,height,weight,workload,BMI,TDEE)
        create a user
        input:
            user(tuple):(account,height,weight,workload,gender,calories,fat,carbs,protein)
        output:
            result(bool):create success or fail

    updateUser(user)
        update user data
        input:
            user:(height,weight,workload,gender,calories,fat,carbs,protein,account)
        output:
            result(bool):update success or fail

    deleteUser(account)
        delete a user
        input:
            account(string):account that you want to delete
        output:
            result(bool):delete success or fail

    getUserInfo(account)
        if account exist then return its personal data
        input:
            account(string)
        output:
            info(tuple): (height,weight,workload,BMI,TDEE),if accunt is not exist return None

    listUser()
        the list of users that have been login at the machine
        input:
            None
        output:
            users:[string]: the list of all account 

