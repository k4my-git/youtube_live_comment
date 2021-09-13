import csv
import numpy as np
import matplotlib.pyplot as plt

fname = input("insert ID >>")
word = input("insert Word >>")
interval = int(input("insert interval >>"))

with open("data/"+fname+".csv") as f:
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

    
last = l[-1][0]
cut_time = seconds(last) // interval

x = np.linspace(0, seconds(last), cut_time)
y = []

start = 0
count = 0

for i in range(cut_time):
    for lists in l:
        if seconds(lists[0]) >= interval*i and seconds(lists[0]) < interval*(i+1):
            if word in lists[1]:
                count += 1
    y.append(count)
    count = 0

dic = {}
for i in range(len(x)):
    key = int(x[i]) - interval
    dic[key] = y[i]
dic2 = dict(sorted(dic.items(), key=lambda x:x[1], reverse=True))

print("Ranking by"+word)
rank = 1
for i in range(3):
    url = 'https://youtu.be/'+fname+'?t='+str(list(dic2.keys())[i])
    print(str(rank)+"st "+url)
    rank += 1

fig = plt.figure()
plt.title("Highlight", fontsize=24)
plt.xlabel("times(s)", fontsize=24)
plt.ylabel("count", fontsize=24)
plt.grid(True)
plt.plot(x, y, marker="o", color = "blue")
fig.set_size_inches(15, 5)
fig.tight_layout()
#plt.savefig(fname+'.png')
plt.show()

