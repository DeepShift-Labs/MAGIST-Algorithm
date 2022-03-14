# MAGIST-Algorithm
Multi-Agent Generally Intelligent Simultaneous Training Algorithm for Project Zeta

## Working Principal
Here is a flow diagram with the entire system drawn:
![image](https://user-images.githubusercontent.com/85193239/158191842-c66549ca-b432-4051-86f5-1501fef8804d.png)

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
