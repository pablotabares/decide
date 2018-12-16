% release: bash ./release-tasks.sh
% web: gunicorn decide.wsgi
% prepara el repositorio para su despliegue.
release: sh -c 'cd docker/decide && python manage.py migrate'
% especifica el comando para lanzar Decide
web: sh -c 'cd docker/decide && gunicorn decide.wsgi --log-file -'
