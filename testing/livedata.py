import requests

url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"

querystring = {"Category": "soccer", "Timezone": "-7"}

headers = {
	"X-RapidAPI-Key": "e2be43c19dmsh510507d5ab1265bp1c72ddjsn2dbbfe871ab5",
	"X-RapidAPI-Host": "livescore6.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
