# -*- coding: utf-8 -*-
"""Calories Burnt Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z-u07g01rFezvTarBOJb1I8F7T-jAngM

# **Calories Burnt Prediction**

**Importing Libraries**
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
sns.set()
import warnings
warnings.filterwarnings('ignore')
import joblib
import pickle

"""**Data Loading and Reading**"""

#!pip install opendatasets

import opendatasets
dataset_url = 'https://www.kaggle.com/datasets/fmendes/fmendesdat263xdemos'
opendatasets.download(dataset_url)

calories_path = '/content/fmendesdat263xdemos/calories.csv'
exercise_path = '/content/fmendesdat263xdemos/exercise.csv'

# loading data from csv file to Pandas dataframe
calories_data = pd.read_csv(calories_path)
exercise_data = pd.read_csv(exercise_path)

exercise_data.head()

#make copies of the original dataset
excercise_copy = exercise_data.copy()
calories_copy = calories_data.copy()

#seperate a Calories column from calories_data and then append to exercise_data
target = calories_data['Calories']
exercise_data['Calories'] = target

exercise_data.head()

#shape of the dataset
exercise_data.shape

#columns of the datasets
exercise_data.columns

#information about the dataset
exercise_data.info()

#dtypes of the dataset
exercise_data.dtypes

# statistical information about numerical columns
exercise_data.describe()

#categorical column statistics
exercise_data.describe(include='object')

#checking for missing values
exercise_data.isnull().sum()

"""**Data Visualization**"""

# drop User_ID
exercise_data = exercise_data.drop('User_ID',axis=1)
exercise_data.head()

numerical_columns =list(exercise_data.select_dtypes(['int64','float64']).columns)
len(numerical_columns)

# visualizing numerical columns using boxplot,violinplot,histogram,kde,
def make_plot(plot_kind,numerical_columns):
  plot_func = {
      'violin':sns.violinplot,
      'box':sns.boxplot,
      'kde':sns.kdeplot,
      'hist': plt.hist
  }
  fig = plt.figure(figsize=(15,10))
  for index,column in enumerate(numerical_columns):
    axis = fig.add_subplot(3,3,index+1)
    if plot_kind not in ['hist','kde']:
      plot_func[plot_kind](y=exercise_data[column],ax=axis)
      plt.title(f'{plot_kind} plot for {column}')
    else:
      plot_func[plot_kind](exercise_data[column])
      plt.title(f'{plot_kind} plot for {column}')
  plt.tight_layout()
  plt.show()

#violinplot
make_plot('violin',numerical_columns)

# boxplot
make_plot('box',numerical_columns)

# barplot
make_plot('hist',numerical_columns)

# kde plot
make_plot('kde',numerical_columns)

#Gender
gender = exercise_data['Gender'].value_counts()
gender

#Gender Distributions
gender.plot(kind='bar')
plt.title('Distribution of Genders')
plt.show()

#Gender Distributions
gender.plot(kind='pie',autopct = '%.f%%')
plt.title('Distribution of Genders')
plt.show()

exercise_data.head()

#correlation_matrix
plt.figure(figsize=(10,8))
correlation = exercise_data.corr()
sns.heatmap(correlation,annot=True,fmt='.1f',cbar=True,cmap='Blues')
plt.show()

"""**Gender column label encoding**"""

exercise_data.replace({'Gender':{'male':0,'female':1}},inplace=True)

exercise_data.head()

# seperate features and target
features = exercise_data.drop('Calories',axis=1)
target = exercise_data['Calories']

# split the data into train,test 
train_data,test_data,train_labels,test_labels = train_test_split(features,target,test_size=0.2,random_state=3)

print(features.shape,train_data.shape,test_data.shape)

"""**Modeling**

**base model linear regression**
"""

linear_model = LinearRegression()
linear_model.fit(train_data,train_labels)

"""**Prediction on train_data**"""

linear_prediction = linear_model.predict(train_data)
linear_MAE = mean_absolute_error(train_labels,linear_prediction)
linear_r2_score = r2_score(train_labels,linear_prediction)
linear_MSE = mean_squared_error(train_labels,linear_prediction)
print('R2 score of linear model on training data is: ',linear_r2_score)
print('Mean squared error on training data is: ',linear_MSE)

linear_prediction

# prediction vs actual value on training data
linear_df = pd.DataFrame({'Actual':train_labels,'Prediction':linear_prediction})
linear_df.head(10)

"""**Prediction on test_data**"""

test_prediction = linear_model.predict(test_data)
linear_MAE = mean_absolute_error(test_labels,test_prediction)
test_r2_score = r2_score(test_labels,test_prediction)
test_MSE = mean_squared_error(test_labels,test_prediction)
print('R2 score of linear model on testing data is: ',test_r2_score)
print('Mean squared error on testing data is: ',test_MSE)

# prediction vs actual value on training data for testing data
test_df = pd.DataFrame({'Actual':test_labels,'Prediction':test_prediction})
test_df.head(10)

"""**Trying with many models**"""

models = [LinearRegression(),XGBRegressor(objective='reg:squarederror'),RandomForestRegressor(),DecisionTreeRegressor()]

results = []
def best_model(models):
  for model in models:
    model.fit(train_data,train_labels)
    prediction = model.predict(test_data)
    r2score = r2_score(test_labels,prediction)
    MSE = mean_squared_error(test_labels,prediction)
    results.append({
        'Model':str(model),
        'R2 Score':r2score,
        'Mean Squared Error':MSE
    })
  return pd.DataFrame(results).sort_values(by='R2 Score',ascending=False)

model_resuls= best_model(models)

model_resuls

"""**Random forest regressor scored the highest**"""

Randomforest_model = RandomForestRegressor()
Randomforest_model.fit(train_data,train_labels)
Randomforest_model_prediction = Randomforest_model.predict(test_data)

rf_dataframe = pd.DataFrame({'Actual':test_labels,'Predicted':Randomforest_model_prediction})

rf_dataframe.head(30)

"""**Save The model**"""

#save the model using joblib
joblib_filename = 'Calories_Randomforest_model.joblib'
joblib.dump(Randomforest_model,joblib_filename)

# save model using pickle
pickle_filename = 'Calories_Randomforest_model.pkl'
pickle.dump(Randomforest_model,open(pickle_filename,'wb'))

"""**Predictive System**"""

features.head()

input_data = [1,23,56,30,40,100,40]
input_data_array = np.asarray(input_data)
input_data_array_reshaped = input_data_array.reshape(1,-1)
predict = Randomforest_model.predict(input_data_array_reshaped)
predict