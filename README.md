# tv-aficionado

# Requirements

## External Requirements
* TheTVDB

## System Requirements
* Python3 and Pip3
    * Install on Linux: ```sudo apt-get update && sudo apt-get install python3 python3-pip```
    * Install on MacOS:
        * First install `Homebrew`: ```/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"```
        * Then Python3 and Pip3: ```brew intall python3```.
* Django
    * Install on Linux and MacOS: ```pip3 install django```
* Selenium (on hosts running tests)
    * Install on Linux and MacOS: ```sudo pip3 install --upgrade selenium```
    * On Linux and MacOS, copy the webdriver binary in `/usr/local/bin`.

# TO DO
* Make a script to install the requirements
    * Look into the gists for the selenium drivers: https://gist.github.com/cgoldberg/4097efbfeb40adf698a7d05e75e0ff51