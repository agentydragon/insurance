# Helper for some tests
import sys
import fileinput
from insurance import Data
dataset = Data()
dataset.load(sys.stdin)

# Find customers that chose a weirdo product
n = 0
for customer in dataset.customers.values():
  if not customer.did_choose_browsed_plan:
    print(customer.customer_id)
    n += 1

print()
print("%d of %d customers chose an unbrowsed product" % (n, len(dataset.customers)))
