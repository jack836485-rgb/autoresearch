"""随机奖励在直接 logit（softmax）参数化下的二阶漂移与“胜出”频率核对。

用途：支撑 IDEA-008 的关键方向（主导模式被压低、胜出频率比初始质量更平）。
只用 numpy，CPU 几分钟。运行：python softmax_drift_check.py
"""
import numpy as np

rng = np.random.default_rng(1)


def sm(z):
    e = np.exp(z - z.max())
    return e / e.sum()


def second_order_drift(p, h=1e-4):
    """E[Δp] 的二阶项（单位 η²c/G）：0.5 * tr(∇²p_m · J)，J = diag(p) - p pᵀ。"""
    k = len(p)
    z = np.log(p)
    jac = np.diag(p) - np.outer(p, p)
    out = np.zeros(k)
    eye = np.eye(k)
    for m in range(k):
        hess = np.zeros((k, k))
        for i in range(k):
            for j in range(k):
                ei, ej = eye[i] * h, eye[j] * h
                hess[i, j] = (sm(z + ei + ej)[m] - sm(z + ei - ej)[m]
                              - sm(z - ei + ej)[m] + sm(z - ei - ej)[m]) / (4 * h * h)
        out[m] = 0.5 * np.sum(hess * jac)
    return out


def closed_form(p):
    s2, s3 = np.sum(p ** 2), np.sum(p ** 3)
    return p * ((0.5 + s2) * (p - s2) - 1.5 * (p ** 2 - s3))


def run(p0, steps, eta, group, normalize):
    z = np.log(p0).copy()
    k = len(p0)
    eye = np.eye(k)
    for _ in range(steps):
        p = sm(z)
        ys = rng.choice(k, size=group, p=p)
        if normalize:
            r = rng.integers(0, 2, size=group).astype(float)
            sd = r.std()
            if sd < 1e-6:
                continue
            adv = (r - r.mean()) / sd
        else:
            adv = rng.choice([-1.0, 1.0], size=group)
        z += eta * (adv[:, None] * (eye[ys] - p)).sum(0) / group
    return sm(z)


if __name__ == "__main__":
    for p in [np.array([0.5, 0.3, 0.2]), np.array([0.6, 0.3, 0.1]),
              rng.dirichlet(np.ones(5))]:
        d = second_order_drift(p)
        print("p", p.round(3), "二阶漂移", d.round(5),
              "闭式误差", np.abs(d - closed_form(p)).max().round(8))
    p0 = np.array([0.6, 0.3, 0.1])
    for normalize, eta, steps in [(False, 0.3, 4000), (True, 0.15, 12000)]:
        fins = np.array([run(p0, steps, eta, 4, normalize) for _ in range(400)])
        wins = np.bincount(fins.argmax(1), minlength=3) / 400
        print("组内标准化", normalize, "胜出频率", wins, "初始", p0,
              "最大概率均值", fins.max(1).mean().round(3))
