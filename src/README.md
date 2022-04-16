# MAGIST-Algorithm
Multi-Agent Generally Intelligent Simultaneous Training Algorithm for Project Zeta

## Working Principal
Here is a flow diagram with the entire system drawn:
https://lucid.app/documents/embeddedchart/6d04c807-0b77-495e-9b84-3abf38f32630

### Data
The data is the most important element as the entire intelligence works around it. That is why it is important for the AI to process it and provide reasonable assumptions. There is another condition however: the algorithm, in its finished state, MUST be stricly Python code. This means no pretrained models or presets. It must find its own data and process it unsupervised. This structure is called a "semi-supervised" structure. Here, the data wil assume the following structure:

```
Object -> Common Associated Verbs, Synonyms, Events, Timestamps of usage, Nearby Objects, etc.
```

This is the "Who, What, When, Where, Why, How" of the data. This data can later be filtered and called apon when inferences are needed. To get here, however, the data must first be extacted from a single image. Since no pretrained models are allowed, here is the process to follow:

```
1. K-Means Clustering(find key objects in image) -> Discriminator for integrity check(see if clustering was performed well)
2. Reverse Image Search and Google Scraping(find label of image) -> Data Downloader(find dataset from large datasets)
3. Transfer Learn Model -> Object Detector
```

### Natural Language Processing
Another key stage of this AGI(Artificial General Intelligence) is the huaman interaction and understanding. MAGIST will use a Transformer chatbot to listen to conversations and simultaneously train on them. When it is queried, it will collect information from the database, and use the transformer to fit a response. This will be done by using a GAN system infused into the transformer. The transformer will act as the discriminator to perform an integrity check. 

## Usage
This project is still under development. Please contact me at [deepshiftlabs@outlook.com]() if you want immediate access to MAGIST. Once the algorithm is in a stable state, I will release a Python Package on PYPI and Github for access.


## Contributing
Your contribution, monetary or programmatically, is crucial for the rapid development of the algorithm and its training. Please consider contributing. Even the smallest change to my README will be greatly appreciated.
