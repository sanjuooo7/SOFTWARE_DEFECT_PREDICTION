import csv

from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np
x=[]
y=[]
dlabels=[]

with open(r'C:\Users\hp\PycharmProjects\myproject\my_app\jm1.csv', mode ='r')as file:
# with open('C:\\Users\\hp\\PycharmProjects\\myproject\\my_app\\jm1.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    i=0
    for lines in csvFile:
        # print(lines)

        if i!=0:
            r=[]
            for j in range(21):
                if lines[j] == "?":
                    r.append(float(lines[0]))
                else:

                    r.append(float(lines[j]))
            x.append(r)
            if lines[21] not in dlabels:
                dlabels.append(lines[21])

            y.append(dlabels.index(lines[21]))
        i=i+1
print(x)
print(dlabels)
print(y)




def random_forest(t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21):
    from sklearn.model_selection import train_test_split

    from sklearn.metrics import accuracy_score
    from sklearn.metrics import classification_report
    from sklearn.metrics import confusion_matrix

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    rfc = RandomForestClassifier()
    rfc.fit(x,y)


    rfc_predict = rfc.predict(X_test)
    print(dlabels)
    print("----------------------------------")
    print(dlabels[rfc_predict[0]])
    ab = rfc.score(X_test, y_test)

    #
    print(accuracy_score(y_test, rfc_predict))
    print(classification_report(y_test, rfc_predict))
    print(confusion_matrix(y_test, rfc_predict))
    return str(dlabels[rfc_predict[0]])




print("Predicted Result=================")
print(random_forest(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1))