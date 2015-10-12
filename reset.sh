
rm -f database/mysite.db

python manage.py syncdb --noinput

rm media/photos/*
rm media/documents/*

python manage.py loaddata fixtures/admin_data.json
cp fixtures/me.png media/photos/
python manage.py loaddata fixtures/basic.json 

