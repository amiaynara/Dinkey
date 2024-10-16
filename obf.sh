rm -rf dist
mkdir dist
cp -a django_app dist/
pyarmor gen -O dist -r django_app
mv dist/pyarmor_runtime_000000 dist/django_app/pyarmor_runtime_000000

# now take the django_app and place it in the appropriate place