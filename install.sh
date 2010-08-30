#!/usr/bin/env bash
aptitude install screen
aptitude install rabbitmq-server
aptitude install libjpeg
aptitude install libpng3
aptitude install git-core
aptitude install python-pip
aptitude install python-virtualenv
aptitude install nginx
aptitude install upstart

apt-get install binutils libgdal1-1.5.0 postgresql-8.3-postgis postgresql-server-dev-8.3 python-psycopg2 python-setuptools
useradd wluw -m -s/bin/bash

scp chris.dickinson@unbearablecomics.com:~/wluw/backup.psql ./
scp chris.dickinson@unbearablecomics.com:~/wluw/usr.tar.gz ~wluw/usr.tar.gz
scp chris.dickinson@unbearablecomics.com:~/wluw/local_settings.py ~wluw/local_settings.py

POSTGIS_SQL_PATH=/usr/share/postgresql-8.3-postgis
createdb -E UTF8 template_postgis # Create the template spatial database.
createlang -d template_postgis plpgsql # Adding PLPGSQL language support.
psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';"
psql -d template_postgis -f $POSTGIS_SQL_PATH/lwpostgis.sql # Loading the PostGIS SQL routines
psql -d template_postgis -f $POSTGIS_SQL_PATH/spatial_ref_sys.sql
psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;" # Enabling users to alter spatial tables.
psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

createuser wluw -s
createdb -Uwluw -Ttemplate_postgis wluw
cat backup.psql | psql -Uwluw wluw 

echo '#!/usr/bin/env bash' > ~wluw/install.sh
echo 'git clone git@unbearablecomics.com:chris/wluw.git && cd wluw && virtualenv . && source bin/activate && pip install -E . -r pip_requirements.txt' >> ~wluw/install.sh
echo 'cp ~/local_settings.py wluw/local_settings.py'
echo 'wluw/manage.py syncdb && wluw/manage.py migrate' >> ~wluw/install.sh
echo 'tar zxfv ~/usr.tar.gz' >> ~wluw/install.sh

chown wluw:wluw ~wluw/local_settings.py
chown wluw:wluw ~wluw/install.sh
chown wluw:wluw ~wluw/usr.tar.gz

chmod +x ~wluw/install.sh

su wluw -c 'cd ~ && ./install.sh'

scp chris.dickinson@unbearablecomics.com:~/wluw/wluw_* /etc/init/
scp chris.dickinson@unbearablecomics.com:~/wluw/nginx_wluw /etc/nginx/sites-enabled/

start wluw_celery
start wluw_gunicorn
