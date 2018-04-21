
# coding: utf-8

# In[ ]:

import sys
import pickle
sys.path.append("../tools/")
import pandas as pd
import numpy as np
from collections import defaultdict


# In[ ]:

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


# In[ ]:

### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
#features_list = ['poi','salary'] # You will need to use more features
first_feature = ['poi']
financial_features = ['salary', 'deferral_payments', 'total_payments', 'exercised_stock_options',
                      'bonus', 'restricted_stock', 'restricted_stock_deferred', 'total_stock_value',
                      'expenses', 'loan_advances', 'director_fees', 'deferred_income', 'other',
                      'long_term_incentive']
email_features = ['to_messages', 'shared_receipt_with_poi', 'from_messages', 
                  'from_this_person_to_poi', 'from_poi_to_this_person']
features_list = first_feature + financial_features + email_features


payment_features = ['salary', 'bonus', 'long_term_incentive', 'deferred_income', 'deferral_payments',
                    'loan_advances', 'other', 'expenses', 'director_fees']
stock_features = ['exercised_stock_options', 'restricted_stock', 'restricted_stock_deferred']


# In[ ]:

# Transform data from dictionary to the Pandas DataFrame
data_df = pd.DataFrame.from_dict(data_dict , orient = 'index')
#Order columns in DataFrame, exclude email column
data_df = data_df[features_list]
#Replace NaN with np.nan
data_df = data_df.replace('NaN', np.nan)
#Replace all np.Inf with np.nan
data_df = data_df.replace(np.inf, np.nan)
#Replace np.nan by 0
data_df = data_df.fillna(0)
#check data: summing payments features and compare with total_payments
data_df[data_df[payment_features].sum(axis='columns') != data_df.total_payments]


# In[ ]:

def correctdata(data_dict):
      
    #Correction of wrong value
    data_dict['BHATNAGAR SANJAY'] = data_dict.fromkeys(data_dict['BHATNAGAR SANJAY'], 'NaN')
    data_dict['BHATNAGAR SANJAY']['expenses'] = 137864
    data_dict['BHATNAGAR SANJAY']['total_payments'] = 137864
    data_dict['BHATNAGAR SANJAY']['exercised_stock_options'] = 15456290
    data_dict['BHATNAGAR SANJAY']['restricted_stock'] = 2604490
    data_dict['BHATNAGAR SANJAY']['restricted_stock_deferred'] = -2604490
    data_dict['BHATNAGAR SANJAY']['total_stock_value'] = 15456290
    data_dict['BHATNAGAR SANJAY']['poi'] = False
    data_dict['BHATNAGAR SANJAY']['to_message'] = 523
    data_dict['BHATNAGAR SANJAY']['shared_receipt_with_poi'] = 463
    data_dict['BHATNAGAR SANJAY']['from_message'] = 29
    data_dict['BHATNAGAR SANJAY']['from_this_person_to_poi'] = 1
    data_dict['BHATNAGAR SANJAY']['from_poi_to_this_person'] = 0
    #data_dict['BHATNAGAR SANJAY',]
        
    data_dict['BELFER ROBERT'] = data_dict.fromkeys(data_dict['BELFER ROBERT'], 'NaN')
    data_dict['BELFER ROBERT']['total_payments'] = 3285
    data_dict['BELFER ROBERT']['restricted_stock'] = 44093
    data_dict['BELFER ROBERT']['restricted_stock_deferred'] = -44093
    data_dict['BELFER ROBERT']['director_fees'] = 102500
    data_dict['BELFER ROBERT']['deferred_income'] = -102500
    data_dict['BELFER ROBERT']['expenses'] = 3285
    data_dict['BELFER ROBERT']['poi'] = False
    #data_dict['BELFER ROBERT',]
    return(data_dict)


# In[ ]:

if __name__ == "__main__":
    
    correctdata(data_dict)    
    # Transform data from dictionary to the Pandas DataFrame
    data_df = pd.DataFrame.from_dict(data_dict , orient = 'index')
    #Replace NaN with 0
    data_df = data_df.replace('NaN', np.nan)
    data_df = data_df.fillna(0)
    #Rechecking if those records are corrected
    print(data_df[data_df[payment_features].sum(axis='columns') != data_df.total_payments])
    print(data_df[data_df[stock_features].sum(axis='columns') != data_df.total_stock_value])


# In[ ]:



