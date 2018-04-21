
# coding: utf-8

# In[ ]:

import sys
import pickle
sys.path.append("../tools/")
import pandas as pd
import csv
import numpy as np
from numpy import mean
from collections import defaultdict
from sklearn.feature_selection import SelectKBest
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score
import operator
import pprint


# In[ ]:

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


# In[ ]:

data_dict["BHATNAGAR SANJAY"]


# In[ ]:

#Remove the outliers from data.
from remove_outlier import remove_outliers
data_dict = remove_outliers(data_dict)


# In[ ]:

#Correct records for BHATNAGAR and BELFIER
from correct_records import correctdata
data_dict = correctdata(data_dict)


# In[ ]:

#All feature list
first_feature = ['poi']
financial_features = ['salary', 'deferral_payments', 'total_payments', 'exercised_stock_options',
                      'bonus', 'restricted_stock', 'restricted_stock_deferred', 'total_stock_value',
                      'expenses', 'loan_advances', 'director_fees', 'deferred_income', 'other',
                      'long_term_incentive']
email_features = ['to_messages', 'shared_receipt_with_poi', 'from_messages', 
                  'from_this_person_to_poi', 'from_poi_to_this_person']
features_list = first_feature + financial_features + email_features


# In[ ]:

# Transform data from dictionary to the Pandas DataFrame
data_df = pd.DataFrame.from_dict(data_dict , orient = 'index')
#Order columns in DataFrame, exclude email column
data_df = data_df[features_list]
#Replace NaN with np.nan
data_df = data_df.replace('NaN', np.nan)
#Replace Inf with np.nan
data_df = data_df.replace(np.inf, np.nan)
#Replace np.nan by 0
data_df = data_df.fillna(0)
#Transform back to dictionary
data_dict = pd.DataFrame.to_dict(data_df , orient = 'index')
#data_dict


# In[ ]:

#Format the data to get the features and labels
data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)


# In[ ]:

from selectFeatures_tuneClassifier import select_kbest_feature


# In[ ]:

#from select_features import select_kbest_feature
feature_count = 12
kbest_features, kbest_features_score = select_kbest_feature(data_dict,features_list,feature_count)
kbest_features_score


# In[ ]:

# Transform data from dictionary to the Pandas DataFrame
data_df = pd.DataFrame.from_dict(data_dict , orient = 'index')


# In[ ]:

#Order columns in DataFrame, exclude email column
data_df = data_df[features_list]
#Replace NaN with np.nan
data_df = data_df.replace('NaN', np.nan)
#Replace Inf with np.nan
data_df = data_df.replace(np.inf, np.nan)
#Replace np.nan by 0
data_df = data_df.fillna(0)


# In[ ]:

#Add new feature. Create additional feature: fraction of person's email to POI to all sent messages
data_df['fraction_to_poi'] = data_df['from_this_person_to_poi']/data_df['from_messages']
data_df['fraction_from_poi'] = data_df['from_poi_to_this_person']/data_df['to_messages']


# In[ ]:

#Replace NaN with np.nan
data_df = data_df.replace('NaN', np.nan)
#Replace Inf with np.nan
data_df = data_df.replace(np.inf, np.nan)
#Replace np.nan by 0
data_df = data_df.fillna(0)


# Now again checking the K-best features along with these two new features.

# In[ ]:

new_data_dict = pd.DataFrame.to_dict(data_df , orient = 'index')
new_features_list = features_list + ['fraction_to_poi', 'fraction_from_poi']
    
feature_count = 12
new_kbest_features, new_kbest_features_score = select_kbest_feature(new_data_dict,new_features_list,feature_count)
pprint.pprint(new_kbest_features_score)


# In[ ]:

new_kbest_features


# In[ ]:

my_features_list = first_feature + new_kbest_features #features_list + ['fraction_to_poi', 'fraction_from_poi']


# In[ ]:

#Order columns in DataFrame, exclude features other than the selected features 
data_df = data_df[my_features_list]
my_dataset = pd.DataFrame.to_dict(data_df , orient = 'index')


# In[ ]:

#Get features and labels from data set
data = featureFormat(my_dataset, my_features_list, sort_keys = True, remove_NaN = True)
labels, features = targetFeatureSplit(data)


# ###### Feature Scaling
# 
# Feature scaling and tuning the algorithm is done in script 'selectfeatures_tuneclassifier'. Retrieving the best classifier by importing the script.

# In[ ]:

#Scaling features
#All the values are having very different ranges. So we will do feature scaling before training our final classifier.
from sklearn.preprocessing import MinMaxScaler
mm_sc = MinMaxScaler()


# In[ ]:

clf = Pipeline(steps=[('scaler', MinMaxScaler(copy=True, feature_range=(0, 1))),
                      ('skb', SelectKBest(k='all')),
                      ('clf', LogisticRegression(C=1000000000, class_weight='balanced', dual=False,
                                                 fit_intercept=True, intercept_scaling=1, max_iter=100,
                                                 multi_class='ovr', n_jobs=1, penalty='l2', random_state=42,
                                                 solver='liblinear', tol=1e-05, verbose=0, warm_start=False))])


# The above final classifier is derived in script 'selectFeatures_tuneClassifier.py'. The result of this one is shown below.
# 
# Recall score:  0.75
# 
# Precision score:  0.4
# 
# Accuracy score:  0.744186046512

# Next validating the result using function `'test_classifier'` of given script 'tester.py'. This function is usin 1000 folds of   `StratifiedShuffleSplit` to split the data set to traning and test data set.

# In[ ]:

from tester import test_classifier
test_classifier(clf, my_dataset, my_features_list)


# In[ ]:

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, my_features_list)

