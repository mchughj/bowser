
# Bowser

This is a simple mechanism to build a centralized redirection service that is easy to augment.  Something like this has existed in various forms notably yubnub and bunny1.  When I worked at Facebook every engineer (and most employees as well) used a system called 'bunnylol' (which was historically based off of bunny1 in some way) every single day.  As part of the first day of onboarding you set this up.  I've missed the capabilities and the idea behind it so replicating here.

The system is called 'bowser' for three reasons.  

## Getting started

I'm going to document here the commands used in Ubuntu in order to get things running.In the below if your default 'python' is python3 then change the below commands to just be 'python'.

1. Install necessary prerequisites
   ```
   sudo apt install -y python3
   python3 -m pip install --user --upgrade pip
   python3 -m pip install --user virtualenv
   ```
1. Create a new virtual environment within the same directory as the git checkout.
   ```
   python3 -m virtualenv --python=python3 env
   ```
1. Activate the new virtual environment
   ```
   source env/bin/activate
   ```
1. Install, into the new virtual environment, the required python modules for this specific environment.  This will be installed within the virtual env which was activated earlier.
   ```
   python3 -m pip install -r requirements.txt
   ```
1. Finally, start the server process here
   ```
   python3 server.py
   ```
   Under the covers this repo uses flask as the webserver but it is advised to not use the flask executable - this won't pick up the necessary dependencies and you will be forced to install the requirements outside of the virtual env as well as inside of it.

## Using the server

Go to http://[deployment host:port]/install and follow the instructions for making this your default search engine.

## Running the server as a systemd process 

If you want this to be automatically run and managed by systemd then use the 'install' script.

```
./install.sh
```

From this point forward the services will be restarted automatically on startup of the Linux box.  To see the logs use the ./showLogs.sh.  Other useful control scripts are also created.


