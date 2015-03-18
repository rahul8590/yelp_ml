import numpy as np
import sklearn as sk
import pandas as pd
from time import time
import argparse 
import math
from pprint import pprint
from scipy import stats
### scikit imports 
from sklearn.lda import LDA
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.feature_selection import VarianceThreshold, RFE, SelectKBest, f_classif,SelectPercentile, SelectFpr, SelectFdr, SelectFwe, f_regression 
from sklearn.linear_model import LogisticRegression, RandomizedLogisticRegression, SGDClassifier, LinearRegression, Ridge, BayesianRidge, SGDRegressor
from sklearn.svm import SVC, SVR, LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, ExtraTreesClassifier, GradientBoostingClassifier, AdaBoostClassifier, RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, precision_score, recall_score, f1_score, accuracy_score, classification_report, mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import ShuffleSplit, StratifiedKFold, StratifiedShuffleSplit, KFold, train_test_split
from sklearn.grid_search import GridSearchCV

def load_data(file_name):
	df    = np.load(file_name)
        Y     = df[:,0]
        Y_cas = df[:,1]
        Y_reg = df[:,2]
	X     = df[:,3:]
	return X, Y_cas, Y_reg, Y
def load_test_data(file_name):
        df         = np.load(file_name)
        Y          = df[:, 0]
        X_datetime = df[:, 1]
        X          = df[:, 2:]
        print Y.shape, X_datetime.shape, X.shape
        print "sample-count", Y[0:2]
        print "date-time", X_datetime[0:2]
        print "data", X[0:2]
        return X, X_datetime, Y

class ml_model():
	def __init__(self, name, method, params):
		self.name   = name
		self.method = method
		self.params = params
		self.name_n_params = (name, params)
		self.name_n_method = (name, method)


## feature transformation
min_max_scaler = ml_model('min-max-scaler', MinMaxScaler(), {})
std_scaler     = ml_model('std-scaler', StandardScaler(), {})

## feature selection techniques
vr            = ml_model('var-threshold', VarianceThreshold(), {'threshold' : (0.0001, 0.0010, 0.005, 0.01)})
select_k_best = ml_model('select-k-best', SelectKBest(f_regression), {'k' : (3,4,5,6,7,8,9)})
rfe           = ml_model('rfe', RFE(estimator=SVR(kernel='linear')), {'n_features_to_select' : (3,4,5,6,7,8,9)})

## regression techniques
linear_reg    = ml_model('linear-regression', LinearRegression(), {})
rf_reg        = ml_model('random-forest-reg', RandomForestRegressor(), {'n_estimators' : (100, 300, 500)})
gb_reg        = ml_model('gb-reg', GradientBoostingRegressor(), {'n_estimators' : (100, 200, 300, 400), 'max_depth' : (5, 6, 7) })
ada_reg       = ml_model('adaboost-reg', AdaBoostRegressor(), {'n_estimators' : (100, 200, 300, 400), 'loss' : ('square', 'linear', 'exponential'), 'random_state' : (12345, None)})
bayes_ridge   = ml_model('bayesian-ridge-regression', BayesianRidge(), {})
svr           = ml_model('svm-regression', SVR(), {'kernel' : ('linear', 'rbf'), 'gamma' : 10.0 ** np.arange(-3, 3), 'C' : 10.0 ** np.arange(-2, 2), 'epsilon' : 10.00 ** np.arange(-3, 0), 'tol' : 10.0 ** np.arange(-5, -2)} )
sgd_reg       = ml_model('sgd-regressor', SGDRegressor(), {'loss' : ('squared_loss', 'epsilon_insensitive', 'squared_epsilon_insensitive'), 'penalty' : ('l1', 'l2', 'elasticnet'), 'n_iter' : (5, 10, 20, 30, 50, 100, 200, 300, 400, 500, 1000)}) 

''' root mean squared log error '''
def rmsle(y_true, y_pred):
      assert(len(y_true) == len(y_pred))
      n = len(y_true)
      s = 0.0
      for i in range(n):
           val = y_pred[i] - y_true[i]
           s += (val * val)
      return math.sqrt(s/float(n))

def gen_pipeline_steps():
 for reg in [ rf_reg]:  
    name          = reg.name
    steps         = [reg.name_n_method]
    name_n_params = [reg.name_n_params] 
    yield (name, steps, get_hyperparameter_grid(name_n_params))
    '''for ft in [min_max_scaler, std_scaler]:                           
       name          = ft.name + ':' + reg.name
       steps         = [ft.name_n_method, reg.name_n_method]
       name_n_params = [ft.name_n_params, reg.name_n_params] 
       yield (name, steps, get_hyperparameter_grid(name_n_params))
       for fs in []:
	     name          = ft.name + ':' + fs.name + ':' + reg.name
             steps         = [ft.name_n_method, fs.name_n_method, reg.name_n_method]
	     name_n_params = [ft.name_n_params, fs.name_n_params, reg.name_n_params] 
 	     yield (name, steps, get_hyperparameter_grid(name_n_params))
    ''' 
def get_hyperparameter_grid(steps):
	grid = {}
	for name, params in steps:
	      for param_name, vals in params.iteritems():
	                grid[name + '__' + param_name] = vals
	return grid
	                 
def do_grid_search(pipeline, parameters, cross_v, X, Y):
	print("Performing grid search...")
	print("pipeline:", [name for name, _ in pipeline.steps])
	print("parameters:")
	pprint(parameters)
	grid_search = GridSearchCV(pipeline, parameters, cv = cross_v, n_jobs = -1, refit = True, verbose=1, score_func=rmsle)
        t0 = time()
        grid_search.fit(X, Y)
        time_taken = time() - t0
	print("done in %0.3fs" % (time_taken))
	print()
	print("Best score: %0.3f" % grid_search.best_score_)
	best_parameters = grid_search.best_estimator_.get_params()
	for param_name in sorted(parameters.keys()):
               print("\t%s: %r" % (param_name, best_parameters[param_name]))
	return grid_search.best_estimator_, best_parameters , grid_search.best_score_, time_taken

def do_kaggle_submission(Y_pred, X_datetime, name):
	   
	 print("Doing Kaggle Submission...")
         print rmsle(Y_pred[0], Y_pred[1] + Y_pred[2])
         fout = open(name + '.sub.csv', 'w')
         fout_y = open(name + '.sub1.csv', 'w')
         fout.write("datetime,count")
         fout_y.write("datetime,count")
         for i in range(Y_pred[0].shape[0]):
              cas = math.exp(Y_pred[1][i]) - 1
              reg = math.exp(Y_pred[2][i]) - 1
              total = math.exp(Y_pred[0][i]) - 1
	      fout.write("\n" + str(X_datetime[i]) + "," + str(cas + reg))
	      fout_y.write("\n" + str(X_datetime[i]) + "," + str(total))
         fout.close() 
         fout_y.close()

if __name__ == '__main__':
       X, Y_cas, Y_reg, Y   = load_data('train.npy')
       Y   = np.log(1 + Y)
       Y_cas = np.log(1 + Y_cas)
       Y_reg = np.log(1 + Y_reg)
       print X.shape, Y.shape[0], Y_cas.shape[0], Y_reg.shape[0]
        
       X_test, X_datetime, Y_test = load_test_data('test_distribute.npy')
       print "# of features - ", X.shape[1], "# of examples - ", X.shape[0]
       fout = open('reg-perf-data.csv', 'w')
       fout.write('feature-scaling, feature-selection, classifier, score, train-time, pred-time\n')
       cv = KFold(n = X.shape[0], n_folds=3, shuffle=True, random_state=12345)
       for name, steps, parameters in gen_pipeline_steps():
	       print "Doing Grid Search for ", name 
               pipeline = Pipeline(steps)
	       best_est, best_params, best_score1, time_taken = do_grid_search(pipeline, parameters, cv, X, Y)
	       Y_pred = best_est.predict(X_test)
               Y_train_pred = best_est.predict(X)
               print "train-error-Y", rmsle(Y, Y_train_pred) 
                 
               pipeline = Pipeline(steps)
	       best_est, best_params, best_score2, time_taken = do_grid_search(pipeline, parameters, cv, X, Y_cas)
	       Y_pred_cas = best_est.predict(X_test)
               Y_train_pred = best_est.predict(X)
               print "train-error-Y", rmsle(Y_cas, Y_train_pred) 
               

               pipeline = Pipeline(steps)
	       best_est, best_params, best_score3, time_taken = do_grid_search(pipeline, parameters, cv, X, Y_reg)
	       Y_pred_reg = best_est.predict(X_test)
               Y_train_pred = best_est.predict(X)
               print "train-error-Y", rmsle(Y_reg, Y_train_pred) 
               
               print '*' * 1000
               scores = '-'.join(map(lambda x : str(x), [best_score1, best_score2, best_score3]))
               do_kaggle_submission([Y_pred, Y_pred_cas, Y_pred_reg], X_datetime, str(scores) + "-" + name)
               '''fn = 'None' ; fs = 'None' ; clf = 'None' 
               splits = name.split(':')
               if len(splits) == 3:
                      fn, fs, clf = splits
               else:
                      fn, clf = splits
               fout.write(fn + ',' + fs + ',' + clf + ',' + str(best_score) + ',' + str(t1_train) + ',' + str(t1_test) + '\n')
               fout.flush() 
               print '-' * 30, '\n' '''
       fout.close()
       	
