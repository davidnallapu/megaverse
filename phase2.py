import time
import requests

# Your Candidate ID
CANDIDATE_ID = 'ecc38c1c-d6e2-42c9-8bdd-c96f3264e820'

# API URLs
MEGAVERSE_API_POLYANETS_URL = "https://challenge.crossmint.io/api/polyanets"
MEGAVERSE_API_SOLOONS_URL = "https://challenge.crossmint.io/api/soloons"
MEGAVERSE_API_COMETHS_URL = "https://challenge.crossmint.io/api/comeths"

# Goal data URL (You can modify this to fetch real-time data)
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

# Function to create a Polyanet
def create_polyanet(row, column):
    print(f"Creating Polyanet at row {row}, column {column}...")
    response = requests.post(MEGAVERSE_API_POLYANETS_URL, json={
        'candidateId': CANDIDATE_ID,
        'row': row,
        'column': column
    })
    return response

# Function to create a Soloon
def create_soloon(row, column, color):
    print(f"Creating {color.capitalize()} Soloon at row {row}, column {column}...")
    response = requests.post(MEGAVERSE_API_SOLOONS_URL, json={
        'candidateId': CANDIDATE_ID,
        'row': row,
        'column': column,
        'color': color
    })
    return response

# Function to create a Cometh
def create_cometh(row, column, direction):
    print(f"Creating {direction.capitalize()} Cometh at row {row}, column {column}...")
    response = requests.post(MEGAVERSE_API_COMETHS_URL, json={
        'candidateId': CANDIDATE_ID,
        'row': row,
        'column': column,
        'direction': direction
    })
    return response

# Function to process the goal data and create objects on the map
def process_goal_data(goal_data):

    goal = goal_data['goal']  # Access the 'goal' array
    
    print("Processing goal data...")

    for row_index, row in enumerate(goal):
        for col_index, value in enumerate(row):
            if value == 'POLYANET':
                # Create a Polyanet
                response = create_polyanet(row_index, col_index)
                print(f'Polyanet at ({row_index}, {col_index}) - Status: {response.status_code}')
                time.sleep(2)  # 2-second delay between each request
            
            elif value.endswith('_SOLOON'):
                # Extract the color from the value (e.g., "WHITE_SOLOON" -> "white")
                color = value.split('_')[0].lower()
                response = create_soloon(row_index, col_index, color)
                print(f'{color.capitalize()} Soloon at ({row_index}, {col_index}) - Status: {response.status_code}')
                time.sleep(2)  # 2-second delay between each request
            
            elif value.endswith('_COMETH'):
                # Extract the direction from the value (e.g., "UP_COMETH" -> "up")
                direction = value.split('_')[0].lower()
                response = create_cometh(row_index, col_index, direction)
                print(f'{direction.capitalize()} Cometh at ({row_index}, {col_index}) - Status: {response.status_code}')
                time.sleep(2)  # 2-second delay between each request
            
            else:
                print(f"There is a: {value}, so not calling the api")
                # Not adding delay here because Im not calling the API.
            

# Main execution logic
if __name__ == '__main__':
    print("Fetching goal data...")
    goal_data = get_goal_data()  # Fetch the goal data from the API

    if goal_data:
        print("Generating Crossmint logo automatically...")
        process_goal_data(goal_data)  # This triggers the creation of Polyanets once and then exits
        print("\nCrossmint logo generated!")
    else:
        print("Failed to retrieve goal data. Exiting.")

    # app.run(debug=False) # Not running a server as I need to do this only once