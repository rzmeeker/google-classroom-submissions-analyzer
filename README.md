# google-classroom-submissions-analyzer

Requirements: CentOS8 Server (might work on centos 7, but it assumes yum and firewalld exist). Public IP pointing at this server with ports 80 and 443 open in the firewall. DNS A record pointing at the hostname of this server.

To install, have an administrator account name gcs input the following commands:

cd /home/gcs
su root
yum -y install git
git clone https://github.com/rzmeeker/google-classroom-submissions-analyzer
cd google-classroom-submissions analyzer
chmod +x nginx_install.sh
./nginx_install.sh

And then follow the prompts in the installer.
