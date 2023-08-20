from flask import Blueprint, Flask, render_template
import requests
from datetime import datetime
import traceback

live_bp = Blueprint('live', __name__, url_prefix='/')


@live_bp.route('/')
def get_live_matches():
    try:

        # API endpoint URL
        # Define your API key
        cricket_api_key = '9b7d604d50ceaba560c57dab362bde430303cbad9a1e48b762655d6c34ba75db'

        # API endpoint URL with the API key
        url = f'https://apiv2.api-cricket.com/?method=get_livescore&APIkey={cricket_api_key}'
        # Send GET request to the API
        response = requests.get(url)

        current_date_gmt = datetime.utcnow().strftime('%Y-%m-%d')

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the data from the response
            data = response.json()

            # Check if there are matches available
            if 'result' in data and data['result']:
                # Process the data for live matches
                live_matches = []
                upcomming_matches = []
                today_upcomming_matches = []
                for match in data['result']:
                    if match['event_status'] == 'In Progress':
                        team1_score = match['event_home_final_result']
                        team2_score = match['event_away_final_result']
                        team1_name = match['event_home_team'].split('[')[
                            0].strip().lower()
                        team2_name = match['event_away_team'].split('[')[
                            0].strip().lower()
                        scorecard = match.get("scorecard", {})
                        # Extract runs and overs from team1score
                        team1_runs = ''
                        team1_overs = ''

                        # wicket getting
                        team1_wickets = ''
                        team2_wickets = ''

                        if '/' in team1_score:
                            team1_runs, team1_wickets = team1_score.split('/')
                            # Extracting the wickets part before any additional information
                            team1_wickets = team1_wickets.split()[0]
                            team1_runs = int(team1_runs)
                            team1_wickets = int(team1_wickets)
                            print(team1_runs)
                            print(team1_wickets)
                            # print(scorecard.extra)

                        # Extract runs and overs from team2score
                        team2_runs = ''
                        team2_overs = ''

                        if '/' in team2_score:
                            team2_runs, team2_wickets = team2_score.split('/')
                            # Extracting the wickets part before any additional information
                            team2_wickets = team2_wickets.split()[0]
                            team2_runs = int(team2_runs)
                            team2_wickets = int(team2_wickets)
                            print(team2_runs)
                            print(team2_wickets)

                        for inning_key, inning_data in scorecard.items():
                            if match.get("event_home_team") in inning_key and "1 INN" in inning_key:
                                team1_overs = match.get("extra", {}).get(
                                    inning_key, {}).get("total_overs", "")

                                # break
                            elif match.get("event_home_team") in inning_key and "2 INN" in inning_key:
                                team1_overs = match.get("extra", {}).get(
                                    inning_key, {}).get("total_overs", "")

                                # break

                        for inning_key, inning_data in scorecard.items():
                            if match.get("event_away_team") in inning_key and "1 INN" in inning_key:
                                team2_overs = match.get("extra", {}).get(
                                    inning_key, {}).get("total_overs", "")

                                # break
                            elif match.get("event_away_team") in inning_key and "1 INN" in inning_key:
                                team2_overs = match.get("extra", {}).get(
                                    inning_key, {}).get("total_overs", "")

                                # break

                        print(team1_overs, 'overs team1')
                        print(team2_overs, 'overs team2')

                        # Convert runs and overs to appropriate data types
                        team1_runs = int(team1_runs) if team1_runs else None
                        team1_overs = float(
                            team1_overs) if team1_overs else None
                        team2_runs = int(team2_runs) if team2_runs else None
                        team2_overs = float(
                            team2_overs) if team2_overs else None

                        # Calculate run rate
                        team1_current_run_rate = round(
                            team1_runs / team1_overs, 2) if team1_runs and team1_overs else None
                        team2_current_run_rate = round(
                            team2_runs / team2_overs, 2) if team2_runs and team2_overs else None

                        team1_run_rate = None
                        team2_run_rate = None
                        team1_calculated_run_rate = None
                        team2_calculated_run_rate = None
                        if match['event_type'] == 'T20':
                            if team1_wickets is not None:
                                # team1_wickets = int(team1_wicket)
                                if team1_current_run_rate is not None:
                                    if team1_wickets == 0:
                                        if team1_current_run_rate < 8:
                                            team1_run_rate = 7.5
                                        elif team1_current_run_rate >= 8:
                                            team1_run_rate = 8.5
                                        elif team1_current_run_rate >= 10:
                                            team1_run_rate = 9.5
                                        else:
                                            team1_run_rate = team1_current_run_rate
                                    elif 1 <= team1_wickets <= 5:
                                        if team1_current_run_rate <= 6:
                                            team1_run_rate = (
                                                6 + 1 - (team1_wickets * 0.4))
                                        elif team1_current_run_rate > 6:
                                            team1_run_rate = (
                                                team1_current_run_rate + 2 - (team1_wickets * 0.4))
                                        elif team1_current_run_rate >= 10:
                                            team1_run_rate = (
                                                11.2 - team1_wickets * 0.4)
                                        else:
                                            team1_run_rate = team1_current_run_rate
                                    elif team1_wickets >= 5:
                                        team1_run_rate = team1_current_run_rate
                            else:
                                team1_run_rate = None

                            if team2_wickets is not None:
                                # team2_wickets = int(team2_wicket)
                                if team2_current_run_rate is not None:
                                    if team2_wickets == 0:
                                        if team2_current_run_rate < 8:
                                            team2_run_rate = 7.5
                                        elif team2_current_run_rate >= 8:
                                            team2_run_rate = 8.5
                                        elif team2_current_run_rate >= 10:
                                            team2_run_rate = 9.5
                                        else:
                                            team2_run_rate = team2_current_run_rate
                                    elif 1 <= team2_wickets <= 5:
                                        if team2_current_run_rate <= 6:
                                            team2_run_rate = (
                                                6 + 1 - (team2_wickets * 0.4))
                                        elif team2_current_run_rate > 6:
                                            team2_run_rate = (
                                                team2_current_run_rate + 2 - (team2_wickets * 0.4))
                                        elif team2_current_run_rate >= 10:
                                            team2_run_rate = (
                                                11.2 - team2_wickets * 0.4)
                                        else:
                                            team2_run_rate = team2_current_run_rate
                                    elif team2_wickets >= 5:
                                        team2_run_rate = team2_current_run_rate
                            else:
                                team2_run_rate = None

                            team1_estimated_run = team1_run_rate * \
                                20 if team1_run_rate is not None else None
                            team2_estimated_run = team2_run_rate * \
                                20 if team2_run_rate is not None else None
                            if team1_wickets == 10:
                                team1_estimated_run = team1_runs

                            if team2_wickets == 10:
                                team2_estimated_run = team2_runs

                            team_winning = ""
                            if team1_estimated_run is not None and team2_estimated_run is not None:
                                if team1_estimated_run > team2_estimated_run:
                                    team_winning = team1_name + " will win"
                                elif team2_estimated_run > team1_estimated_run:
                                    team_winning = team2_name + " will win"
                                else:
                                    team_winning = "Should Wait"
                            estimated_team1_runOver = None
                            estimated_team2_runOver = None
                            if team1_overs is not None:
                                if team1_overs <= 5:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 5 if team1_current_run_rate is not None else None,
                                        'overs': 5
                                    }
                                elif team1_overs <= 10:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 10 if team1_current_run_rate is not None else None,
                                        'overs': 10
                                    }
                                elif team1_overs <= 15:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 15 if team1_current_run_rate is not None else None,
                                        'overs': 15
                                    }
                                elif team1_overs <= 20:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 20 if team1_current_run_rate is not None else None,
                                        'overs': 20
                                    }

                            else:
                                estimated_team1_runOver = None

                            if team2_overs is not None:
                                if team2_overs <= 5:
                                    estimated_team2_runOver = {
                                        'runs': team2_run_rate * 5 if team2_run_rate is not None else None,
                                        'overs': 5
                                    }
                                elif team2_overs <= 10:
                                    estimated_team2_runOver = {
                                        'runs': team2_run_rate * 10 if team2_run_rate is not None else None,
                                        'overs': 10
                                    }
                                elif team2_overs <= 15:
                                    estimated_team2_runOver = {
                                        'runs': team2_run_rate * 15 if team2_run_rate is not None else None,
                                        'overs': 15
                                    }
                                elif team2_overs <= 20:
                                    estimated_team2_runOver = {
                                        'runs': team2_run_rate * 20 if team2_run_rate is not None else None,
                                        'overs': 20
                                    }

                            else:
                                estimated_team2_runOver = None

                        elif match['event_type'] == 'odi':
                            if team1_current_run_rate is not None:
                                if team1_current_run_rate >= 5:
                                    team1_run_rate = 5.5
                                elif team1_current_run_rate <= 4:
                                    team1_run_rate = 5
                                else:
                                    team1_run_rate = team1_current_run_rate
                                if team1_wicket is not None:
                                    team1_wicket = int(team1_wicket)
                                    if 1 <= team1_wicket <= 3:
                                        team1_run_rate = (
                                            team1_current_run_rate + 2) - (team1_wicket * 0.8)
                                    elif 4 <= team1_wicket <= 5:
                                        team1_run_rate = (
                                            team1_current_run_rate + 2) - (team1_wicket * 0.4)
                                    elif team1_wicket >= 6:
                                        team1_run_rate = team1_current_run_rate
                                    else:
                                        team1_run_rate = team1_run_rate
                            else:
                                team1_run_rate = None
                            if team2_current_run_rate is not None:
                                if team2_current_run_rate >= 5:
                                    team2_run_rate = 5.5
                                elif team2_current_run_rate <= 4:
                                    team2_run_rate = 5
                                else:
                                    team2_run_rate = team2_current_run_rate
                                if team2_wicket is not None:
                                    team2_wicket = int(team2_wicket)
                                    if 1 <= team2_wicket <= 3:
                                        team2_run_rate = (
                                            team2_current_run_rate + 2) - (team2_wicket * 0.8)
                                    elif 4 <= team2_wicket <= 5:
                                        team2_run_rate = (
                                            team2_current_run_rate + 2) - (team2_wicket * 0.4)
                                    elif team2_wicket >= 6:
                                        team2_run_rate = team2_current_run_rate
                                    else:
                                        team2_run_rate = team2_run_rate
                            else:
                                team2_run_rate = None
                            team1_estimated_run = team1_run_rate * \
                                50 if team1_run_rate is not None else None
                            team2_estimated_run = team2_run_rate * \
                                50 if team2_run_rate is not None else None
                            team_winning = ""
                            if team1_estimated_run is not None and team2_estimated_run is not None:
                                if team1_estimated_run > team2_estimated_run:
                                    team_winning = team1_name + " will win"
                                elif team2_estimated_run > team1_estimated_run:
                                    team_winning = team2_name + " will win"
                                else:
                                    team_winning = "Should Wait"
                            estimated_team1_runOver = None
                            estimated_team2_runOver = None

                            if team1_overs is not None:
                                if team1_overs <= 5:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 5 if team1_current_run_rate is not None else None,
                                        'overs': 5
                                    }
                                elif team1_overs <= 10:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 10 if team1_current_run_rate is not None else None,
                                        'overs': 10
                                    }
                                elif team1_overs <= 15:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 15 if team1_current_run_rate is not None else None,
                                        'overs': 15
                                    }
                                elif team1_overs <= 20:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 20 if team1_current_run_rate is not None else None,
                                        'overs': 20
                                    }
                                elif team1_overs <= 25:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 25 if team1_current_run_rate is not None else None,
                                        'overs': 25
                                    }
                                elif team1_overs <= 30:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 30 if team1_current_run_rate is not None else None,
                                        'overs': 30
                                    }
                                elif team1_overs <= 35:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 35 if team1_current_run_rate is not None else None,
                                        'overs': 35
                                    }
                                elif team1_overs <= 40:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 40 if team1_current_run_rate is not None else None,
                                        'overs': 40
                                    }
                                elif team1_overs <= 45:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 45 if team1_current_run_rate is not None else None,
                                        'overs': 45
                                    }
                                elif team1_overs <= 50:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 50 if team1_current_run_rate is not None else None,
                                        'overs': 50
                                    }

                            else:
                                estimated_team1_runOver = None

                            if team2_overs is not None:
                                if team2_overs <= 5:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 5 if team2_current_run_rate is not None else None,
                                        'overs': 5
                                    }
                                elif team2_overs <= 10:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 10 if team2_current_run_rate is not None else None,
                                        'overs': 10
                                    }
                                elif team2_overs <= 15:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 15 if team2_current_run_rate is not None else None,
                                        'overs': 15
                                    }
                                elif team2_overs <= 20:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 20 if team2_current_run_rate is not None else None,
                                        'overs': 20
                                    }
                                elif team2_overs <= 25:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 25 if team2_current_run_rate is not None else None,
                                        'overs': 25
                                    }
                                elif team2_overs <= 30:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 30 if team2_current_run_rate is not None else None,
                                        'overs': 30
                                    }
                                elif team2_overs <= 35:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 35 if team2_current_run_rate is not None else None,
                                        'overs': 35
                                    }
                                elif team2_overs <= 40:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 40 if team2_current_run_rate is not None else None,
                                        'overs': 40
                                    }
                                elif team2_overs <= 45:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 45 if team2_current_run_rate is not None else None,
                                        'overs': 45
                                    }
                                elif team2_overs <= 50:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 50 if team2_current_run_rate is not None else None,
                                        'overs': 50
                                    }

                            else:
                                estimated_team2_runOver = None

                        elif match['event_type'] == 'test':
                            if team1_wicket is not None:
                                team1_wicket = int(team1_wicket)
                                if team1_current_run_rate is not None:
                                    if team1_wicket == 0:
                                        if team1_current_run_rate < 4:
                                            team1_run_rate = 3
                                        elif team1_current_run_rate >= 4:
                                            team1_run_rate = 4
                                        else:
                                            team1_run_rate = team1_current_run_rate
                                    elif 1 <= team1_wicket <= 5:
                                        if team1_current_run_rate <= 4:
                                            team1_run_rate = (
                                                (team1_current_run_rate) - (team1_wicket * 0.4))
                                        elif team1_current_run_rate > 4:
                                            team1_run_rate = (
                                                4.5 - (team1_wicket * 0.4))
                                        else:
                                            team1_run_rate = team1_current_run_rate
                                    elif team1_wicket >= 5:
                                        if team1_current_run_rate >= 4:
                                            team1_run_rate = (
                                                4.5 - (team1_wicket * 0.2))
                                        elif team1_current_run_rate < 4:
                                            team1_run_rate = (
                                                4 - (team1_wicket * 0.2))
                                        else:
                                            team1_run_rate = team1_current_run_rate
                                    else:
                                        team1_run_rate = team1_current_run_rate
                            else:
                                team2_run_rate = None
                            if team2_wicket is not None:
                                team2_wicket = int(team2_wicket)
                                if team2_current_run_rate is not None:
                                    if team2_wicket == 0:
                                        if team2_current_run_rate < 4:
                                            team2_run_rate = 3
                                        elif team2_current_run_rate >= 4:
                                            team2_run_rate = 4
                                        else:
                                            team2_run_rate = team2_current_run_rate
                                    elif 1 <= team2_wicket <= 5:
                                        if team2_current_run_rate <= 4:
                                            team2_run_rate = (
                                                (team2_current_run_rate) - (team2_wicket * 0.4))
                                        elif team2_current_run_rate > 4:
                                            team2_run_rate = (
                                                4.5 - (team2_wicket * 0.4))
                                        else:
                                            team2_run_rate = team2_current_run_rate
                                    elif team2_wicket >= 5:
                                        if team2_current_run_rate >= 4:
                                            team2_run_rate = (
                                                4.5 - (team2_wicket * 0.2))
                                        elif team2_current_run_rate < 4:
                                            team2_run_rate = (
                                                4 - (team2_wicket * 0.2))
                                        else:
                                            team2_run_rate = team2_current_run_rate
                                    else:
                                        team2_run_rate = team2_current_run_rate
                            else:
                                team2_run_rate = None
                            if team1_wicket is None:
                                team1_wicket_left = 10
                            else:
                                team1_wicket_left = 10 - team1_wicket
                            if team2_wicket is None:
                                team2_wicket_left = 10
                            else:
                                team2_wicket_left = 10 - team2_wicket
                            team1_estimated_run = (
                                team1_overs + team1_wicket_left * 10) * (team1_run_rate - (0.1 * team1_wicket)) if team1_run_rate is not None else None
                            team2_estimated_run = (
                                team2_overs + team2_wicket_left * 10) * (team2_run_rate - (0.1 * team2_wicket)) if team2_run_rate is not None else None
                            team_winning = ""
                            if team1_estimated_run is not None and team2_estimated_run is not None:
                                if team1_estimated_run > team2_estimated_run:
                                    team_winning = team1_name + " will win"
                                elif team2_estimated_run > team1_estimated_run:
                                    team_winning = team2_name + " will win"
                                else:
                                    team_winning = "Should Wait"
                            estimated_team1_runOver = None
                            estimated_team2_runOver = None

                            if team1_overs is not None:
                                if team1_overs <= 5:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 5 if team1_current_run_rate is not None else None,
                                        'overs': 5
                                    }
                                elif team1_overs <= 10:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 10 if team1_current_run_rate is not None else None,
                                        'overs': 10
                                    }
                                elif team1_overs <= 15:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 15 if team1_current_run_rate is not None else None,
                                        'overs': 15
                                    }
                                elif team1_overs <= 20:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 20 if team1_current_run_rate is not None else None,
                                        'overs': 20
                                    }
                                elif team1_overs <= 25:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 25 if team1_current_run_rate is not None else None,
                                        'overs': 25
                                    }
                                elif team1_overs <= 30:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 30 if team1_current_run_rate is not None else None,
                                        'overs': 30
                                    }
                                elif team1_overs <= 35:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 35 if team1_current_run_rate is not None else None,
                                        'overs': 35
                                    }
                                elif team1_overs <= 40:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 40 if team1_current_run_rate is not None else None,
                                        'overs': 40
                                    }
                                elif team1_overs <= 45:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 45 if team1_current_run_rate is not None else None,
                                        'overs': 45
                                    }
                                elif team1_overs <= 50:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 50 if team1_current_run_rate is not None else None,
                                        'overs': 50
                                    }
                                elif team1_overs <= 55:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 55 if team1_current_run_rate is not None else None,
                                        'overs': 55
                                    }
                                elif team1_overs <= 60:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 60 if team1_current_run_rate is not None else None,
                                        'overs': 60
                                    }
                                elif team1_overs <= 65:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 65 if team1_current_run_rate is not None else None,
                                        'overs': 65
                                    }
                                elif team1_overs <= 70:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 70 if team1_current_run_rate is not None else None,
                                        'overs': 70
                                    }
                                elif team1_overs <= 75:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 75 if team1_current_run_rate is not None else None,
                                        'overs': 75
                                    }
                                elif team1_overs <= 80:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 80 if team1_current_run_rate is not None else None,
                                        'overs': 80
                                    }
                                elif team1_overs <= 85:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 85 if team1_current_run_rate is not None else None,
                                        'overs': 85
                                    }
                                elif team1_overs <= 90:
                                    estimated_team1_runOver = {
                                        'runs': team1_current_run_rate * 90 if team1_current_run_rate is not None else None,
                                        'overs': 90
                                    }
                            else:
                                estimated_team1_runOver = None

                            if team2_overs is not None:
                                if team2_overs <= 5:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 5 if team2_current_run_rate is not None else None,
                                        'overs': 5
                                    }
                                elif team2_overs <= 10:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 10 if team2_current_run_rate is not None else None,
                                        'overs': 10
                                    }
                                elif team2_overs <= 15:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 15 if team2_current_run_rate is not None else None,
                                        'overs': 15
                                    }
                                elif team2_overs <= 20:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 20 if team2_current_run_rate is not None else None,
                                        'overs': 20
                                    }
                                elif team2_overs <= 25:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 25 if team2_current_run_rate is not None else None,
                                        'overs': 25
                                    }
                                elif team2_overs <= 30:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 30 if team2_current_run_rate is not None else None,
                                        'overs': 30
                                    }
                                elif team2_overs <= 35:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 35 if team2_current_run_rate is not None else None,
                                        'overs': 35
                                    }
                                elif team2_overs <= 40:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 40 if team2_current_run_rate is not None else None,
                                        'overs': 40
                                    }
                                elif team2_overs <= 45:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 45 if team2_current_run_rate is not None else None,
                                        'overs': 45
                                    }
                                elif team2_overs <= 50:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 50 if team2_current_run_rate is not None else None,
                                        'overs': 50
                                    }
                                elif team2_overs <= 55:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 55 if team2_current_run_rate is not None else None,
                                        'overs': 55
                                    }
                                elif team2_overs <= 60:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 60 if team2_current_run_rate is not None else None,
                                        'overs': 60
                                    }
                                elif team2_overs <= 65:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 65 if team2_current_run_rate is not None else None,
                                        'overs': 65
                                    }
                                elif team2_overs <= 70:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 70 if team2_current_run_rate is not None else None,
                                        'overs': 70
                                    }
                                elif team2_overs <= 75:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 75 if team2_current_run_rate is not None else None,
                                        'overs': 75
                                    }
                                elif team2_overs <= 80:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 80 if team2_current_run_rate is not None else None,
                                        'overs': 80
                                    }
                                elif team2_overs <= 85:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 85 if team2_current_run_rate is not None else None,
                                        'overs': 85
                                    }
                                elif team2_overs <= 90:
                                    estimated_team2_runOver = {
                                        'runs': team2_current_run_rate * 90 if team2_current_run_rate is not None else None,
                                        'overs': 90
                                    }
                            else:
                                estimated_team2_runOver = None

                        else:
                            team1_run_rate = team1_current_run_rate
                            team2_run_rate = team2_current_run_rate
                            estimated_team1_runOver = None
                            estimated_team2_runOver = None
                            team1_estimated_run = None
                            team2_estimated_run = None
                            team_winning = None

                        live_match = {
                            # 'id': match['id'],
                            # 'dateTimeGMT': match['dateTimeGMT'],
                            'matchType': match['event_type'],
                            # 'status': match['status'],
                            'team1': match['event_home_team'],
                            'team2': match['event_away_team'],
                            'team1Score': team1_score,
                            'team2Score': team2_score,
                            'team1RunRate': team1_current_run_rate,
                            'team1CalculatedRunRate': team1_run_rate,
                            'team2CalculatedRunRate': team2_run_rate,
                            'team2RunRate': team2_current_run_rate,
                            'teamWinning': team_winning,
                            'team1Wicket': team1_wickets,
                            'team2Wicket': team2_wickets,
                            'team1EstimatedRun': team1_estimated_run,
                            'team2EstimatedRun': team2_estimated_run,
                            'estimatedTeam1RunOver': estimated_team1_runOver,
                            'estimatedTeam2RunOver': estimated_team2_runOver,
                        }
                        live_matches.append(live_match)

                    # if match['status'] == 'Match not started':
                    #     upcomming_match = {
                    #         'id': match['id'],
                    #         'dateTimeGMT': match['dateTimeGMT'],
                    #         'matchType': match['matchType'],
                    #         'matchDate': match['dateTimeGMT'][:10],
                    #         'status': match['status'],
                    #         'matchStatus': match['ms'],
                    #         'team1': match['t1'],
                    #         'team2': match['t2'],
                    #     }
                    #     upcomming_matches.append(upcomming_match)

                    # if match['status'] == 'Match not started' and match['dateTimeGMT'][:10] == current_date_gmt:
                    #     today_upcomming_match = {
                    #         'id': match['id'],
                    #         'dateTimeGMT': match['dateTimeGMT'],
                    #         'matchType': match['matchType'],
                    #         'status': match['status'],
                    #         'team1': match['t1'],
                    #         'team2': match['t2'],
                    #     }
                    #     today_upcomming_matches.append(today_upcomming_match)

                # Render the template with the live matches data
                return render_template('index.html', matches=live_matches)
            else:
                return 'No live matches found.'
        else:
            # Display an error message if the request was unsuccessful
            return f'Request failed with status code: {response.status_code}'
    except Exception as e:
        error_message = f'An error occurred: {str(e)}'
        traceback_msg = traceback.format_exc()
        error_message += f"\n\nTraceback:\n{traceback_msg}"
        return error_message
