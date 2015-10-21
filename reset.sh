
rm -f database/mysite.db

python manage.py syncdb --noinput

rm -fr media/photos
mkdir media/photos
rm -fr media/documents
mkdir media/documents

python manage.py loaddata fixtures/admin_data.json
cp fixtures/me.png media/photos/
python manage.py loaddata fixtures/basic.json
