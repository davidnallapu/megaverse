from flask import Flask, jsonify
import requests
import time
import os

app = Flask(__name__)

# Replace this with your actual candidateId
CANDIDATE_ID = "ecc38c1c-d6e2-42c9-8bdd-c96f3264e820"
MEGAVERSE_API_BASE_URL = "https://challenge.crossmint.io/api/polyanets"
GOAL_URL = f'https://challenge.crossmint.com/api/map/{CANDIDATE_ID}/goal'

# Function to get the goal data from the API
def get_goal_data():
    response = requests.get(GOAL_URL)
    if response.status_code == 200:
        print("Goal Data Retrieved Successfully!")
        return response.json()
    else:
        print(f"Failed to retrieve goal data. Status Code: {response.status_code}, Response: {response.text}")
        return None
    
# Function to create a Polyanet at the specified row and column
def create_polyanet(row, column):
    response = requests.post(MEGAVERSE_API_BASE_URL, json={
        'candidateId': CANDIDATE_ID,
        'row': row,
        'column': column
    })
    return response

# Function to automatically generate Polyanets based on the provided goal data
def generate_polyanets(goal_data):
    goal = goal_data['goal']  # Accessing the 'goal' array
    
    # Loop through the rows and columns to find 'POLYANET'
    for row_index, row in enumerate(goal):
        for col_index, value in enumerate(row):
            if value == 'POLYANET':
                # Call the create_polyanet function to create the Polyanet at the row and column
                response = create_polyanet(row_index, col_index)

                # Log the status code and response body for debugging
                print(f'\nRequest to create Polyanet at row {row_index}, column {col_index}:')
                print(f'Status Code: {response.status_code}')
                print(f'Response: {response.text}')

                if response.status_code != 201:  # Consider 200 as success
                    print(f'Polyanet created successfully at row {row_index}, column {col_index}')
                else:
                    print(f'Failed to create Polyanet at row {row_index}, column {col_index}. Error: {response.json()}')

                # Add a delay to avoid "Too Many Requests" error i.e Rate limting 
                time.sleep(2)  # Wait for 2 seconds before sending the next request

# Main execution logic
if __name__ == '__main__':
    print("Fetching goal data...")
    goal_data = get_goal_data()  # Fetch the goal data from the API

    if goal_data:
        print("Generating Polyanets automatically...")
        generate_polyanets(goal_data)  # This triggers the creation of Polyanets once and then exits
        print("\nPolyanets generated!")
    else:
        print("Failed to retrieve goal data. Exiting.")

    # app.run(debug=False) # Not running a server as I need to do this only once