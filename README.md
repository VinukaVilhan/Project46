# Control

## Introduction

The name of the application is Control. The application controls the main functions such as shutting down, restarting, sleeping, and setting the Wi-Fi on/off at a given time.

This Desktop application works for Windows os based devices.

### The problem I wanted to solve

When downloading content from the internet we use time-based internet packages. Mostly, the package will be over at 8.30 in the morning. If you do not pause the downloading when the package is over your limited data from other data plans will be consumed and if you are not a morning person you probably have to wake up and pause the download manually.

### Solution

So, to solve this problem I made this app to turn off the wifi at a given time. So, as a not-so-much of a morning person, I don't have to wake up and do the pausing manually! :joy:

## Functionalities

I added some extra functionalities which could be useful.

- Shutdown Function
The Computer could be shut down at any given time.

- Restart Function
The computer could be restarted at any given time

- Sleep Function

- WIFI Off/On Function
The wifi adapter will be on/off according to a given time

 ![The interface of the application. Functions in order [shutdown, restart, sleep, wifi on, wifi off]](https://github.com/VinukaVilhan/Project46/assets/125667311/bb4e9749-0cef-4428-ad40-1fff3ee8e03c)


### Rules

1. *If an option such as shutdown, restart, or sleep operation is executed it will disable the other two options. You should abort the current execution to enable the other options*
Ex - If the shutdown command is executed restart and sleep options would be unavailable.

2. *If options such as shutdown, restart, or sleep operation are executed the wifi on or off time should be before the main operation execution time*
Ex - if restart command is executed, the time for turning wifi on or off should be before the main operation execution time.

## Important

1. *WIFI* - When the wifi is turned off it turns off the wifi adapter. Do not be afraid you can easily turn it back on using the wifi turn ON option. And it could be done immediately.
2. *VIRUS* - When executing the application you will encounter messages that say this application contains viruses. It's because the application demands admin right to execute commands such as shutdown, restart, etc but there are no viruses. Please, allow the application to work in your antivirus or Windows security.

  ![image](https://github.com/VinukaVilhan/Project46/assets/125667311/30e7f7f5-fce2-4e33-a089-96b11a5a736c)
  
3. Click on the threat and allow the app to make changes.

## How to get the application and use it?

Go to this link https://github.com/VinukaVilhan/Project46/releases/tag/v1.0.0 and download the `Control.exe` file and run it.

![image](https://github.com/VinukaVilhan/Project46/assets/125667311/cae585a9-7dc6-4ae4-ac62-b4caba913a49)


### Installation of the application in your code base

1. You can install the required packages using the command below

    >`pip install -r requirements.txt`

2. Go to the directory and execute this command to run the application
    >`python app.py`

    >`python app.py`
