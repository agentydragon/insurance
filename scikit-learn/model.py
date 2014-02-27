import sys
from sklearn import svm, metrics
from sklearn.externals import joblib

# A: 0/1/2
# B: 0/1
# C: 1/2/3/4
# D: 1/2/3
# E: 0/1
# F: 0/1/2/3
# G: 1/2/3/4

print("Loading input.", file=sys.stderr)

from insurance import Data
dataset = Data()
dataset.load(sys.stdin)

# Napady:
#   - zkusit tomu dat za vstup tu hodnotu parametru, ktera dostala nejmensi cenu.
#   - u kolika zakazniku vubec dochazi k nejakym zmenam?
#   - identifikovat obvykle kombinace.
#   - nejak do toho zahrnout i cenu.
#   - nejak do toho zahrnout bool flagy, jake veci jsem si prohledl.

# TODO: vyzkouset:
#   - nejaka ta chytra volba parametru
#   - jeden velky klasifikator?

def customer_to_data(customer):
  data = []

  p = customer.points[0]
  data.extend([p.day, p.group_size, p.homeowner, p.car_age, p.age_oldest, p.age_youngest, p.married_couple])
  # zajimave... on tomu cost moc nepridava...
  data.extend([p.a, p.b, p.c, p.d, p.e, p.f, p.g]) #, p.cost])

  # Further attributes:
  #   - time
  #   - state
  #   - location
  #   - risk_factor
  #   - c_previous
  #   - duration_previous
  #   - cost

  p = customer.points[-1]
  data.extend([p.a, p.b, p.c, p.d, p.e, p.f, p.g]) # , p.cost])

  return data

class MyDataset:
  def __init__(self, dataset, target_extract_function):
    data = []
    target = []

    for customer in dataset.customers.values():
      data.append(customer_to_data(customer))
      target.append(target_extract_function(customer))

    self.data = data
    self.target = target

if len(sys.argv) > 1 and sys.argv[1] == '--train':
  print("Training on given data.")

  classifiers = []

  for i in range(0, 7):
    print("Training classifier of parameter %d/7" % (i + 1))
    ds = MyDataset(dataset, lambda c: c.selected_plan[i])
    classifier = svm.SVC(gamma=0.01)

    n = len(ds.data) // 2
    print("Training on %d samples." % (n))
    classifier.fit(ds.data[:n], ds.target[:n])
    predicted = classifier.predict(ds.data[n:])
    # print(predicted)
    print("Classifier report for %s:\n%s\n" % (classifier, metrics.classification_report(ds.target[n:], predicted)))
    classifiers.append(classifier)

  joblib.dump(classifiers, "trained/svcs.pkl")
else:
  # Load the model.
  classifiers = joblib.load("trained/svcs.pkl")
  print("Running.", file=sys.stderr)

  for customer in dataset.customers.values():
    plan = []
    data = customer_to_data(customer)

    for i in range(0,7):
      plan.append(classifiers[i].predict(data)[0]) # 1
    # customer.selected_plan = [1, 1, 1, 1, 1, 1, 1]

    customer.selected_plan = plan

  dataset.export_results(sys.stdout)
