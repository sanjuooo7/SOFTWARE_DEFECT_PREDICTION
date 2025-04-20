import csv
# from sklearn.neighbors import KNeighborsClassifier

x=[]
y=[]
dlabels=[]

with open('jm1.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    i=0
    for lines in csvFile:
        # print(lines)

        if i!=0:
            r=[]
            for j in range(21):
                if lines[j] == "?":
                    r.append(float(0))
                else:
                    r.append(float(lines[j]))
            x.append(r)
            if lines[7] not in dlabels:
                dlabels.append(lines[21])

            y.append(dlabels.index(lines[21]))
        i=i+1
print(x)
print(dlabels)
print(y)

# print(x[0])
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
# print(scaler,"ggggggggggggggggggggggg")
scaler.fit(x)
# print(scaler.fit(x))

# print(scaler.data_max_)

x=scaler.transform(x)
# print(x,"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
# neigh =linear_model.LogisticRegression()
# neigh = KNeighborsClassifier(n_neighbors=3)
# print(neigh,"kkkkkkkkkkkkkkkkkkkkk")
# f=neigh.fit(X_train, y_train)
# print(f)


# y_pred=neigh.predict(X_test)
# print("output")
# print(y_pred)
# print(y_test)

# from sklearn.metrics import accuracy_score
# # from sklearn.metrics import classification_report
# from sklearn.metrics import confusion_matrix
#
# print(accuracy_score(y_test, y_pred))
# # print(classification_report(y_test, y_pred))
# print(confusion_matrix(y_test, y_pred))


print("=================================")
print("=================================")
print("=================================")
#decision tree
from sklearn.tree import DecisionTreeClassifier
dtree = DecisionTreeClassifier()
dtree = dtree.fit(X_train, y_train)
y_pred=dtree.predict(X_test)
print(y_pred)
print(y_test)
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
# svm
from sklearn import svm
clf = svm.SVC()
clf.fit(X_train, y_train)
y_pred=clf.predict(X_test)
#
# print(y_pred)
# print(y_test)
#
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import classification_report
# from sklearn.metrics import confusion_matrix
#
print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
