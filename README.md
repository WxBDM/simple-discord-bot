# SDB - Simple Discord Bot
Creating a Discord bot is, to put it simply, hard. The purpose of this repository is supposed to give you a "bare bones" workable discord bot "out of the box". It is designed to be lightweight and demonstrate how to construct a Discord bot. Note that all of the installation information is not currently here. This will come in a future version.

## Installation
**It is highly recommended to use a virtual environment.** See [here](https://docs.python.org/3/library/venv.html) on how to create a virtual environment using venv. To install, clone the repository. This is not installed using pip, as it is not a package.

## Dependencies
All dependencies can be found in the `requirements.txt` file in the repository. Below is a partial list:

 - aiohttp==3.7.4.post0 
 - async-timeout==3.0.1 
 - asyncio==3.4.3
 - discord==1.0.1 

## Secret Key
You must have a secret key in order for your bot to work. This can be found in the Discord Developer's Dashboard. It is **highly** recommended to hide this secret key in the environmental variables in your computer (note that this bot checks the environmental variables for the secret key).

