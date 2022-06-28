# Welcome
We are thrilled that you have shown interest in the MAGIST project. We are currently in the process of building the
MAGIST. As a result, there might be issues or bugs that you encounter. If you encounter any issues, please post a issue
on the MAGIST Github repository. We will try to resolve them as soon as possible. If you have a solution to the issue,
you may create a pull request and we will review it as soon as possible. With that out of the way, let's get started!

## How it works?
We are using a powerful technique that combine the decades of research brilliant researchers have done. We are using a
multi-agent approach to intelligently process real-world data and learn off of it. To understand this, however, it is
crucial to understand how we define general intelligence, as there are major discrepancies from source to source.

### Our Goal
General intelligence is the ability of a machine to automatically acquire and train itself on a vast variety of knowledge that it may acquire from any source. It must also be able to make new predictions on the data upon inquisition (direct or indirect). This machine may not start with any pre-trained models, data, etc.

## Setup
MAGIST is a complex project, so a clean and efficient work space is essential. The entirety of this project was made in
the following environment:

 * PyCharm Professional
 * Python 3.10.4
 * [Anaconda Environment](https://www.anaconda.com/)
 * [Firefox Headless](https://www.mozilla.org/en-US/firefox/headless/)

Replicating this environment is crucial for stability and performance.

## Complete Installation Guide

This project has many dependencies. Most can be installed using `pip`. Some require OS-level package managers.

***These instruction are for Linux-based systems. In particular for Ubuntu 20.04 LTS based operating systems. Other
systems may have errors that will require debugging.***

### Linux (Ubuntu-based Systems)
First install `Python 3` and `pip`:
```commandline
sudo apt python3 python3-dev python3-pip
```
Next, we need to install Firefox and its corresponding `geckodriver` for headless Selenium searches:
```commandline
sudo apt install firefox
```

**Note:** If you get an error regarding the geckodriver, you can install it manually by following the instructions
[here](https://github.com/mozilla/geckodriver).

#### Install System Packages
Next, we need to install the system packages that MAGIST uses.
```commandline
sudo apt install python3-pyaudio
sudo apt install libasound-dev
```

#### MongoDB
Next, we need to install MongoDB. This is a database that MAGIST uses to store its data.
```commandline
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
```

If you get an error with the command above, you need to install `gnupg` and then reimport the key.
```commandline
sudo apt install gnupg
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
```

Next, we need to make the list file:
```commandline
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
```

Reload the package list:
```commandline
sudo apt update
```

Finally install MongoDB:
```commandline
sudo apt install mongodb-org
```

Next, create a Python environment. There are 2 ways to do this: Anaconda or VEnv.

#### Anaconda
First install Anaconda from https://www.anaconda.com/. You will need to download the latest installer and then run the following commands:
```commandline
sudo chmod +x Anaconda3-xxxx.xx-Linux-x86_64.sh
./Anaconda3-xxxx.xx-Linux-x86_64.sh
```

Close and reopen **all** terminal windows.

Make the Anaconda environment:
```commandline
conda create --name myenv
```
Activate the environment in your current console. Note: You will have to do this every time you want to run MAGIST.
```commandline
conda activate myenv
```
Install MAGIST:
```commandline
pip3 install MAGIST-Algorithm-x.x.x-py3-none-any.whl
```

#### VEnv
Make the environment in a designated location.
```commandline
python3 -m venv /path/to/new/virtual/environment
```
To activate it, you must travel to that `path/bin/` and then run:
```commandline
source activate
```
Install MAGIST:
```commandline
pip3 install MAGIST-Algorithm-x.x.x-py3-none-any.whl
```

**Congratulations! You are all setup to script and use MAGIST**

## Enterprise Setup

Future versions of MAGIST will come with ElasticSearch as a powerful search-alternative to MongoDB. The setup is a lot harder involving a seperate server and more powerful computer hardware. A future section of this Wiki will cover Enterprise setup. 
