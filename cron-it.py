import requests

bot_token = 'BOT_TOKEN'
chat_id = 'CHAT_ID'

command = 'Please use /prijs to get the new charts'

url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={command}"
response = requests.get(url)
print(response.json())
