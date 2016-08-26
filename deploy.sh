#!/bin/bash
# flask web service deploy script
appname=flask-service
srcdir=/usr/local/src
appdir=/var/www/$appname
confdir=/etc/apache2/sites-available
confpath=$confdir/$appname.conf
reqsname=requirements.txt
servname=service.py
wsgipath=$appdir/wsgi.py
venv=venv

apt-get update
apt-get install -y apache2 gnupg
apt-get install -y libapache2-mod-wsgi python-dev python-pip python-virtualenv

a2enmod wsgi
mkdir $appdir
cd $appdir
cp $srcdir/$servname $appdir

virtualenv $venv
source $venv/bin/activate
pip install -r $srcdir/$reqsname
deactivate

cat >$confpath <<EOL
<VirtualHost *:80>
    WSGIScriptAlias / $wsgipath
    <Directory $appdir>
        Order allow,deny
        Allow from all
    </Directory>
</VirtualHost>
EOL

cat >$wsgipath <<EOL
#!/usr/bin/python
import sys

sys.path.insert(0, '$appdir')
sys.path.append('$appdir/$venv/lib/python2.7/site-packages')

from service import app as application
EOL

a2ensite $appname
a2dissite 000-default
service apache2 restart