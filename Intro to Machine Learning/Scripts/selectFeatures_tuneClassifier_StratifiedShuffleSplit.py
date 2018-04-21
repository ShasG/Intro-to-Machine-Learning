
# coding: utf-8

# In[ ]:

import sys
import pickle
sys.path.append("../tools/")
import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from feature_format import featureFormat, targetFeatureSplit
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import operator
import pprint
from sklearn.metrics import accuracy_score, precision_score, recall_score
from numpy import mean
from sklearn.grid_search import GridSearchCV
#from tester import test_classifier
from tester_custom import test_classifier


# In[ ]:

if __name__ == "__main__":
    ### Load the dictionary containing the dataset
    with open("final_project_dataset.pkl", "r") as data_file:
        data_dict = pickle.load(data_file)


# In[ ]:

if __name__ == "__main__":
    #Remove the outliers from data.
    from remove_outlier import remove_outliers
    data_dict = remove_outliers(data_dict)
    #Correct records for BHATNAGAR and BELFIER
    from correct_records import correctdata
    data_dict = correctdata(data_dict)


# In[ ]:

if __name__ == "__main__":
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

if __name__ == "__main__":

    # List valid occurrences
    non_nas = {}
    for feature in features_list:
        for k, v in data_dict.iteritems():
            if v[feature] != 'NaN':
                if feature not in non_nas.keys():
                    non_nas[feature] = 0
                non_nas[feature] += 1
    
    valid_records_per_feature = sorted((non_nas).items(), key = operator.itemgetter(1), reverse = True)
    pprint.pprint(valid_records_per_feature)


# In[ ]:

def select_kbest_feature(data_dict,features_list,feature_count):
    
    data = featureFormat(data_dict, features_list)
    labels, features = targetFeatureSplit(data)
    
    clf = SelectKBest(k = feature_count)
    clf = clf.fit(features, labels)
    feature_weights = {}
    for idx, feature in enumerate(clf.scores_):
        feature_weights[features_list[1:][idx]] = feature
    best_features = sorted(feature_weights.items(), key = lambda k: k[1], reverse = True)[:feature_count]
    kbest_init_features = []
    for k, v in best_features:
        kbest_init_features.append(k)
        
    features_score_list = zip(clf.get_support(), features_list[1:], clf.scores_)
    features_score_list = sorted(features_score_list, key=lambda x: x[2], reverse = True)
        
    return(kbest_init_features,features_score_list)


# In[ ]:

if __name__ == "__main__":
    
    feature_count = 12
    kbest_init_features,kbest_init_features_score_list = select_kbest_feature(data_dict,features_list,feature_count)
    pprint.pprint(kbest_init_features_score_list)


# In[ ]:

if __name__ == "__main__":
    
    # Transform data from dictionary to the Pandas DataFrame
    data_df = pd.DataFrame.from_dict(data_dict , orient = 'index')
    #Order columns in DataFrame, exclude email column
    data_df = data_df[features_list]
    #Replace NaN with np.Nan
    data_df = data_df.replace('NaN', np.nan)
    #Replace Inf with np.NaN
    data_df = data_df.replace(np.inf, np.nan)
    #data_df[data_df == np.Inf] = np.NaN
    #Replace all np.NaN with 0
    data_df = data_df.fillna(0)


# ###### Using another method to select features:

# In[ ]:

#def features_with_non_null_importance():
if __name__ == "__main__":
    #Decision tree using features with non-null importance
    from sklearn.tree import DecisionTreeClassifier
    
    data = featureFormat(data_dict, features_list)
    labels, features = targetFeatureSplit(data)
    
    clf = DecisionTreeClassifier(random_state = 75)
    clf.fit(features,labels)
    
    # show the features with non null importance, sorted and create features_list of features for the model
    features_importance = []
    for i in range(len(clf.feature_importances_)):
        #if clf.feature_importances_[i] > 0:
        features_importance.append([data_df.columns[i+1], clf.feature_importances_[i]])
        
    features_importance.sort(key=lambda x: x[1], reverse = True)

    for f_i in features_importance:
        print(f_i)    


# This one is also indicating some of the parameters as important over others but the list is not same. I will go with the k-best options as it seems more relevant to me.

# In[ ]:

#Adding new features
if __name__ == "__main__":
    #create additional feature: fraction of person's email to POI to all sent messages
    data_df['fraction_to_poi'] = data_df['from_this_person_to_poi']/data_df['from_messages']
    data_df['fraction_from_poi'] = data_df['from_poi_to_this_person']/data_df['to_messages']
    #Replace NaN with 0
    data_df = data_df.replace('NaN', np.nan)
    #Replace all np.Inf with np.NaN
    data_df = data_df.replace(np.inf, np.nan)
    #data_df[data_df == np.Inf] = np.NaN 
    #Replace all np.NaN with 0
    data_df = data_df.fillna(0)
    
    new_data_dict = pd.DataFrame.to_dict(data_df , orient = 'index')
    new_features_list = features_list + ['fraction_to_poi', 'fraction_from_poi']
    
    feature_count = 12
    new_kbest_features,new_kbest_features_score_list = select_kbest_feature(new_data_dict,new_features_list,feature_count)
    pprint.pprint(new_kbest_features_score_list)


# We can see the new feature 'fraction_to_poi' is having much better score than other email-features and scoring a 5th best feature among all of them.

# In[ ]:

#Scaling features
#All the values are having very different ranges. So we will do feature scaling before training our final classifier.
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

if __name__ == "__main__":
    mm_sc = MinMaxScaler()


# Now will check with classifier and these features combination to finalize the classifier and corresponding best features.

# In[ ]:

if __name__ == "__main__":
    
    classifier_1 = [{'classifier': DecisionTreeClassifier(),
                     'params':
                     {
                        "clf__criterion": ["gini", "entropy"],
                        "clf__min_samples_split": [10,15,20,25],
                        "clf__random_state":[42] 
                     }},
                    {'classifier': GaussianNB(),
                     'params': {}
                    }]


# In[ ]:

if __name__ == "__main__":
    
    classifier_2 = [{'classifier': LogisticRegression(),
                     'params': {  "clf__C": [0.05, 0.5, 1, 10, 10**2, 10**3, 10**5,10**9, 10**10, 10**15],
                                  "clf__tol":[10**-1, 10**-2, 10**-4, 10**-5, 10**-6, 10**-10, 10**-15],
                                  "clf__class_weight":['balanced'],
                                  "clf__random_state":[42]
                                }
                    }]


# In[ ]:

#def evaluate_classifier(clf,features, labels, num_iter, test_size, params):

def evaluate_classifier(clf,dataset, feature_list, num_iter,test_size, params):
    """
    #Evaluates algorithms and prints out the mean value of precision, recall, and accuracy.
    
    """

    features_train, features_test, labels_train, labels_test =         train_test_split(features, labels, test_size=test_size, random_state=42)

    precision_values = []
    recall_values = []
    accuracy_values = []

    for i in xrange(0, num_iter):
        #print params
        clf = GridSearchCV(clf, params)
        clf.fit(features_train, labels_train)
        clf = clf.best_estimator_
        
        accuracy_score, precision_score, recall_score = test_classifier(clf, dataset, feature_list)
        precision_values.append(precision_score)
        recall_values.append(recall_score)
        accuracy_values.append(accuracy_score)
        
    print '_______________________________________________________________'
    print clf
    
    print 'Recall score: ', mean(recall_values)
    print 'Precision score: ', mean(precision_values)
    print 'Accuracy score: ' , mean(accuracy_values)        


# In[ ]:

#Test set size to be used during split of data set
test_size = 0.3


# ###### Checking with all of the 20 original features:

# In[ ]:

if __name__ == "__main__":
    
    #data = featureFormat(data_dict, features_list)
    #labels, features = targetFeatureSplit(data)
    
#For Classifiers those do not need any feature scaling
    for c in classifier_1:
        clf = Pipeline(steps=[("skb", SelectKBest(k='all')), ("clf", c['classifier'])])
        evaluate_classifier(clf, data_dict, features_list, 50, test_size, c['params'])
    
#For Classifiers those need feature scaling   
    for c in classifier_2:
        clf = Pipeline(steps=[("scaler", mm_sc), ("skb", SelectKBest(k='all')), ("clf", c['classifier'])])
        evaluate_classifier(clf, data_dict, features_list, 50, test_size, c['params'])       


# ###### With 20 original features and 2 new features:

# In[ ]:

if __name__ == "__main__":
    
    #data = featureFormat(new_data_dict, new_features_list)
    #labels, features = targetFeatureSplit(data)
    
#For Classifiers those do not need any feature scaling
    for c in classifier_1:
        clf = Pipeline(steps=[("skb", SelectKBest(k='all')), ("clf", c['classifier'])]) 
        evaluate_classifier(clf,new_data_dict, new_features_list, 50,test_size, c['params'])

#For Classifiers those need feature scaling   
    for c in classifier_2:
        clf = Pipeline(steps=[("scaler", mm_sc), ("skb", SelectKBest(k='all')), ("clf", c['classifier'])])
        evaluate_classifier(clf,new_data_dict, new_features_list, 50,test_size, c['params'])      


# ###### K best features selected from SelectKBest from original 20 features:

# In[ ]:

if __name__ == "__main__":
    
    dummy_features = first_feature + kbest_init_features
    #data = featureFormat(data_dict, dummy_features)
    #labels, features = targetFeatureSplit(data)
    
#For Classifiers those do not need any feature scaling
    for c in classifier_1:
        clf = Pipeline(steps=[("skb", SelectKBest(k='all')), ("clf", c['classifier'])])
        evaluate_classifier(clf,data_dict, dummy_features, 50,test_size, c['params'])
    
#For Classifiers those need feature scaling   
    for c in classifier_2:
        clf = Pipeline(steps=[("scaler", mm_sc), ("skb", SelectKBest(k='all')), ("clf", c['classifier'])])
        evaluate_classifier(clf,data_dict, dummy_features, 50,test_size, c['params'])      


# ###### k best features selected from SelectKBest and then adding the 2 new features, total k+2 features:

# In[ ]:

if __name__ == "__main__":
    
    kbestfeatures_add = first_feature + kbest_init_features + ['fraction_to_poi', 'fraction_from_poi']
    #data = featureFormat(new_data_dict, kbestfeatures_add)
    #labels, features = targetFeatureSplit(data)
    
#For Classifiers those do not need any feature scaling
    for c in classifier_1:
        clf = Pipeline(steps=[("skb", SelectKBest(k='all')), ("clf", c['classifier'])])
        evaluate_classifier(clf, new_data_dict, kbestfeatures_add, 50,test_size, c['params'])
    
#For Classifiers those need feature scaling   
    for c in classifier_2:
        clf = Pipeline(steps=[("scaler", mm_sc), ("skb", SelectKBest(k='all')), ("clf", c['classifier'])])
        evaluate_classifier(clf, new_data_dict, kbestfeatures_add, 50,test_size, c['params'])       


# ###### k best features selected from SelectKBest among 22 features(20 original and 2 new features):

# In[ ]:

if __name__ == "__main__":
    
    dummy_features_list = first_feature + new_kbest_features
    #data = featureFormat(new_data_dict, dummy_features_list)
    #labels, features = targetFeatureSplit(data)
    
#For Classifiers those do not need any feature scaling
    for c in classifier_1:
        clf = Pipeline(steps=[("skb", SelectKBest(k='all')), ("clf", c['classifier'])]) 
        evaluate_classifier(clf, new_data_dict, dummy_features_list,10,test_size, c['params'])
    
#For Classifiers those need feature scaling   
    for c in classifier_2:
        clf = Pipeline(steps=[("scaler", mm_sc), ("skb", SelectKBest(k='all')), ("clf", c['classifier'])])
        evaluate_classifier(clf, new_data_dict, dummy_features_list,10,test_size, c['params'])
        


# ###### According to above result, best algorithm is 'LogisticRegression' with below parameters.
# Pipeline(steps=[('scaler', MinMaxScaler(copy=True, feature_range=(0, 1))), ('skb', SelectKBest(k='all', score_func=<function f_classif at 0x000000000C39A198>)), ('clf', LogisticRegression(C=1000000000, class_weight='balanced', dual=False,
#           fit_intercept=True, intercept_scaling=1, max_iter=100,
#           multi_class='ovr', n_jobs=1, penalty='l2', random_state=42,
#           solver='liblinear', tol=1e-05, verbose=0, warm_start=False))])

# In[ ]:

def tuned_classifier_evaluation(clf,scaler,features,labels,test_size,num_iter):
    
    features_train, features_test, labels_train, labels_test =     train_test_split(features, labels, test_size=test_size, random_state=42)
    
    features_train = scaler.fit_transform(features_train)
    features_test = scaler.transform(features_test)

    precision_values = []
    recall_values = []
    accuracy_values = []

    for i in range(0, num_iter):
        
        clf.fit(features_train, labels_train)
        pred = clf.predict(features_test)
        precision_values.append(precision_score(labels_test, pred))
        recall_values.append(recall_score(labels_test, pred))
        accuracy_values.append(accuracy_score(labels_test, pred))
        
    print clf
    print 'Recall score: ', mean(recall_values)
    print 'Precision score: ', mean(precision_values)
    print 'Accuracy score: ' , mean(accuracy_values)

