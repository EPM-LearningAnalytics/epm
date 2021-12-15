# epm: Main Package

This is the codebase for our project epm. We don't have a "main" function, and everything is contained within the submodule folders

## Module Descriptions:

The folders here are submodules that each have their own `init.py` file and can be called independently.

### 1. data_prep

* It includes two files `grades_prep.py` and `log_prep.py` that prepare datasets for building machine learning models.
* The `pickles` folder contains features and machine learning models pickled and ready for website embedment. 

### 2. graph

* It includes `graph_data.py` that prepares datasets for visualizations and `graph_fun.py` for plotting

### 3. modeling

* `ml_modeling.py` subsets certain number of important features and detects student behavior and groups students
* `review_alert.py` creates a dataframe that represents which sessions a student is recommended to review first before the final exam.
