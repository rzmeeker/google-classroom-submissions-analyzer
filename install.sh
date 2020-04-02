echo Please input this servers FQDN such as www.example.com:
read FQDN
echo Please input the FQDN again without www such as example.com:
read FQDNnoWWW
echo Please input the admin email contact for this server such as admin@domain.com:
read email

firewall-cmd --add-port=80/tcp --permanent
firewall-cmd --add-port=443/tcp --permanent
firewall-cmd --reload

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
mv /var/www/gcs/letsencrypt.conf /etc/httpd/conf.d/letsencrypt.conf
mv /var/www/gcs/ssl-params.conf /etc/httpd/conf.d/ssl-params.conf
sed -i "s/ example.com/$FQDNnoWWW/g" /var/www/gcs/challenge-server.conf > /var/www/gcs/challenge-server.conf.tmp
sed -i "s/www.example.com/$FQDN/g" /var/www/gcs/challenge-server.conf.tmp > /etc/httpd/conf.d/$FQDNnoWWW.conf
rm /var/www/gcs/challenge-server.conf.tmp
systemctl reload httpd
/usr/local/bin/certbot-auto certonly --agree-tos --email $email --webroot -w /var/lib/letsencrypt/ -d $FQDNnoWWW -d $FQDN
cp /var/www/gcs/gcs.conf /etc/httpd/conf.d/$FQDNnoWWW.conf.example
sed -i "s/ example.com/$FQDNnoWWW/g" /etc/httpd/conf.d/$FQDNnoWWW.conf.example | tee /etc/httpd/conf.d/$FQDNnoWWW.conf.tmp
sed -i "s/www.example.com/$FQDN/g" /etc/httpd/conf.d/$FQDNnoWWW.conf.tmp | tee /etc/httpd/conf.d/$FQDNnoWWW.conf
rm /etc/httpd/conf.d/$FQDNnoWWW.conf.tmp
systemctl restart httpd

setenforce 0


cd /var/www
virtualenv --python=python3 gcs
cd /var/www/gcs
source bin/activate
pip install -r requirements.txt

chown -R apache:apache /var/www
systemctl restart httpd