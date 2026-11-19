import csv

rows = list(csv.DictReader(open("data/rideops_support_tickets.csv", encoding="utf-8")))

total = len(rows)
escalated = [r for r in rows if r["escalated_to_eng"] == "Yes"]

print("Total tickets:", total)
print("Escalated to engineering:", len(escalated))
print("Escalation rate: %.1f%%" % (100 * len(escalated) / total))

print()
print("Escalations by category:")
counts = {}
for r in escalated:
    counts[r["category"]] = counts.get(r["category"], 0) + 1
for cat, n in sorted(counts.items(), key=lambda x: -x[1]):
    print(" ", n, cat)
