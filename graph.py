import csv
import numpy as np
import matplotlib.pyplot as plt

fname = input("insert ID >>") + ".csv"

with open(fname) as f:
    reader = csv.reader(f)
    l = [row for row in reader]

def seconds(times):
    if times.count(":") == 1:
        m,s = times.split(":")
        second = int(s) + (int(m) * 60)
    else:
        h,m,s = times.split(":")
        second = int(s) + (int(m) * 60) + (int(h) * 3600)
    return second


interval = 60

last = l[-1][0]
cut_time = seconds(last) // interval

x = np.linspace(0, seconds(last), cut_time)
y = []

start = 0
count = 0
for i in range(cut_time):
    for lists in l:
        if seconds(lists[0]) >= interval*i and seconds(lists[0]) < interval*(i+1):
            if "草" in lists[1]:
                count += 1
    y.append(count)
    count = 0

fig = plt.figure()
plt.title("Highlight", fontsize=24)
plt.xlabel("times(s)", fontsize=24)
plt.ylabel("count", fontsize=24)
plt.grid(True)
plt.plot(x, y, marker="o")
fig.set_size_inches(15, 5)
plt.show()