
# coding: utf-8

# In[32]:


"""
Created on Thu Feb 22 15:38:34 2018

@author: Disha
"""
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
import pprint


# In[18]:

#Ploting figures to get an understanding of outliers: 
def plotOutliers(subplot, data_set, feature_x, feature_y):    
    data = featureFormat(data_set, [feature_x, feature_y])
    for point in data:
        x = point[0]
        y = point[1]
        subplot.scatter( x, y )        
    subplot.set_xlabel(feature_x)
    subplot.set_ylabel(feature_y) 


# In[25]:

if __name__ == "__main__":
    
    #Populate data and feature list
    first_feature = ['poi']
    financial_features = ['salary', 'deferral_payments', 'total_payments', 'exercised_stock_options', 'bonus', 
                          'restricted_stock', 'restricted_stock_deferred', 'total_stock_value', 'expenses',
                          'loan_advances', 'director_fees', 'deferred_income', 'other', 'long_term_incentive']
    email_features = ['to_messages', 'shared_receipt_with_poi', 'from_messages', 'from_this_person_to_poi',
                      'from_poi_to_this_person']
    features_list = first_feature + financial_features + email_features
    
    #Load the dictionary containing the dataset
    with open("final_project_dataset.pkl", "r") as data_file:
        data_dict = pickle.load(data_file)
    
    fig = plt.figure(figsize=(14,8))
    fig.suptitle('Outlier Plots(Currency unit $)')
    ax1 = fig.add_subplot(221)
    plotOutliers(ax1, data_dict, 'total_payments', 'total_stock_value')
    ax2 = fig.add_subplot(222)
    plotOutliers(ax2, data_dict, 'from_poi_to_this_person', 'from_this_person_to_poi')
    ax3 = fig.add_subplot(223)
    plotOutliers(ax3, data_dict, 'salary', 'bonus')
    ax4 = fig.add_subplot(224)
    plotOutliers(ax4, data_dict, 'total_payments', 'other')
    plt.show()        


# In[20]:

if __name__ == "__main__":
        
    values = []
    for key, value in data_dict.items() :
        values = value
        for i,j in values.items():
            #the order of items in values is alphabetically, hence 'bonus' will come first and then 'salary'
            if (i == "total_payments" and j > 300000000 and j!= "NaN"):
                print (key,i,j)
            if (i == "salary" and j > 25000000 and j!= "NaN"):
                print (key,i,j) 


# In[22]:

if __name__ == "__main__":
    
    #Pop out the outlier
    data_dict.pop("TOTAL" , 0 )    


# In[24]:

if __name__ == "__main__":
    #Let's plot the figures once again after removing 'TOTAL'
    fig = plt.figure(figsize=(14,8))
    fig.suptitle('Outlier Plots(Currency unit $)')
    ax1 = fig.add_subplot(221)
    plotOutliers(ax1, data_dict, 'total_payments', 'total_stock_value')
    ax2 = fig.add_subplot(222)
    plotOutliers(ax2, data_dict, 'from_poi_to_this_person', 'from_this_person_to_poi')
    ax3 = fig.add_subplot(223)
    plotOutliers(ax3, data_dict, 'salary', 'bonus')
    ax4 = fig.add_subplot(224)
    plotOutliers(ax4, data_dict, 'total_payments', 'other')
    plt.show()


# Still we can see some outlier values. Find the outlier record

# In[26]:

if __name__ == "__main__":
    values = []
    for key, value in data_dict.items() :
        values = value
        for i,j in values.items():
            #the order of items in values is alphabetically, hence 'bonus' will come first and then 'salary'
            if (i == "total_payments" and j > 100000000 and j!= "NaN"):
                print (key,i,j)
            if (i == "salary" and j > 1000000 and j!= "NaN"):
                print (key,i,j)
            if (i == "other" and j > 6000000 and j!= "NaN"):
                print (key,i,j)
    
    #Lay and Skilling are important persons for ENRON. Are they POI?
    #Are the POI??
    print(data_dict["LAY KENNETH L"]["poi"])
    print(data_dict["SKILLING JEFFREY K"]["poi"])
    print(data_dict["FREVERT MARK A"]["poi"])    


# Lay and Skilling are 'Person of Interest'. So we can't ignore that value. We are keeping it in our data set. Mark Frevert is not POI as per data set, but his salary is near to those two person, that can't be an outlier. We will keep his record.

# In[34]:

if __name__ == "__main__":
    # Finding records having features value as "NaN"
    nan_dict = {}
    for key in data_dict:
        nan_dict[key] = 0
        for feature in features_list:
            if data_dict[key][feature] == "NaN":
                nan_dict[key] += 1
    sorted(nan_dict.items(), key=lambda x: x[1])
    pprint.pprint (sorted(nan_dict.items(), key=lambda x: x[1]))


# "LOCKHART EUGENE E" having NaN values for all features.

# In[35]:

if __name__ == "__main__":
    print(data_dict["LOCKHART EUGENE E"]["poi"])


# And POI is also FALSE. We can skip this record.

# In[39]:

if __name__ == "__main__":
    data_dict["THE TRAVEL AGENCY IN THE PARK"]
    pprint.pprint(data_dict["THE TRAVEL AGENCY IN THE PARK"])


# "THE TRAVEL AGENCY IN THE PARK" is also having NaN values for all features except 'poi', 'other' and 'total_payments'. All of its email features are NaN value. We will skip this record

# In[40]:

if __name__ == "__main__":
    data_dict.pop("LOCKHART EUGENE E" , 0 )
    data_dict.pop("THE TRAVEL AGENCY IN THE PARK" , 0 )


# In[15]:

def remove_outliers(data_dict):
    data_dict.pop("TOTAL" , 0 )
    data_dict.pop("LOCKHART EUGENE E" , 0 )
    data_dict.pop("THE TRAVEL AGENCY IN THE PARK" , 0 )
    return(data_dict)

