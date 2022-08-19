# user = (account,machine_id,height,weight,workload,gender,calories,fat,carbs,protein)
class User():
    def __init__(self, name = ""):
        self.name = name

    def setupUserInfo(self, info_list):
        self.name = info_list[0]
        self.height = info_list[2]
        self.weight = info_list[3]
        self.workload = info_list[4]
        self.gender = info_list[5]
        
        self.BMI = computeBMI(self.height, self.weight)
        self.TDEE = computeTDEE(self.height, self.weight, self.workload, self.gender)

        self.cal = info_list[6]
        self.fat = info_list[7]
        self.carbs = info_list[8]
        self.protein = info_list[9]

    def setupDailyDiet(self, daily_info):
        self.daily_cal = daily_info[0]
        self.daily_fat = daily_info[1]
        self.daily_carbs = daily_info[2]
        self.daily_protein = daily_info[3]

def computeBMI(height, weight):
    if height == 0: return 0
    return round(weight / ((height/100)**2), 2)

def computeTDEE(height, weight, workload, gender):
    if height == 0 or weight == 0: return 0
    if gender == 1:    # male
        std_weight = (height-80) * 0.7
    else:
        std_weight = (height-70) * 0.6
    std_weight_lower = std_weight * 0.9
    std_weight_upper = std_weight * 1.1
    
    if workload == "light":
        if weight < std_weight_lower:      tdee = 35*std_weight
        elif weight > std_weight_upper:    tdee = 30*std_weight
        else:                              tdee = 25*std_weight

    elif workload == "mid":
        if weight < std_weight_lower:      tdee = 40*std_weight
        elif weight > std_weight_upper:    tdee = 35*std_weight
        else:                              tdee = 30*std_weight

    elif workload == "heavy":
        if weight < std_weight_lower:      tdee = 45*std_weight
        elif weight > std_weight_upper:    tdee = 40*std_weight
        else:                              tdee = 35*std_weight
    return int(tdee)

def computeDiet(cal):
    fat = int(cal * 0.23 / 9)
    carbs = int(cal * 0.65 / 4)
    protein = int(cal * 0.12 / 4)
    return fat, carbs, protein

id = 0
user = User()
user_list = []
page = ["Welcome"]
back_flag = False
create_new_account_flag = False

def backToLastPage():
    global page, back_flag
    back_flag = True
    page.pop()