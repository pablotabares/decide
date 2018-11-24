TOKEN = "711487599:AAGtMvo4S02ZxLvZ2-l-avTLngJ6MNZ7-Hg"
NAME = "Decide Ortosia"
WEBHOOK = False
## The following configuration is only needed if you setted WEBHOOK to True ##
IP = '0.0.0.0'
PORT = 80
URL_PATH = TOKEN # This is recommended for avoiding random people making fake updates to your bot
WEBHOOK_URL = 'https://example.com/%s' % (URL_PATH,)