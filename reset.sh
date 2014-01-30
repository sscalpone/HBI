
rm -f database/mysite.db

python manage.py syncdb --noinput

python manage.py loaddata fixtures/admin_data.json 
python manage.py loaddata fixtures/basic.json 

