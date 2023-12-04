if ! [[ "18.04 20.04 22.04 23.04" == *"$(lsb_release -rs)"* ]];
then
    echo "Ubuntu $(lsb_release -rs) is not currently supported.";
    exit;
fi

curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo apt-get install -y unixodbc-dev


cd ~/HomeEasy/
git pull
sudo rm -r /var/www/HomeEasy-API/
sudo cp -r ~/HomeEasy/API_Service /var/www/HomeEasy-API/

cd /var/www/HomeEasy-API

sudo python3 -m venv venv
source venv/bin/activate
sudo pip install -r requirements.txt

# sudo nano /etc/apache2/sites-available/api.hartzlerhome.solutions.conf
sudo cp ./api.hartzlerhome.solutions.conf /etc/apache2/sites-available/api.hartzlerhome.solutions.conf
sudo a2ensite api.hartzlerhome.solutions.conf

sudo chown -R www-data:www-data ./


sudo service apache2 restart