import json

model_name = "inceptionv3_0825"

classes = ['Apple', 'Banana', 'Grape', 'Guava', 'Tomato', \
           'dumplings', 'french_fries', 'fried_rice', 'pizza', 'steak']

# Apple', 'Banana', 'Grape', 'Guava', 'Tomato',\
#         'dumplings', 'french_fries', 'ice_cream', 'pizza', 'steak', 'sushi'

json_string = json.dumps(classes)
print(json_string)


# output 
with open("{}.json".format(model_name), 'w') as f:
    json.dump(json_string, f)
# Closing file
f.close()
