# Optical handwritten digits data

`digits.csv.gz` contains the 1,797 8×8 digit images distributed by scikit-learn's `load_digits`: 64 integer pixel features (0–16) and a class label (0–9) per row. These rows are a copy of the original UCI dataset's test subset. This example creates a new, explicitly documented train/validation/test split; its scores are **not the official UCI benchmark split**.

Dataset creators: E. Alpaydin and C. Kaynak. Citation: Alpaydin, E. & Kaynak, C. (1998). *Optical Recognition of Handwritten Digits*. UCI Machine Learning Repository. [DOI: 10.24432/C50P49](https://doi.org/10.24432/C50P49).

The dataset is distributed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), as stated on its [UCI dataset page](https://archive.ics.uci.edu/dataset/80/optical%2Brecognition%2Bof%2Bhandwritten%2Bdigits). The gzip file was copied without modification from the already installed scikit-learn data distribution; [load_digits documentation](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html) describes this subset. Dataset licensing is separate from nanoRSI's Apache-2.0 source code.
