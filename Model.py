
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import pickle

data_set= pd.read_csv('fichier_preprocessed.csv')


feature= data_set.iloc[:, [1,2]].values
target =  data_set.iloc[:, 3].values
X_train_list = [str(item) for item in feature.tolist()]
print(X_train_list)

# splitting into train and tests
X_train, X_test, Y_train, Y_test = train_test_split(X_train_list, target, test_size =.2, random_state=100)
print(X_train)
print(Y_train)


def SVM():
    pipe = make_pipeline(TfidfVectorizer(),
                     SVC())
    param_grid = {'svc__kernel': ['rbf', 'linear', 'poly'],
                'svc__gamma': [0.1, 1, 10, 100],
                'svc__C': [0.1, 1, 10, 100]}

    SVM = GridSearchCV(pipe, param_grid, cv=3,verbose=2)
    SVM.fit(X_train, Y_train)

    return SVM

SVM= SVM()

prediction = SVM.predict(X_test)
print(f"Accuracy score is {accuracy_score(Y_test, prediction):.2f}")
print(classification_report(Y_test, prediction))
pickle.dump(SVM, open('EntrainementSVM.sav', 'wb'))
