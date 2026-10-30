import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# 当前 Python 文件所在的目录
folder = Path(__file__).resolve().parent


def load_data(filename):
    path = folder / filename

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    t = np.array([float(row["t"]) for row in rows])
    y = np.array([float(row["y"]) for row in rows])
    delta = np.array([float(row["delta"]) for row in rows])

    print(filename, "数据点数：", len(t))

    return t, y, delta


# 读取两组实验数据
t_pd, y_pd, delta_pd = load_data("pd_tracking.csv")
t_p, y_p, delta_p = load_data("p_tracking.csv")


# 计算性能指标
def evaluate(y):
    rmse = np.sqrt(np.mean(y ** 2))
    max_error = np.max(np.abs(y))
    final_error = np.abs(y[-1])

    return rmse, max_error, final_error


print("PD 控制:", evaluate(y_pd))
print("P 控制:", evaluate(y_p))

# 计算调节时间和最大转向角变化率
def extra_metrics(t, y, delta, tolerance=0.05):

    # 找出误差超出 ±0.05 m 的所有时刻
    outside = np.where(np.abs(y) > tolerance)[0]

    if len(outside) == 0:
        settling_time = t[0]
    elif outside[-1] == len(y) - 1:
        settling_time = None
    else:
        settling_time = t[outside[-1] + 1]

    # 计算相邻采样点之间的转向角变化率
    delta_rate = np.diff(delta) / np.diff(t)

    max_rate = np.max(np.abs(delta_rate))

    return settling_time, max_rate


for name, t, y, delta in [
    ("P", t_p, y_p, delta_p),
    ("PD", t_pd, y_pd, delta_pd)
]:
    settling, max_rate = extra_metrics(t, y, delta)

    print(name, "调节时间:", settling)
    print(name, "最大转向角变化率:", max_rate, "rad/s")


# 绘制横向跟踪误差
plt.figure(figsize=(9, 5))

plt.plot(t_pd, y_pd, label="PD Control")
plt.plot(t_p, y_p, label="P Control")

plt.axhline(0, color="black", linestyle="--", label="Reference")

plt.xlabel("Time (s)")
plt.ylabel("Lateral Error (m)")
plt.title("Lateral Tracking Error Comparison")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(folder / "tracking_error_comparison.png", dpi=200)


# 绘制转向角变化
plt.figure(figsize=(9, 5))

plt.plot(t_pd, delta_pd, label="PD Control")
plt.plot(t_p, delta_p, label="P Control")

plt.xlabel("Time (s)")
plt.ylabel("Steering Angle (rad)")
plt.title("Steering Control Comparison")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(folder / "steering_comparison.png", dpi=200)
plt.show()