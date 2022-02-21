import matplotlib.pyplot as plt
import numpy as np
import statistics

a = input("enter file name(Except for .txt)\n")

f = open("%s.txt" % a, "r")
t = []
l = []
col = []
lsp = []
fast = []
out = []
steer = []
rat = []
step = []
mileage = []
env = []
avg = []
gamma = 0.99
s = 0  # 総ステップ回数
p = 0  # エピソードごとのステップ回数
timeout = 0
line = f.readline()
while line:
    n = list(map(str, line.split(":")))
    for i in range(len(n)):
        n[i] = n[i].strip()

    if len(n) > 7:
        if n[4] == "env steps":
            env.append(0)
            env[len(env) - 1] = int(n[5])
            avg.append(0)
            avg[len(avg) - 1] = float(n[7])

    if "回目" in n[0]:
        t.append(0)
        l.append(0)
        col.append(0)
        lsp.append(0)
        fast.append(0)
        out.append(0)
        steer.append(0)
        rat.append(0)
        step.append(p)
        p = 0
    if n[0] == "time":
        t[len(t) - 1] = float(n[1])
    if n[0] == "reward":
        l[len(l) - 1] += float(n[1])
        p += 1
        if p == 501:
            timeout += 1
        s += 1
    if n[0] == "r_collision":
        col[len(col) - 1] += float(n[1])
    if n[0] == "lspeed_lon":
        lsp[len(lsp) - 1] += float(n[1])
    if n[0] == "r_fast":
        fast[len(fast) - 1] += float(n[1])
    if n[0] == "r_out":
        out[len(out) - 1] += float(n[1])
    if n[0] == "r_steer":
        steer[len(steer) - 1] += float(n[1])
    if n[0] == "r_lat":
        rat[len(rat) - 1] += float(n[1])

    line = f.readline()
f.close()

step.pop(0)
step.append(0)

# リワードがなかったエピソードを削除
for i in reversed(range(len(l))):
    if l[i] == 0:
        del step[i]
        del t[i]
        del l[i]
        del col[i]
        del lsp[i]
        del fast[i]
        del out[i]
        del steer[i]
        del rat[i]
"""
mileage = [i * 0.1 for i in lsp]

misp = [x / y for (x, y) in zip(mileage, step)]
misp = [x * y for (x, y) in zip(misp, lsp)]  # 走行距離×速度
"""
cc = 0
oo = 0
colout = 0
for i in range(len(l)):
    if col[i] == -1:
        cc += 1  # 衝突回数
    if out[i] == -1:
        oo += 1  # コースアウト回数
    if col[i] == -1 or out[i] == -1:
        colout += 1

    """
    print("エピソード",i+1)
    print("走行距離",mileage[i])
    print("step",step[i])
    print("time",t[i])
    print('reward',l[i])
    print('col',col[i])
    print('lsp',lsp[i])
    print('fast',fast[i])
    print('out',out[i])
    print('steer',steer[i])
    print('rat',rat[i])
    """
print(l)
print("全エピソード数:", len(l))
print("全step数:", s)
print("衝突回数:", cc, "回", cc * 100 / len(l), "%")
print("コースアウト回数:", oo, "回", oo * 100 / len(l), "%")
print("タイムアウトによる終了回数:", timeout, "回", timeout * 100 / len(l), "%")
print("衝突もコースアウトもしなかった回数:", len(l) - colout, "回", (len(l) - colout) * 100 / len(l), "%")
print(
    "時間内に目的地に到達した回数:",
    len(l) - colout - timeout,
    "回",
    (len(l) - colout - timeout) * 100 / len(l),
    "%",
)

# 走行距離の平均
# mean = statistics.mean(mileage)
# print("平均走行距離:", mean)

x = [i for i in range(len(l))]
fig, axs = plt.subplots(3, 3, figsize=(15, 8), constrained_layout=True)
# axs[0,0].plot(x,l)
# axs[0,0].set_xlabel('episode')
# axs[0,0].set_ylabel('reward')
"""
axs[0, 0].plot(env, avg)
axs[0, 0].set_xlabel("step(≠time_step)")
axs[0, 0].set_ylabel("average return")
"""
axs[0, 0].plot(x, l)
axs[0, 0].set_xlabel("episode")
axs[0, 0].set_ylabel("reward")
axs[0, 1].plot(x, col)
axs[0, 1].set_xlabel("episode")
axs[0, 1].set_ylabel("r_collision")
axs[0, 2].plot(x, lsp)
axs[0, 2].set_ylabel("speed")
axs[1, 0].plot(x, fast)
axs[1, 0].set_ylabel("fast")
axs[1, 1].plot(x, out)
axs[1, 1].set_ylabel("out")
axs[1, 2].plot(x, steer)
axs[1, 2].set_ylabel("steer")
axs[2, 0].plot(x, rat)
axs[2, 0].set_ylabel("rat")
# axs[2,1].plot(x,t)
# axs[2,1].set_ylabel('time')
""""
axs[2, 1].plot(x, mileage)
axs[2, 1].set_ylabel("mileage")
axs[2, 2].plot(x, misp)
axs[2, 2].set_ylabel("speed*mileage")
"""
plt.show()
