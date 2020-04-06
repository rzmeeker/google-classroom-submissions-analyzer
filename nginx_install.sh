#!/usr/bin/env bash
#nginx version
creds=/home/gcs/credentials.json
if test -f "$creds"
then
    echo "Credentials Found"
else
    echo "Credentials not found! Please download credentials to /home/gcs/credentials.json!"
    exit 1
fi
#user input
echo Please input this servers FQDN such as www.example.com:
read FQDN
echo Please input the FQDN again without www such as example.com:
read FQDNnoWWW
echo Please input the admin email contact for this server such as admin@domain.com:
read email

#firewall
firewall-cmd --add-port=80/tcp --permanent
firewall-cmd --add-port=443/tcp --permanent
firewall-cmd --reload

#install nginx and required utils
yum -y install nginx git openssl mod_ssl
systemctl start nginx
systemctl enable nginx

#create virtualenv
pip3 install virtualenv
cd /var/www
git clone https://github.com/rzmeeker/google-classroom-submissions-analyzer gcs
virtualenv --python=python3 gcs
cd /var/www/gcs
source bin/activate
pip install -r requirements.txt
mv /home/gcs/credentials.json /var/www/gcs/credentials.json

#generate SSL cert
sudo openssl req -newkey rsa:4096 -x509 -sha256 -days 3650 -nodes \
  -out /etc/pki/tls/certs/localhost.crt \
  -keyout /etc/pki/tls/private/localhost.key
wget -P /usr/local/bin https://dl.eff.org/certbot-auto
chmod +x /usr/local/bin/certbot-auto
openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
mkdir -p /var/lib/letsencrypt/.well-known
chgrp nginx /var/lib/letsencrypt
chmod g+s /var/lib/letsencrypt
mkdir /etc/nginx/snippets
mv /var/www/gcs/letsencrypt.conf /etc/nginx/snippets/letsencrypt.conf
mv /var/www/gcs/ssl-params.conf /etc/nginx/snippets/ssl.conf


if [ "$FQDN" == "$FQDNnoWWW" ]; then
    mv /var/www/gcs/nginx_letsencrypt_sameurl.conf /etc/nginx/conf.d/$FQDNnoWWW.conf
    sed -i "s/example.com/$FQDNnoWWW/g" /etc/nginx/conf.d/$FQDNnoWWW.conf
    systemctl restart nginx
    systemctl reload nginx
    /usr/local/bin/certbot-auto certonly --agree-tos --email $email --webroot -w /var/lib/letsencrypt/ -d $FQDNnoWWW
else
    mv /var/www/gcs/nginx_letsencrypt.conf /etc/nginx/conf.d/$FQDNnoWWW.conf
    sed -i "s/www.example.com/$FQDN/g" /etc/nginx/conf.d/$FQDNnoWWW.conf
    sed -i "s/example.com/$FQDNnoWWW/g" /etc/nginx/conf.d/$FQDNnoWWW.conf
    systemctl restart nginx
    systemctl reload nginx
    /usr/local/bin/certbot-auto certonly --agree-tos --email $email --webroot -w /var/lib/letsencrypt/ -d $FQDNnoWWW -d $FQDN
fi
#disable selinux because I haven't figured out how to not make that break everything yet
#If you see this comment and know how to fix it please submit a pull request
setenforce 0
sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config



###################
#Actual NGINX and uwsgi config
###################
mv /var/www/gcs/app.service /etc/systemd/system/app.service
mkdir /var/log/uwsgi/
touch /var/log/uwsgi/app.log
chown -R nginx:nginx /var/log/uwsgi/
systemctl start app
systemctl enable app
###MAKE NGINX CONFIG CHANGE
mv -f /var/www/gcs/nginx.conf /etc/nginx/nginx.conf
sed -i "s/example.com/$FQDNnoWWW/g" /etc/nginx/nginx.conf

#####################
chown -R nginx:nginx /etc/letsencrypt/live/$FQDNnoWWW
systemctl reload nginx
systemctl restart nginx


###########
#GUI REQUIRED!
#Authenticating webapp with gsuite account
###########

chown -R gcs:gcs /var/www/gcs
su -s /bin/bash -c "python auth.py" -g gcs gcs
chown -R nginx:nginx /var/www
cd /var/www/gcs
source bin/activate
pip install uwsgi
systemctl restart app
systemctl restart nginx

