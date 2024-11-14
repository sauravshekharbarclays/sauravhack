import random
import json
from datetime import datetime, timedelta
import pandas as pd
from sdv.metadata import Metadata
from sdv.single_table import GaussianCopulaSynthesizer

# Define the activities and their descriptions
activities = [
    {"name": "Pay", "description": "Funding smart investor account using existing bank account or debit card"},
    {"name": "Withdraw", "description": "Withdrawing cash present in smart investor account to bank account"},
    {"name": "Explore Funds", "description": "Search, explore and learn about various bank promoted ready made funds and multi manager funds, view their info and performances. Also letting them proceed to investing in it if chosen."},
    {"name": "Search Investments", "description": "Search Investment Instruments via filters and criteria to look for equities, funds ETFs, know more about them and proceed to invest."},
    {"name": "Buy", "description": "Going directly to buy and invest in an instrument customer is already aware and decided."},
    {"name": "Sell", "description": "Going directly to sell an instrument present in customer's holdings."},
    {"name": "Order History", "description": "Let a customer go through his trading and investment history."},
    {"name": "Settings", "description": "Various account and portfolio level settings"},
    {"name": "Portfolio", "description": "Looking at portfolio in terms of all holding its value, invested amount and gain loss and performance at various levels."}
]

# Generate initial data for training the model
def generate_initial_data(num_records=1000):
    data = {
        'customer_id': [i for i in range(1000000000, 1000000000 + num_records)],
        'activity': [random.choice([activity["name"] for activity in activities]) for _ in range(num_records)],
        'start_time': [(datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S') for _ in range(num_records)],
        'duration': [random.randint(1, 300) for _ in range(num_records)]
    }
    return pd.DataFrame(data)

# Define metadata for the data schema
metadata = Metadata()
metadata.detect_table_from_dataframe(table_name='user_interactions', data=generate_initial_data())

# Save metadata to JSON for replicability
metadata.save_to_json('metadata.json')

# Generate synthetic user interaction data
def generate_synthetic_data(num_users=80, total_sessions=500):
    initial_data = generate_initial_data(num_users * total_sessions * 10)  # Generate more data for variability
    synthesizer = GaussianCopulaSynthesizer(metadata)
    synthesizer.fit(initial_data)
    
    synthetic_data = synthesizer.sample(num_users * total_sessions * 10)
    
    user_data = []
    sessions_per_user = [random.randint(1, 10) for _ in range(num_users)]
    total_sessions_generated = 0
    
    for customer_id in synthetic_data['customer_id'].unique():
        if total_sessions_generated >= total_sessions:
            break
        if not sessions_per_user:
            break
        sessions = []
        customer_data = synthetic_data[synthetic_data['customer_id'] == customer_id]
        num_sessions = sessions_per_user.pop()
        for _ in range(num_sessions):
            if total_sessions_generated >= total_sessions:
                break
            interactions_per_session = random.randint(1, 10)
            if len(customer_data) < interactions_per_session:
                interactions_per_session = len(customer_data)
            session_interactions = customer_data.sample(interactions_per_session).to_dict(orient='records')
            used_activities = set()
            for interaction in session_interactions:
                available_activities = [activity["name"] for activity in activities if activity["name"] not in used_activities]
                if available_activities:
                    interaction['activity'] = random.choice(available_activities)
                    used_activities.add(interaction['activity'])
                interaction['end_time'] = (datetime.strptime(interaction['start_time'], '%Y-%m-%d %H:%M:%S') + timedelta(seconds=interaction['duration'])).strftime('%Y-%m-%d %H:%M:%S')
            sessions.append({
                "customer_id": int(customer_id),  # Convert to standard Python int
                "interactions": session_interactions
            })
            total_sessions_generated += 1
        user_data.append({
            "customer_id": int(customer_id),  # Convert to standard Python int
            "sessions": sessions
        })
    
    return user_data

# Generate data for 80 users with a total of 500 sessions and variable interactions per session
user_interaction_data = generate_synthetic_data()

# Add activity metadata
activity_metadata = {activity["name"]: activity["description"] for activity in activities}

# Combine data and metadata
output_data = {
    "activity_metadata": activity_metadata,
    "user_interactions": user_interaction_data
}

# Save the data to a JSON file
with open("user_interaction_data.json", "w") as f:
    json.dump(output_data, f, indent=4)

print("Synthetic user interaction data generated and saved to user_interaction_data.json")