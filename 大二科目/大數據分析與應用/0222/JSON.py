import json

# Reading a JSON file
with open('example.json', 'r') as file:
    data = json.load(file)

# Accessing data
print(data['key'])

# Modifying data
data['new_key'] = 'new_value'

# Writing back to JSON file
with open('modified.json', 'w') as file:
    json.dump(data, file, indent=4)
