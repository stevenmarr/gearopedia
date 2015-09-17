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
	sudo git clone 
	


		
		 
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

