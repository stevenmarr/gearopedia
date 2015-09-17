gearopedia
===================

A catalog of production equipment sorted into categories with user authentication

Getting started

0) Setup the enviroment
	
Download & install Virtual Box (https://www.virtualbox.org/wiki/Downloads), Vagrant (https://www.vagrantup.com/downloads)
then from the terminal navigate to home folder and run

		mkdir catalog
		cd catalog
		vagrant init ubuntu/trusty64
		vagrant up

after bootup

		vagrant ssh 
		
First we we update the virual machine (this should be done at each boot-up

	sudo apt-get update
	sudo apt-get upgrade
	
Now we will install the software on our virtual machine necessary to install the python packages to run our web app

	sudo apt-get install python-pip

Install python libraries needed for app to run
	
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
	
Next we need to tweak our setting.py file for a local development enviroment, uncomment the following lines from settings.py
	
	


	


	


		
		 
	clone the repo https://github.com/udacity/fullstack-nanodegree-vm.git where you will be running the application from [APP_DIRECTORY]

	navigate to [APP_DIRECTORY] clone the repo:
	https://github.com/stevenmarr/gearopedia.git
	Setup the enviroment

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

