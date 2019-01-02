psql -c "create user decide with password 'decide'"
psql -c "create database decide owner decide"
cd docker/decide
cp heroku_settings.py local_settings.py
python manage.py migrate
