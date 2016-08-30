#!/bin/bash
# flask web service deploy script
appname=flask-service
srcdir=/usr/local/src
appdir=/var/www/$appname
confdir=/etc/httpd/conf.d
confpath=$confdir/$appname.conf
reqsname=requirements.txt
servname=service.py
wsgipath=$appdir/wsgi.py
venv=$appdir/venv

yum update -y
yum install -y gcc gnupg python27-devel python27-pip python27-virtualenv
yum install -y httpd24 mod24_wsgi-python27

mkdir $appdir
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
sys.path.append('$venv/lib/python2.7/site-packages')

from service import app as application
EOL

chkconfig httpd on
service httpd start