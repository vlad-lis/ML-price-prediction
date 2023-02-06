# Ironhack midterm project - Used cars price prediction

[Project's repository](https://github.com/vlad-lis/Ironhack-midterm)

## Members of the group:
* Markus Schmidt
* Vladislav Lis

## Goal of the project:
Creating a model to predict prices for used cards.

## Description of the dataset:
[Vehicle dataset](https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho) found on Kaggle.

The dataset has up to 14,828 rows spread over 4 csvs. Every csv has a different amount of columns, different header names and the data is formatted in a different style.
Columns range from 8 to 20 so we will most likely use 6 columns if there is not enough overlap.
After the EDA and data cleaning we will most likely have to drop some rows and columns in case we cannot use all of the rows because of the aformentioned situation.

## Planning:
* Day 1 - EDA:  
  * Getting insights from the data set;
  * Checking for outliers and anomalies;
  * Determining correlation between variables.
* Day 2 - Cleaning the data:
  * Removing null vales;
  * Correcting data types;
  * Checking for duplicates;
  * Filtering unwanted outliers.
* Day 3 - Transforming the data:
  * Scaling numerical features;
  * Encoding categorical features.
* Day 4 - Modelling:
  * Creating a model;
  * Testing the model;
  * Comparing predicted and test results;
  * Plotting test results.
* Day 5 - Presentation:
  * Presenting the model.


## Day 1 - EDA:
* EDA results included in the jupyter file;
* EDA plan for data preparation before concatenation described in [.xls file ](https://github.com/vlad-lis/Ironhack-midterm/blob/main/EDA_planning.xlsx):
![EDA plan](./EDAplan.png)