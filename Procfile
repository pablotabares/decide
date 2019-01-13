% set up repository to deploy
release: sh -c 'cd decide && python manage.py migrate'

% launch decide in web process
web: sh -c 'cd decide && gunicorn decide.wsgi --log-file -' 