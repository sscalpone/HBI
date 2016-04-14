
rm -f database/mysite.db

python manage.py syncdb --noinput

rm -fr media
mkdir media
mkdir media/photos
mkdir media/documents

rm -fr database/db_merging
mkdir database/db_merging
rm -fr media/documents
mkdir media/documents
rm -fr csvs
mkdir csvs

python manage.py loaddata fixtures/admin_data.json
cp fixtures/me.png media/photos/
python manage.py loaddata fixtures/basic.json
