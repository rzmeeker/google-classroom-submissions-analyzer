echo Please input this server's FQDN such as www.example.com:
read FQDN
echo Please input the FQDN again without www such as example.com:
read FQDNnoWWW
echo Please input the admin email contact for this server such as admin@domain.com:
read email

yum -y install httpd git openssl mod_ssl
systemctl start httpd
yum -y install mod_wsgi
systemctl restart httpd
pip3 install virtualenv
cd /var/www
git clone http://10.16.8.87/it/google-classroom.git gcs
cd gcs
sudo openssl req -newkey rsa:4096 -x509 -sha256 -days 3650 -nodes \
  -out /etc/pki/tls/certs/localhost.crt \
  -keyout /etc/pki/tls/private/localhost.key
wget -P /usr/local/bin https://dl.eff.org/certbot-auto
chmod +x /usr/local/bin/certbot-auto
openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
mkdir -p /var/lib/letsencrypt/.well-known
chgrp apache /var/lib/letsencrypt
chmod g+s /var/lib/letsencrypt
mv /var/www/gcs/letsencrpyt.conf /etc/httpd/conf.d/letsencrypt.conf
mv /var/www/gcs/ssl-params.conf /etc/httpd/conf.d/ssl-params.conf
systemctl reload httpd
/usr/local/bin/certbot-auto certonly --agree-tos --email $email --webroot -w /var/lib/letsencrypt/ -d $FQDNnoWWW -d $FQDN
mv /var/www/gcs/gcs.conf /etc/httpd/conf.d/$FQDNnoWWW.conf
sed -i "s/ example.com/$FQDNnoWWW/g" /etc/httpd/conf.d/$FQDNnoWWW.conf
sed -i "s/www.example.com/$FQDN/g" /etc/httpd/conf.d/$FQDNnoWWW.conf
systemctl restart httpd

cd /var/www/gcs
source bin/activate
pip install requirements.txt

systemctl restart httpd