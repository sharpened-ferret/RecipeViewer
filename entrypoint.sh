nginx
python3 manage.py collectstatic
gunicorn --env DJANGO_SETTINGS_MODULE=RecipeViewer.settings --workers=2 -b=0.0.0.0:8000 RecipeViewer.wsgi