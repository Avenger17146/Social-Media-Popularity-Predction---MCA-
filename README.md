### About the directory structure

Dataset source : https://social-media-prediction.github.io/PredictionChallenge/datasets.html
The folder named "Captions And Word2vecs" has a modified version of "https://github.com/DeepRNN/image_captioning" which is used to generate PCA of last layer of CNN and word2vecs of the generated image captions.

"DeepGBM" is the model used to train the data which has been taken from "https://github.com/motefly/DeepGBM" and modified to match our dataset formats.

"Dataset Creation" contains the scripts for generating data in our folders by downloading it, preprocessing it, adding features to it, matching to remove null values.

main.py is our model which can be run by just running it as (it just requires the final prepared dataset to work on):
$ python main.py
[requirements will be provided in another text file]

Due to large size of datasets and huge time taken in upload of multiple such files on github. These files are at the host system itself.
