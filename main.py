import re
import requests
import user_agent
import telebot
from urllib.parse import quote
user = user_agent.generate_user_agent()
r = requests.Session()

API_TOKEN = "6893534253:AAGsBnAk49VFL1F27wdDYNbAhUy-rn6prwE"
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Please send your file 📁")

@bot.message_handler(content_types=['document'])
def analyze_links(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('links.txt', 'wb') as new_file:
            new_file.write(downloaded_file)

        with open('links.txt', 'r') as f:
            for line in f:
                url = line.strip()
                mainurl = quote(url, safe='')
                headers = {
                    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
                }
                response = requests.get(f'https://builtwith.com/?{mainurl}', headers=headers)

                result_message = "❛ ━━━━･⌁ 𝙅Ú𝙉𝙄𝙊𝙍🇧🇷⌁･━━━ ❜\n"
                result_message += f"❁ 𝙎𝙄𝙏𝙀 ➜ {url}\n"

                if "Cloudflare" in response.text:
                    result_message += "❁ 𝘾𝙇𝙊𝙐𝘿𝙁𝙇𝘼𝙍𝙀🛡️ ➜ ✅\n"
                else:
                    result_message += "❁ 𝘾𝙇𝙊𝙐𝘿𝙁𝙇𝘼𝙍𝙀🛡️ ➜ ❌\n"

                if any(captcha in response.text for captcha in ["CAPTCHA", "reCAPTCHA", "eCAPTCHA"]):
                    result_message += "❁ 𝘾𝘼𝙋𝙏𝘾𝙃𝘼🔁 ➜ ✅\n"
                else:
                    result_message += "❁ 𝘾𝘼𝙋𝙏𝘾𝙃𝘼🔁 ➜ ❌\n"

                if "❁ 𝘾𝘼𝙋𝙏𝘾𝙃𝘼🔁 ➜ ❌\n" in result_message and "❁ 𝘾𝙇𝙊𝘼𝙍𝙀🛡️ ➜ ❌\n" in result_message:
                    result_message += "❁ CLEANED\n"

                headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-GB,en;q=0.9',
    'cache-control': 'no-cache',
    'user-agent': user,
                }

                response = r.get('https://cmsdetect.com/', headers=headers)
                tok = re.search(r'input name="_token" type="hidden" value="(.*?)"', response.text).group(1)

                headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-GB,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'user-agent': user,
                }

                data = {
    '_token': tok,
    'url': url,
                }

                response = r.post('https://cmsdetect.com/', cookies=r.cookies, headers=headers, data=data)
                res = response.text
                platform = re.search(r'target="_blank">([^"]+)</a>', res).group(1).split('Try out')[1]
                result_message += f"❁ 𝙋𝙇𝘼𝙏𝙁𝙊𝙍𝙈➜ {platform}\n"
                
                    

                result_message += "❁ 𝙃𝙏𝙏𝙋_𝙎𝙏𝘼𝙏𝙐𝙎 ➜ 🟢𝟮𝟬𝟬🟢\n"
                result_message += "❁ 𝘿𝙀𝙑 ➜ @JR_HERO\n"
                result_message += "❛ ━━━━･⌁ 𝙃𝙀𝙍𝙊🇧🇷⌁･━━━ ❜\n"

                bot.reply_to(message, result_message)

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

bot.polling()
