
echo 'Starting tools '
cd ./tools/SCSS2DJ/ ; ./run.sh  & cd -
python manage.py  validate
python manage.py reset feedbackEngine  sample
python manage.py sql feedbackEngine  sample
python manage.py syncdb 
python manage.py runserver 0.0.0.0:7777