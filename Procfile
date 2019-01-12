% worker processes for bots
telegram-bot: sh -c 'cd telegram-bot && python main.py'
slack-bot: sh -c 'cd slack-bot && python slackbot.py'

% set up repository to deploy
release: sh -c 'cd decide && python manage.py migrate'

% launch decide in web process
web: sh -c 'cd decide && gunicorn decide.wsgi --log-file -' 