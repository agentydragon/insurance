# This model selects the most likely of the quoted plans.
# The likelihood is determined by the product of class scores on trained SVMs.


import sys
import fileinput
from sklearn import svm, metrics
from sklearn.externals import joblib

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
#   - stane se nekdy, ze si vyberu pojisteni, jehoz nejaky flag jsem si nenechal nikdy naquotovat?

# TODO: vyzkouset:
#   - nejaka ta chytra volba parametru
#   - jeden velky klasifikator?

# TODO: je dobry napad tomu klasifikatoru davat jako vstup i prvni a posledni
# quote, i kdyz ten klasifikator ma zhodnocovat jejich pravdepodobnost?

# TODO: deterministicke experimenty?

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

  data.append(len(customer.points))

  return data

# An attempt to automatically find the cases that don't choose what they
# browsed. This doesn't happen a lot, through, so it's dropped for now.
##  # TODO: normalizovat data na 0-1
##  def train_chosen_browsed_plan():
##    print("Training chosen-browsed-plan classifier.")
##    data = list(map(customer_to_data, dataset.customers.values()))
##    target = list(map(lambda c: c.did_choose_browsed_plan, dataset.customers.values()))
##  
##    n = int(len(data) * 0.8)
##  
##    nlc_classifier = svm.SVC(gamma=0.01)
##    nlc_classifier.fit(data[:n], target[:n])
##    predicted = nlc_classifier.predict(data[n:])
##    print("Classifier report for %s:\n%s\n" % (nlc_classifier, metrics.classification_report(target[n:], predicted))) 
##    joblib.dump(nlc_classifier, "trained/nlc_classifier.pkl")

def train_attribute_classifiers():
  print("Training attribute classifiers.")
  classifiers = []
  data = list(map(customer_to_data, dataset.customers.values()))
  n = int(len(data) * 0.8)
  for i in range(0, 7):
    print("Training classifier of parameter %d/7" % (i + 1))

    target = list(map(lambda c: c.selected_plan[i], dataset.customers.values()))

    classifier = svm.SVC(gamma=0.01, probability=True)

    print("Training on %d samples." % (n))
    classifier.fit(data[:n], target[:n])
    predicted = classifier.predict(data[n:])
    # print(predicted)
    print("Classifier report for %s:\n%s\n" % (classifier, metrics.classification_report(target[n:], predicted)))
    classifiers.append(classifier)
  joblib.dump(classifiers, "trained/svcs.pkl")

if len(sys.argv) > 1 and sys.argv[1] == '--train':
  #train_chosen_browsed_plan()
  train_attribute_classifiers()
else:
  # Load the model.
  classifiers = joblib.load("trained/svcs.pkl")
  print("Running.", file=sys.stderr)

  for customer in dataset.customers.values():
    plan = []
    data = customer_to_data(customer)

    probs = []
    for i in range(0,7):
      probs.append(classifiers[i].predict_proba(data)[0])

    best, best_score = None, None

    for point in customer.points:
      score = 1.0
      for i in range(0,7):
        score *= probs[i][point.plan[i]]

      print("%s: score %f" % (str(point.plan), score), file=sys.stderr)
      if best == None or score > best_score:
        best = list(point.plan)
        best_score = score
    print(file=sys.stderr)

    customer.selected_plan = best

    # Select best hypothesis of each classifier:
    ###  for i in range(0,7):
    ###    plan.append(classifiers[i].predict(data)[0]) # 1
    ###  # customer.selected_plan = [1, 1, 1, 1, 1, 1, 1]
    ###
    ###  customer.selected_plan = plan

  dataset.export_results(sys.stdout)
