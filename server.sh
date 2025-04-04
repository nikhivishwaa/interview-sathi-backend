rm -rf prompt-eval-platform/
git clone https://github.com/nikhivishwaa/prompt-eval-platform.git -b dev-api
cd prompt-eval-platform/
cp -r . ../projectdir/
cd ../projectdir/

source env/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver


deactivate
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx