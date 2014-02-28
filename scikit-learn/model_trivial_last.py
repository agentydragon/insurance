import sys
import fileinput
from insurance import Data

# Trivialni reseni: rekni posledni prohlizenou polozku
# (submission 2, score 0.53793)

dataset = Data()
dataset.load(sys.stdin)

if len(sys.argv) > 1 and sys.argv[1] == '--train':
  print("NOP.")
else:
  print("Running.", file=sys.stderr)

  for customer in dataset.customers.values():
    customer.selected_plan = customer.points[-1].plan

  dataset.export_results(sys.stdout)
