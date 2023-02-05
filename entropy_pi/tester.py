import subprocess
import matplotlib.pyplot as plt
import os
import math

NET7 = False # replace with True if using .Net 7 (e.g. for Linux)

NET7 = "dotnet " if NET7 else ""

def error(n):
    return abs(n - math.pi) / math.pi


def calculate_pi(mutation=1, relative=True, n=10):
    results = []

    relative = r'\r' if relative else ''
    root = os.getcwd()
    os.chdir("Entropy/")

    subprocess.call(f"entc.exe {relative} /m {mutation} {root}/task.en > {root}/error.txt", shell=True)

    for _ in range(10):
        subprocess.call(f"{NET7}task.exe > {root}/calculated_pi.txt", shell=True)
        r = open(f"{root}/calculated_pi.txt", encoding='utf-8').read().strip()
        
        if r == "Infinity":
            r = "inf"
        elif r == "-Infinity":
            r = "-inf"
        try:
            results.append(float(r))
        except ValueError:
            print("Bad float:", r)
            results.append(float("nan"))

    os.remove("task.exe")
    os.chdir(root)

    # print(open("error.txt", encoding='utf-8').read())
    return results


mutations = [0, 0.001, 0.01, 0.05, 0.1, 0.2, 0.4, 0.7, 1.0, 2]
mutations = list(map(str, mutations))
data = [[], []]

relative = True

for m in mutations:
    res = calculate_pi(m, relative)
    res = list(map(error, res))
    res.sort()

    best = sum(res[:5]) / 5
    average = sum(res) / len(res)

    data[0].append(best)
    data[1].append(average)
    print(m)

#plt.plot(mutations, data[0], '-o', label="Absolute best")
#plt.plot(mutations, data[1], '-o', label="Absolute average")
plt.fill_between(mutations, data[0], data[1], color="#F5DFBF")
plt.plot(mutations, data[0], '-o', label="Best")
plt.plot(mutations, data[1], '-o', label="Average")


plt.legend()
plt.xlabel("Mutation rate")
plt.ylabel("Relative error")
plt.yscale("log")
plt.show()
