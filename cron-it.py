import requests

bot_token = "6239024779:AAFPw7dtxvhb7Q_EDAQAeCwCYxUauLhL3_8"
chat_id = "-1001874835620"

command = 'Please use /prijs to get the new charts'

url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={command}"
response = requests.get(url)
print(response.json())
