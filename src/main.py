# Required : lightgbm, pandas and sklearn

import lightgbm as lgb
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
import scipy.stats
import sys
import numpy as np
from catboost import CatBoostRegressor
import matplotlib.pyplot as plt

use_trunc = True
path_feat = '../smhpdata/full-data/matched_output.csv'
path_trunc = 'matched_output_trucated_feature.csv'
only_features = False
out_dgbm = False
catb = False

if not use_trunc:
    cols_to_drop = [0, 1, 4, 10, 11, 12, 13, 14, 15]
    data = pd.read_csv(path_feat, header = None)
    data = data.drop(cols_to_drop, axis = 1)
    data.reset_index(drop=True, inplace=True)
    data.to_csv(path_trunc)
    sys.exit()
else:
    # remove header row manually
    data = pd.read_csv(path_trunc, header = None)

sz = len(data)
idx = int(0.98*sz)

df_train = data[:idx]
df_test = data[idx:]

col_idx = [7]
y_train = df_train[col_idx]
y_test = df_test[col_idx]
X_train = df_train.drop(col_idx, axis=1)
X_test = df_test.drop(col_idx, axis=1)

if only_features:
    # make sure that the dataset being used has feautres
    # Last 9 columns have features.
    X_train = X_train[X_train.columns[-9:]]
    X_test = X_test[X_test.columns[-9:]]
    X_train[[270]] = X_train[[270]].apply(np.log)
    X_test[[270]] = X_test[[270]].apply(np.log)

    # Plotting
    # X_train['lab'] = y_train
    # ab = X_train.corr(method='spearman')
    # corr_matrix = np.corrcoef(ab).round(decimals=2)

    # fig, ax = plt.subplots()
    # im = ax.imshow(corr_matrix)
    # ax.xaxis.set(ticks=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9), ticklabels=('ispro', 'canbuypro', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'log_views', 'labels'))
    # ax.yaxis.set(ticks=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9), ticklabels=('ispro', 'canbuypro', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'log_views', 'labels'))
    # for i in range(10):
    #     for j in range(10):
    #         ax.text(j, i, corr_matrix[i, j], ha='center', va='center',
    #                 color='r')
    # cbar = ax.figure.colorbar(im, ax=ax, format='% .2f')
    # plt.show()



if out_dgbm:
    np.save('npys/train_features.npy', X_train.to_numpy())
    np.save('npys/train_labels.npy', y_train.to_numpy())
    np.save('npys/test_features.npy', X_test.to_numpy())
    np.save('npys/test_labels.npy', y_test.to_numpy())
    print("DEEPgbmised.")
    sys.exit()


if catb:
	model = CatBoostRegressor(iterations=50, learning_rate=0.1, depth=10)	

	model.fit(X_train, y_train)
	y_pred = model.predict(X_test)

	print('The mse of prediction is :', mean_squared_error(y_test, y_pred))
	print('The mae of prediction is :', mean_absolute_error(y_test, y_pred))
	print('the SRC of prediction is : ', scipy.stats.spearmanr(y_test, y_pred)[0])
	sys.exit()


# sys.exit()
# create dataset for lightgbm
lgb_train = lgb.Dataset(X_train, y_train)
lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

# regressing over the dataset 
params = {
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': {'l2', 'l1'},
    'num_leaves': 80,
    'learning_rate': 0.05,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.9,
    'bagging_freq': 5,
    'num_iteration' : 100,
    # 'max_bin' : 1000,
    'verbose': 0
}

# train
gbm = lgb.train(params,
                lgb_train,
                num_boost_round=20,
                valid_sets=lgb_eval,
                early_stopping_rounds=5)

gbm.save_model('model_file.txt')
y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)

print('The mse of prediction is :', mean_squared_error(y_test, y_pred))
print('The mae of prediction is :', mean_absolute_error(y_test, y_pred))
print('the SRC of prediction is : ', scipy.stats.spearmanr(y_test, y_pred)[0])
