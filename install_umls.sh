################
# download UMLS
################

wget http://download.nlm.nih.gov/rxnorm/terminology_download_script.zip
sudo apt-get install unzip
sudo apt-get install s3cmd
s3cmd --configure

unzip terminology_download_script.zip
# Open curl-uts-download.sh and enter your UTS username and password
chmod 755 terminology_download_script/curl-uts-download.sh

# create download.sh
echo "sh ../terminology_download_script/curl-uts-download.sh http://download.nlm.nih.gov/umls/kss/2015AB/full/README.txt" > download.sh
echo "sh ../terminology_download_script/curl-uts-download.sh http://download.nlm.nih.gov/umls/kss/2015AB/full/Copyright_Notice.txt" >> download.sh
echo "sh ../terminology_download_script/curl-uts-download.sh http://download.nlm.nih.gov/umls/kss/2015AB/full/2015AB.CHK" >> download.sh
echo "sh ../terminology_download_script/curl-uts-download.sh http://download.nlm.nih.gov/umls/kss/2015AB/full/2015AB.MD5" >> download.sh
echo "sh ../terminology_download_script/curl-uts-download.sh http://download.nlm.nih.gov/umls/kss/2015AB/full/2015ab-1-meta.nlm" >> download.sh
echo "sh ../terminology_download_script/curl-uts-download.sh http://download.nlm.nih.gov/umls/kss/2015AB/full/2015ab-2-meta.nlm" >> download.sh
echo "sh ../terminology_download_script/curl-uts-download.sh http://download.nlm.nih.gov/umls/kss/2015AB/full/2015ab-otherks.nlm" >> download.sh
echo "sh ../terminology_download_script/curl-uts-download.sh http://download.nlm.nih.gov/umls/kss/2015AB/full/mmsys.zip" >> download.sh

mkdir umls
cd umls
bash ../download.sh
cd ..
s3cmd put -r umls s3://umls-bucket/

###############
# install UMLS
###############

cd umls
unzip mmsys.zip

# installing UMLS requires a GUI
# http://web.archive.org/web/20151223070938/http://stackoverflow.com/questions/25657596/how-to-set-up-gui-on-amazon-ec2-ubuntu-server
sudo apt-get update
sudo apt-get install ubuntu-desktop
sudo apt-get install vnc4server

vncserver
vncserver -kill :1

# http://web.archive.org/web/20151223073329/http://onkea.com/ubuntu-vnc-grey-screen/
# edit ~/.vnc/xstartup
vncserver

# open port 5901 in security group
# open vnc://54.183.115.13:5901
export DISPLAY=:1

# Source: /home/ubuntu/umls
# Destination: /home/ubuntu/umls-data
# Choose Database Load Scripts: Mysql 5.6
# Output Options -> Select database -> MySQL 5.6
# Level 0 + SNOMEDCT US
cd umls
bash ../download.sh

s3cmd put -r umls-data s3://umls-bucket/
