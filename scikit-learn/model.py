import sys
import fileinput
from sklearn import svm, metrics

# A: 0/1/2
# B: 0/1
# C: 1/2/3/4
# D: 1/2/3
# E: 0/1
# F: 0/1/2/3
# G: 1/2/3/4

print("Loading input.")

from insurance import Data
dataset = Data()
dataset.load(sys.stdin)

class MyDataset:
    def __init__(self, dataset, target_extract_function):
        data = []
        target = []

        for customer in dataset.customers.values():
            p = customer.points[0]

            data.append([p.day, p.group_size, p.homeowner, p.car_age, p.age_oldest, p.age_youngest, p.married_couple])
            target.append(target_extract_function(customer))

        self.data = data
        self.target = target

if sys.argv[1] == '--train':
    print("Training on given data.")

    ds = MyDataset(dataset, lambda c: c.selected_plan[0])
    classifier = svm.SVC(gamma=0.01)

    n = len(ds.data) // 2
    print("Training on %d samples." % (n))
    classifier.fit(ds.data[:n], ds.target[:n])
    predicted = classifier.predict(ds.data[n:])
    # print(predicted)
    print("Classifier report for %s:\n%s\n" % (classifier, metrics.classification_report(ds.target[n:], predicted)))

    # TODO: train & save
else:
    # TODO: load model
    print("Running.")

    for cid, customer in dataset.customers.iteritems():
        # TODO: predict from model
        customer.selected_plan = [1, 1, 1, 1, 1, 1, 1]

    dataset.export_results(sys.stdout)
