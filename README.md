# lexi
**Language Explorer with eXtenstive Inventories**

This repository allows users to compare and contrast languages, analyze phonemic patterns, and more. The underlying data is provided by the PHOIBLE dataset (cited below). 

![Phonemic Comparison of English and Spanish](https://github.com/calebmcarr/lexi/blob/main/data/images/eng_esp_comp.png) ![Transition Probabilities of Bigrams in The Declaration of Independence](https://github.com/calebmcarr/lexi/blob/main/data/images/transitionProbs.png)

### Setup

1. Download the PHOIBLE dataset

```
cd lexi
curl -s -o phoible-v2.0.zip 'https://zenodo.org/records/2593234/files/cldf-datasets/phoible-v2.0.zip?download=1'
```

2. Unzip the dataset

```
unzip phoible-v2.0.zip
```

3. Clean up and rename

```
rm phoible-v2.0.zip
mkdir data
mv cldf-datasets-phoible-350563f data/phoible
```

4. Install python dependencies

```
pip3 install -r requirements.txt
```

### Citations & Licensing

The PHOIBLE dataset used here is cited as:

> "Moran, Steven & McCloy, Daniel (eds.) 2019.
PHOIBLE 2.0.
Jena: Max Planck Institute for the Science of Human History.
(Available online at http://phoible.org, Accessed on 2023-12-19.)"

Language Explorer with eXtenstive Inventories © 2023 by Caleb Carr is licensed under CC BY-SA 4.0 
