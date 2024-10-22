rm -rf dist
mkdir dist
cp -a django_app dist/
# pyarmor gen -r --exclude "manage.py" -O dist django_app
pyarmor gen -r --exclude "django_app/temporal" -O dist django_app
mv dist/pyarmor_runtime_000000 dist/django_app/pyarmor_runtime_000000

# cat dist/django_app/manage.py

# now take the django_app and place it in the appropriate place
