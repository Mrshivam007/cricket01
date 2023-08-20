import time
from cricket import Cricket


def print_live_scores():
    cric = Cricket()
    previous_score = ""

    while True:
        score = cric.livescore()

        # Check if the score has changed
        if score != previous_score:
            print(score)
            previous_score = score

        time.sleep(10)  # Sleep for 10 seconds before fetching the score again


# Call the function to start printing live cricket scores
print_live_scores()
