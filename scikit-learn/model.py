import sys
import fileinput
import csv

# A: 0/1/2
# B: 0/1
# C: 1/2/3/4
# D: 1/2/3
# E: 0/1
# F: 0/1/2/3
# G: 1/2/3/4

class ShoppingPoint:
    def load(self, row):
        customer_id, shopping_pt_num, record_type, day, time, state, location, group_size, homeowner, car_age, car_value, risk_factor, age_oldest, age_youngest, married_couple, c_previous, duration_previous, a, b, c, d, e, f, g, cost = row

        self.customer_id = int(customer_id)
        self.shopping_pt_num = int(shopping_pt_num) # 1..x
        self.record_type = int(record_type) # 0 = quote, 1 = buy
        self.day = int(day) # 0..6
        self.time = time # TODO: xx:yy
        self.state = state # TODO: state ID

        if location == 'NA':
            self.location = 0 # TODO
        else:
            self.location = int(location)

        self.group_size = int(group_size)
        self.homeowner = int(homeowner) # 0..1
        self.car_age = int(car_age) # 0..
        self.car_value = car_value # TODO: g/e/c/...?

        if risk_factor == 'NA':
            self.risk_factor = 0 # TODO: lepsi handling N/A
        else:
            self.risk_factor = int(risk_factor)

        self.age_oldest = int(age_oldest)
        self.age_youngest = int(age_youngest)
        self.married_couple = int(married_couple) # 0..1

        if c_previous == 'NA':
            self.c_previous = 0 # TODO: lepsi N/A
        else:
            self.c_previous = int(c_previous) # previous C-value

        if duration_previous == 'NA':
            self.duration_previous = 0
        else:
            self.duration_previous = int(duration_previous)

        if a != 'NA': self.a = int(a)
        if b != 'NA': self.b = int(b)
        if c != 'NA': self.c = int(c)
        if d != 'NA': self.d = int(d)
        if e != 'NA': self.e = int(e)
        if f != 'NA': self.f = int(f)
        if g != 'NA': self.g = int(g)
        self.cost = int(cost)

    def plan(self):
        return [self.a, self.b, self.c, self.d, self.e, self.f, self.g]

class Customer:
    def __init__(self, id):
        self.points = []
        self.selected_plan = None

    def insert_shopping_point(self, point):
        self.points.append(point)

        if point.record_type == 1:
            self.selected_plan = point.plan()

    def export_selected_plan(self):
        return ''.join(map(str, self.selected_plan))

class Data:
    def __init__(self):
        self.customers = {}

    def insert_row(self, row):
        point = ShoppingPoint()
        point.load(row)
        if not point.customer_id in self.customers:
            self.customers[point.customer_id] = Customer(point.customer_id)
        self.customers[point.customer_id].insert_shopping_point(point)

    def load(self, f):
        reader = csv.reader(f, delimiter=',')

        for row in reader:
            if row[0] == 'customer_ID': # skip
                next
            else:
                self.insert_row(row)

        print("Input loaded.")

    def export_results(self, f):
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['customer_ID', 'plan'])
        
        for cid, customer in self.customers.iteritems():
            writer.writerow([cid, customer.export_selected_plan()])

print("Loading input.")

dataset = Data()
dataset.load(sys.stdin)

if sys.argv[0] == '--train':
    print("Training on given data.")
    # TODO: train & save
else:
    # TODO: load model
    print("Running.")

    for cid, customer in dataset.customers.iteritems():
        # TODO: predict from model
        customer.selected_plan = [1, 1, 1, 1, 1, 1, 1]

    dataset.export_results(sys.stdout)

