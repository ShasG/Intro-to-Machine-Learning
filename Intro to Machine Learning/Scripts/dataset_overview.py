
# coding: utf-8

# In[1]:

#Import Libraries
import sys
import pickle
sys.path.append("../tools/")
import pandas as pd
import csv
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data


# In[3]:

#Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


# In[30]:

if __name__ == "__main__":
    
    # Transform data from dictionary to the Pandas DataFrame
    data_df = pd.DataFrame.from_dict(data_dict , orient = 'index')
    print('Data Count:',len(data_df))


# In[24]:

if __name__ == "__main__":
    
    list(data_df.columns)


# In[27]:

if __name__ == "__main__":
    
    #Populate data and feature list
    first_feature = ['poi']
    financial_features = ['salary', 'deferral_payments', 'total_payments',
                          'exercised_stock_options', 'bonus', 
                          'restricted_stock', 'restricted_stock_deferred',
                          'total_stock_value', 'expenses', 'loan_advances',
                          'director_fees', 'deferred_income', 'other',
                          'long_term_incentive']
    email_features = ['to_messages', 'shared_receipt_with_poi', 'from_messages', 
                      'from_this_person_to_poi', 'from_poi_to_this_person']
    features_list = first_feature + financial_features + email_features


# In[28]:

if __name__ == "__main__":
    
    #Populate POI and Non-POI count
    poi_count = 0
    non_poi_count = 0
    null_count = defaultdict(int)
    for key, values in data_dict.iteritems():
        if values['poi']:
            poi_count += 1
        else:
            non_poi_count += 1
        for i,j in values.iteritems():
            if j == 'NaN':
                null_count[i] += 1
            else:
                null_count[i] = null_count[i]
                
    print('POI Count:', poi_count)
    print('Non-POI Count:', non_poi_count)


# In[26]:

#Populate POI and Non-POI count
poi_count = 0
non_poi_count = 0
null_count = defaultdict(int)
for key, values in data_dict.iteritems():
    if values['poi']:
        poi_count += 1
    else:
        non_poi_count += 1
    for i,j in values.iteritems():
        if j == 'NaN':
            null_count[i] += 1
        else:
            null_count[i] = null_count[i]
        
#Find NULL percentage of each feature values
data_len = len(data_dict)
null_percentage = defaultdict(float)
null_percentage = null_count
for i in null_percentage:
    null_percentage[i] = float((float(null_count[i]) / float(data_len))
    * 100.0)
    
    
#Plot the missing ratio
features_names = list(null_percentage.keys())
features_values = list(null_percentage.values())

plt.figure(figsize=(10,7))
plt.barh(range(len(null_percentage)),features_values,tick_label=features_names)
plt.grid(which='major', axis='both', linestyle='--')
plt.xlabel("Percentage of Missing values")
plt.title("Missing value percentage plot")
plt.show()    

