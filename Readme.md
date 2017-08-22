# Pi Pre Config

piPreConfig.py is a small python v3 script that helps you quicky create files needed to get your RaspberryPi configured before the first boot.

Many people want to use the RaspberryPi in a headless configuration without monitor or keyboard, and some people don't realize that by adding certain configuration files and editing others in the boot partition of the SD card will allow you to enable your wifi and ssh server so you can log in for the first time.

This script will ask you a series of questions, based on the answers it will generate the files necessary to get your RaspberryPi configured quickly.  Prior to running this script make sure you have created a bootable microSD card with Rasbpian on it.  This has been tested with 2017-07-05-raspbian-jessie-lite, but should work for most Raspbian images.

This script requires python questionnaire library

To Install:
```
pip install questionnaire
```


To Run:
```
python piPreConfig.py
```

Once you have answered all the questions, there will be 1-3 files in the output directory.  Insert your microSD card into your computer and copy those 3 files to the microSD partition named "boot".

Once the files are copied over eject the microSD card and put it back into your RaspberryPi and boot.  If you enabled wifi and ssh in the questionaire then you should be able to ssh into the RaspberryPi as the default user.  If you enabled i2c, i2s, or spi those should be available to you now.

Notice:  Use this software at your own risk.  I am not responsible for any of the outcomes.

License: You are free to use, and free to modify.  You may not sell this or modified versions commercially.