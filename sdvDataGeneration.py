import pandas as pd
import numpy as np
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata
from datetime import datetime, timedelta
import random
import json

# Load unique customer IDs from JSON file
with open('unique_customer_ids.json', 'r') as file:
    unique_customer_ids = json.load(file)

class InvestmentDataGenerator:
    locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
    occupations = ['Engineer', 'Doctor', 'Teacher', 'Lawyer', 'Artist']
    ethical_preferences = ['Environmental', 'Social', 'Governance', 'None']
    investment_goals = ['Retirement', 'Education', 'Wealth Building', 'Emergency Fund']
    risk_levels = ['Low', 'Medium', 'High']

    def generate_user(self, customer_id):
        return {
            "Customer_ID": customer_id,
            "Name": f"User_{customer_id}",
            "Age": random.randint(25, 65),
            "Gender": random.choice(['Male', 'Female', 'Other']),
            "Location": random.choice(self.locations),
            "Occupation": random.choice(self.occupations),
            "Income_Bracket": random.choice(['Low', 'Medium', 'High']),
            "Investment_Experience_Level": random.choice(['Beginner', 'Intermediate', 'Advanced']),
            "Ethical_Preferences": random.choice(self.ethical_preferences),
            "Financial_Goals": random.choice(self.investment_goals),
            "Risk_Tolerance": random.choice(self.risk_levels),
            "Goal_Type": random.choice(['Growth', 'Income', 'Balanced']),
        }

    def generate_complete_dataset(self, num_users=1):
        dataset = []
        
        for i in range(len(unique_customer_ids)):
            customer_id = unique_customer_ids[i]
            creation_date = datetime.now() - timedelta(days=random.randint(30, 365))
            
            user_data = {
                "User": {
                    **self.generate_user(customer_id)
                }
            }
            dataset.append(user_data)
        
        return dataset

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Usage example
if __name__ == "__main__":
    generator = InvestmentDataGenerator()
    synthetic_data = generator.generate_complete_dataset(num_users=5)
    save_to_json(synthetic_data, 'random_synthetic_investment_data.json')

print("Script Ran Successfully!!!")