cd ~/HomeEasy/
git pull
sudo cp -r ~/HomeEasy/API_Service /var/www/HomeEasy-API

cd /var/www/HomeEasy-API

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# sudo nano /etc/apache2/sites-available/api.hartzlerhome.solutions.conf
sudo cp ./ /etc/apache2/sites-available/api.hartzlerhome.solutions.conf
sudo a2ensite api.hartzlerhome.solutions.conf

sudo chown -R www-data:www-data ./


sudo service apache2 restart