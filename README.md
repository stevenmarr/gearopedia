gearopedia
===================

A catalog of production equipment sorted into categories with user authentication

Getting started

0) Setup the enviroment
	
Download & install Virtual Box (https://www.virtualbox.org/wiki/Downloads), Vagrant (https://www.vagrantup.com/downloads)

create a new directory to run the project from like 
	~/catalog

clone the virual machine to /catalog
	git clone https://github.com/udacity/fullstack-nanodegree-vm.git
	
navigate to the directory, bootup the machine and login
	cd ~/catalog/fullstack-nanodegree-vm/vagrant
	sudo vagrant up
	sudo vagrant ssh

navigate to shared directory
	cd /vagrant/catalog
	
clone the project
	git clone 
	
	sudo pip install flask oauth2client sqlalchemy wtforms 

Install git
	
	sudo apt-get install git 
	
Create directory for catalog

	mkdir ~/catalog
	cd ~/catalog
	sudo git clone https://github.com/stevenmarr/gearopedia.git
	cd gearopedia
	
In order for authorization to work we must create a Google Developers Console project and client ID, instruction can be found here https://developers.google.com/identity/sign-in/web/devconsole-project.  After completing and downloading setup download the client_secretes.json file, open the file and copy the object.  In the terminal run:

	sudo nano ~/catalog/gearopedia client_secrets.json
	
Paste the contents from the clipboard into the file, save and exit. Next we will create the secrets.json file and populate its contents.

	sudo nano ~/catalog/gearopedia secrets.json

Paste the following objects in and fill in the constants, save and exit:

	{"app":{"secret_key":"SECRET_KEY"}}
	
Next we need to tweak our setting.py file for a local development enviroment, open the setting.py file
	
	sudo nano ~/catalog/gearopedia setting.py
	
Ucomment the lines with a *
	
	...
	#APPLICATION ********************
	APPLICATION_NAME = 'Gearopedia'
	#uncomment for development server 
	*#CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
	*#SECRET_KEY = json.loads(open('secrets.json', 'r').read())['app']['secret_key']
	...
	#DATA BASE ************************
	#uncomment for development server 
	*#DATA_BASE = 'sqlite:///gearopedia.db'
	...
	#FILES ***************************
	#uncomment for development server 
	*#UPLOAD_FOLDER = '~/catalog/files/uploads'
	*#UPLOAD_IMG_FOLDER = '~/catalog/files/img'
	...
	
Create the folder to host our files
	
	sudo mkdir ~/catalog/files
	sudo mkdir ~/catalog/files/img
	sudo mkdir ~/catalgo/files/uploads
	

	

1) Run the application
	download Vagrant

	python application.py

2) Navigate to homepage (localhost)

	http://localhost:8080

3) Login to enter/edit items (google accounts)
or
Click on categories to view items (read only)

API endpoints
	

	JSON:
	http://localhost:8080/json

Steven Marr
stevenmarr@me.com

