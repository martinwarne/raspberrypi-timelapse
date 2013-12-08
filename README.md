#Raspberry Pi Timelapse Camera with Dropbox Sync

This program is meant to be loaded onto the RaspberryPi which has the RaspberryPi camera attached to it. It can then be setup to run via a cron job to take pictures as often as you want.

##Setup

The instructions below are written as if you haven't installed anything on your Pi apart from the OS.

####Download

The best way to download the code is through git. To install git do

    sudo apt-get install git
    
Then you can download the code by running the following in the directory you want to download into

    git clone git@github.com:martmatwarne/raspberrypi-timelapse.git

####Requirements

The best way to install the requirements is through pip. To get pip if you don't already have it:

    sudo apt-get install python-setuptools
	sudo easy_install pip
    
then do

    pip install -r requirements.pip
    
 You'll also need avconv so do the following on the termainl
 
    sudo apt-get install libav-tools

####Dropbox program

You'll need to register with Dropbox to get app key and app secret values.

1. Go to https://www.dropbox.com/developers/apps
2. Select 'Create app'
3. Select 'Dropbox API app'
4. Select 'Files and datastores'
5. Select 'Yes My app only needs access to files it creates.'
6. Name it something
7. Save the app
8. Grab the app key and secret from the app page and enter them into settings.json

####Access Key

To sync with Dropbox you'll need to authenticate the program. This is the horrible bit of the setup and something I want to fix! But for now run the program

    python photo_taker.py

The output will then tell you the url you have to go to. Once you've authorised the app an access token will appear that you can type in. If this is done correctly then the program will be able to upload files to the Apps directory in your Dropbox. The program will then add it to data.json so you don't have to keep entering it.

####Set it up via a cron job

Ideally you want to run this script via cron. A guide to cron can be found here or just by googling

<a href="http://www.thegeekstuff.com/2009/06/15-practical-crontab-examples/">http://www.thegeekstuff.com/2009/06/15-practical-crontab-examples/</a>

##Output
The program produces two things. It produces a new picture everytime it runs and it regenerates the video to include the new picture.

##Authors

Martin Warne @martmatwarne

##Version

0.1 - Initial release, 02/12/2013

##TODO

* Fix it so when you git clone you don't get conflicts on the JSON files
* Make Dropbox authentication nicer
* Add other upload services
* Try and make the video encode remotely
* Add more options to configure images and the video
* Find a solution that isn't everyone creating their own Dropbox apps

