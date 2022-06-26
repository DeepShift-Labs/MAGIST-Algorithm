# MAGIST-Algorithm
Multi-Agent Generally Intelligent Simultaneous Training Algorithm for Project Zeta!
![Github Banner(1)](https://user-images.githubusercontent.com/85193239/171949594-50a1f380-de26-4cd1-94d8-769a4c032455.png)

## Working Principal
Here is a flow diagram with the entire system drawn [here](https://lucid.app/documents/embeddedchart/6d04c807-0b77-495e-9b84-3abf38f32630).

### Data
The data is the most important element as the entire intelligence works around it. That is why it is important for the 
AI to process it and provide reasonable assumptions. There is another condition however: the algorithm, in its finished 
state, MUST be strictly Python code. This means no pretrained models or presets. It must find its own data and process it unsupervised. This structure is called a "semi-supervised" structure. Here, the data wil assume the following structure:

```
Object -> Common Associated Verbs, Synonyms, Events, Timestamps of usage, Nearby Objects, etc.
```

This is the "Who, What, When, Where, Why, How" of the data. This data can later be filtered and called apon when 
inferences are needed. To get here, however, the data must first be extacted from a single image. Since no pretrained 
models are allowed, here is the process to follow:

```
1. K-Means Clustering(find key objects in image) -> Discriminator for integrity check(see if clustering was performed well)
2. Reverse Image Search and Google Scraping(find label of image) -> Data Downloader(find dataset from large datasets)
3. Transfer Learn Model -> Object Detector
4. Get summary from internet sources like Wikipedia; location from LiDAR(future); user from facial detection(future); etc.
5. Store all the data in the NeuralDB
```

### Natural Language Processing
Another key stage of this AGI(Artificial General Intelligence) is the huaman interaction and understanding. MAGIST will constantly listen to conversations and make intelligent decisions. Here is the target process:

```
1. Record audio data and transcribe it(this is ***the only*** place where a pretrained model(the transcriber) is used since learning a human language fully unsupervised is incredibly arduous.
2. Use a custom positional embedding with a Self-Attention head to find key words.
3. Search these terms in the NeuralDB for possible entries.
4. Search unknown terms online and store defenitions for future reference. (future)
5. Extract key terms from matching entries. (future)
6. Insert those key terms to a text transformer trained on the collected NeuralDB data to generate a prediction. (future)
7. Utter the prediction. (future)
```

***

## Usage
This project is still under development. Please contact me at [krishna.shah@deepshift.dev]() if you want immediate access and/or support
to MAGIST. Once the algorithm is in a stable state, I will release a Python Package on PYPI and Github for access. There 
will also be documentation with more instructions.

***

## Installation
This project has many dependencies. Most can be installed using `pip`. Some require OS-level package managers. This is 
going to work best in Linux-based systems.

***These instruction are for Linux-based systems. In particular for Ubuntu 20.04 LTS based operating systems. Other 
systems may have errors that will require debugging.***

### Linux (Ubuntu-based Systems)
First install `Python 3` and `pip`:
```commandline
sudo apt install python3 python3-dev python3-pip
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
Next, we need to install MongoDB. This is a database that MAGIST uses to store its data. Please go to the 
[MongoDB Website](https://www.mongodb.com/) and follow the instructions to install it. We have more instructions in the 
[documentation](https://github.com/DeepShift-Labs/MAGIST-Algorithm/tree/main/docs).



Next, create a Python environment. There are 2 ways to do this: Anaconda or VEnv.

#### Anaconda
First install Anaconda from https://www.anaconda.com/.

Make the Anaconda environment:
```commandline
conda create --name myenv
```
Activate the environment in your current console. Note: You will have to do this every time you want to run MAGIST.
```commandline
conda activate myenv
```
Get the latest MAGIST Wheel from our [releases page](https://github.com/DeepShift-Labs/MAGIST-Algorithm/releases)!

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
Get the latest MAGIST Wheel from our [releases page](https://github.com/DeepShift-Labs/MAGIST-Algorithm/releases)!

Install MAGIST:
```commandline
pip3 install MAGIST-Algorithm-x.x.x-py3-none-any.whl
```

**Congratulations! You are all setup to script and use MAGIST**

***

## Contributing
Your contribution, monetary or programmatically, is crucial for the rapid development of the algorithm and its training. 
Please consider contributing. Even the smallest change to my README will be greatly appreciated.

### Project Zeta
We are building a fully biomimetic robot dog to implement MAGIST into. This will serve as the gateway between the AI and the physical world. 

[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=DeepShift-Labs&repo=Project-Zeta)](https://github.com/DeepShift-Labs/Project-Zeta)

***

# Disclaimer
Artificial Intelligence is a powerful field **meant only for research and study**, and it should be kept that way. Unethical use of the AI can have severe repercussions to society and to the perpetrator. DeepShift Labs and any programs it develops are strictly for research purposes. Hence, all of our products, MAGIST included, are to be used **strictly** for research purposes. Misuse of this program can lead to heavy fines and prosecution.
Furthermore, to retitle, rebrand, or redistribute without **explicitly** crediting DeepShift Labs is illegal. 
