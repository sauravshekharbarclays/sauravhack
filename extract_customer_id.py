import json

# Load the JSON data from the file
with open('user_interaction_data.json', 'r') as file:
    data = json.load(file)

# Extract unique customer IDs
unique_customer_ids = set()

for user in data['user_interactions']:
    unique_customer_ids.add(user['customer_id'])
    for session in user['sessions']:
        unique_customer_ids.add(session['customer_id'])
        for interaction in session['interactions']:
            unique_customer_ids.add(interaction['customer_id'])

# Convert the set to a sorted list
unique_customer_ids = sorted(unique_customer_ids)

# Save the unique customer IDs to a new JSON file
with open('unique_customer_ids.json', 'w') as file:
    json.dump(unique_customer_ids, file, indent=4)

print("Unique customer IDs extracted and saved to unique_customer_ids.json")