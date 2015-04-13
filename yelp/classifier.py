import numpy as np
import random
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import SGDRegressor , Lasso
from sklearn.feature_selection import VarianceThreshold
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor , GradientBoostingRegressor

from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from sklearn.svm import SVC

from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report



def cross_val(X,y):
  
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
  print "X train shape",X_train.shape
  print "X_test share",X_test.shape

  #Uncomment the tuned_parameters for the appropiate REgressors
  #tuned_parameters = {'reg__penalty': ['l1','l2'] , 'reg__C':[0.01,0.02,0.05,0.08],'feature_sel__n_features_to_select' : [1,2,3,4,5,6,7,8,9,10,11,12]}
  #tuned_parameters = {'reg__n_iter':[10,30,50], 'feature_sel__n_features_to_select' : [10,20,30,40,50,60,70,80,90,100,110,120]}
  #tuned_parameters = {'reg__penalty': ['l1','l2','elasticnet'],'reg__loss' :['squared_loss','huber'] , 'reg__n_iter': [5,10,20],  'feature_sel__n_features_to_select' : [10,20,30,40,50,60,70,80,90,100,110,120]}
  #pipeline = Pipeline([#('feature_trans', MinMaxScaler()), 
    #('feature_sel', RFE(BayesianRidge())), 
  #  ('reg', BayesianRidge())])
  #LinearSVC
  #tuned_parameters = {'loss': ['l1','l2'],'penalty': ['l2'],
  #                    'C': [1.0,2.0,5.0,10.0]}

  #SVM
  tuned_parameters = {'C': [1.0,2.0,5.0,10.0],
                      'kernel': ['linear','poly'],
                      'probability': [True]}

  scores = ['accuracy']

  for score in scores:
      print("# Tuning hyper-parameters for %s" % score)
      print()
      clf = GridSearchCV(SVC(), tuned_parameters, cv=5, scoring=score)
      clf.fit(X_train, y_train)
      print("Best parameters set found on development set:")
      print()
      print(clf.best_estimator_)
      print()
      print("Grid scores on development set:")
      print()
      for params, mean_score, scores in clf.grid_scores_:
          print("%0.3f (+/-%0.03f) for %r"
                % (mean_score, scores.std() / 2, params))

      return clf.best_estimator_


def init_train():
  '''
  Will Read data from 50p and 50n word samples and populate the 
  training data using vectors.txt file. This will return, the training data 
  which can be directly fed to sklearn classifiers.
  '''
  kwords = {} #known words from p50 & n50
  vdict = {}
  train = []

  with open('./data/50p.txt') as pfile:
    for line in pfile:
      line = line.strip()
      kwords[line] = 1

  with open('./data/50n.txt') as nfile:
    for line in nfile:
      line = line.strip()
      kwords[line] = 0

  with open('../w2vec/vectors.txt') as vfile:
    vfile.next()  #ignoring the first line in the file
    for line in vfile:
      sline = line.strip().split(' ')
      vdict[sline[0]] = map(float,sline[1:])

  for word in kwords:
    if word in vdict:
      features = vdict[word]
      features.append(kwords[word])
      train.append(features)
    else:
      print "The word =>",word," Not found in vector dictionary :("

  return train , vdict


if __name__ == '__main__':
  data_list, entire_dict_feat = init_train()
  data = np.array(data_list)
  y = data[:,-1] 
  X = data[:, :-1] 
  
  clf = cross_val(X,y)
  #clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, 
  #  degree=3, gamma=0.0,kernel='linear', max_iter=-1, probability=True, 
  #  random_state=None, shrinking=True, tol=0.001, verbose=False)


  #rand_word = random.choice(entire_dict_feat.keys()) #getting a random word
  '''
  rand_word = 'tasty'
  print "random word is ", rand_word
  print "feature vector of the random word is ",entire_dict_feat[rand_word]
  rand_word_vector = entire_dict_feat[rand_word]
  print clf.predict(rand_word_vector)[0]
  print clf.predict_proba(rand_word_vector)[0][1]
  '''

  
  #Checking for all the words with label == 1
  flabel = open('label1_all.txt','w')
  for word in entire_dict_feat:
    rand_word_vector = entire_dict_feat[word]
    #print "word is ",word
    #print "rand_word_vector",rand_word_vector

    #removing the last element which I added while training set
    #this means this word is most likely in 50p/50n words
    if len(rand_word_vector) > 100:
      rand_word_vector.pop()  

    pvalue = clf.predict(rand_word_vector)[0]
    #print "the pvalue is ",pvalue
    #if int(pvalue) == 1:
    prob = clf.predict_proba(rand_word_vector)
    flabel.write(word+","+str(prob[0][1])+"\n")
  flabel.close()
  
      

  






























#Uncomment the following pipeline to run any desired classifier you want

'''
clf = SGDRegressor(alpha=0.0001, epsilon=0.1, eta0=0.01, fit_intercept=True,
       l1_ratio=0.15, learning_rate='invscaling', loss='huber', n_iter=10,
       penalty='l1', power_t=0.25, random_state=None, shuffle=False,
       verbose=0, warm_start=False)
'''

'''
clf = Pipeline(steps=[('feature_trans', StandardScaler()), 
  ('feature_sel', RFE(estimator=SGDRegressor(alpha=0.0001, epsilon=0.1, eta0=0.01, fit_intercept=True,
       l1_ratio=0.15, learning_rate='invscaling', loss='squared_loss',
       n_iter=5, penalty='l2', power_t=0.25, random_state=None,
       shuffle=False, verbose=0, warm_start=False)))])
'''

'''
clf = Pipeline(steps=[('feature_trans', StandardScaler()), 
      ('feature_sel', RFE(estimator=BayesianRidge(alpha_1=1e-06, alpha_2=1e-06, compute_score=False, copy_X=True,
       fit_intercept=True, lambda_1=1e-06, lambda_2=1e-06,
       normalize=False, tol=0.001, verbose=False, 
       n_iter=30)))])
'''


'''
clf = RandomForestRegressor(bootstrap=True, compute_importances=None,
           criterion='mse', max_depth=None, max_features='auto',
           max_leaf_nodes=None, min_density=None, min_samples_leaf=1,
           min_samples_split=2, n_estimators=60, n_jobs=1, oob_score=False,
           random_state=None, verbose=0)
'''
'''
clf = Lasso(alpha=0.005, copy_X=True, fit_intercept=True, max_iter=1000,
   normalize=False, positive=False, precompute='auto', tol=0.0001,
   warm_start=False)
'''
'''
clf = LogisticRegression(C=0.01, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, penalty='l1', random_state=None, tol=0.0001)
'''

'''
clf = GradientBoostingRegressor(alpha=0.9, init=None, learning_rate=0.1, loss='lad',
             max_depth=3, max_features=None, max_leaf_nodes=None,
             min_samples_leaf=1, min_samples_split=2, n_estimators=60,
             random_state=None, subsample=1.0, verbose=0, warm_start=False)


clf.fit(X_train, Y_train)
Y_pred = clf.predict(X_test)

fout = open('result.kaggle', 'w')
fout.write("ID,Target\n");
for i in range(Y_pred.shape[0]):
      fout.write("\n" + str(float(i+1)) + "," + str(float(Y_pred[i]))) 
fout.close()



'''