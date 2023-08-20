import requests
from datetime import datetime

# API endpoint URL
url = 'https://api.cricapi.com/v1/cricScore'

# API key
api_key = 'bd137e95-8626-426c-b690-b00d64476df2'

# Alphabet-to-number mapping
alphabet_mapping = {
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 1, 'k': 2, 'l': 3, 'm': 4,
    'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9, 's': 1, 't': 2, 'u': 3, 'v': 4, 'w': 5, 'x': 6, 'y': 7, 'z': 8
}

# Parameters
params = {
    'apikey': api_key,
    'offset': 0
}

# Recursive function to get a single-digit number


def get_single_digit(number):
    if number < 10:
        return number
    else:
        digit_sum = sum(int(digit) for digit in str(number))
        return get_single_digit(digit_sum)


# Send GET request to the API
response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract the data from the response
    data = response.json()

    # Process the data for matches that have started but not ended
    for match in data['data']:
        if match['ms'] == 'live':
            team1_name = match['t1'].split('[')[0].strip().lower()
            team2_name = match['t2'].split('[')[0].strip().lower()

            team1_value = sum(alphabet_mapping.get(char, 0)
                              for char in team1_name)
            team2_value = sum(alphabet_mapping.get(char, 0)
                              for char in team2_name)

            team1_single_digit = get_single_digit(team1_value)
            team2_single_digit = get_single_digit(team2_value)

            current_date = datetime.now().strftime('%d-%m-%Y')
            date_value = sum(int(digit)
                             for digit in current_date if digit.isdigit())
            date_single_digit = get_single_digit(date_value)

            print(match)



            print(f"Team1 Name: {team1_name.capitalize()}")
            print(f"Numeric Value: {team1_value}")
            print(f"Single Digit: {team1_single_digit}")
            if team1_single_digit % 2 == 0 and date_single_digit % 2 == 0:
                print("Result: Win")
            elif team1_single_digit % 2 != 0 and date_single_digit % 2 != 0:
                print("Result: Win")
            else:
                print("Result: Loss")

            print(f"Team2 Name: {team2_name.capitalize()}")
            print(f"Numeric Value: {team2_value}")
            print(f"Single Digit: {team2_single_digit}")
            if team2_single_digit % 2 == 0 and date_single_digit % 2 == 0:
                print("Result: Win")
            elif team2_single_digit % 2 != 0 and date_single_digit % 2 != 0:
                print("Result: Win")
            else:
                print("Result: Loss")


            print()
else:
    # Display an error message if the request was unsuccessful
    print(f'Request failed with status code: {response.status_code}')
