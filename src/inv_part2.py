# -*- coding: utf-8 -*-
"""
《不变子空间》下集 —— 实战：命题 6.6.2 + 例 6.6.2 + 例 6.6.4（苏州大学）
风格：Manim 宋体定理片（与上集同一套组件库 inv_lib.py）

★ 下集结构（按用户 2026-09-24 要求）：
  - 不做全片大知识地图；每道大题开讲前，先来一张「思路导图」（逐节点快速长出）
  - 每个定理/命题/例题：先抄题，再逐步证明，一行不跳

渲染：
  manim src/inv_part2.py Part2 -ql --media_dir ./media     # 低清预览
  manim src/inv_part2.py Part2 -pqh --media_dir ./media    # 1080p60
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inv_lib import *
from inv_lib import _nlabel  # 下划线私有名不会被 import * 带入，需显式导入


# ============================================================
# 思路导图数据（小导图：每题 4~6 个节点，快速长出）
# ============================================================
def _root(text, size=34):
    return Text(text, font=SONG, font_size=size, color=MAP_TXT, weight="BOLD")


def map_data_ex662():
    return {
        "node": _root("例 6.6.2 · 打法"),
        "child": [
            {"node": _nlabel(("t", "① 用 "), ("m", r"AB=BA"),
                             ("t", "：特征子空间互相不变"))},
            {"node": _nlabel(("t", "② 缩进 "), ("m", r"V_\lambda"),
                             ("t", " 里找"))},
            {"node": _nlabel(("t", "③ "), ("m", r"B|_{V_\lambda}"),
                             ("t", " 必有复特征值"))},
            {"node": _nlabel(("t", "④ 公共特征向量到手"))},
        ],
    }


def map_data_ex664():
    return {
        "node": _root("例 6.6.4 · 打法"),
        "child": [
            {"node": _nlabel(("t", "① 老路卡住："), ("m", r"Ad\neq 0"))},
            {"node": _nlabel(("t", "② 先证："), ("m", r"A"),
                             ("t", " 特征值全为 0")), "child": [
                {"node": _nlabel(("t", "迹转圈 "),
                                 ("m", r"\operatorname{tr}(A^k)=0"))},
                {"node": _nlabel(("t", "范德蒙 "), ("m", r"\Rightarrow"),
                             ("t", " 重数全 "), ("m", r"0"))},
            ]},
            {"node": _nlabel(("t", "③ "), ("m", r"V_0=\ker A"),
                             ("t", " 是 "), ("m", r"B"), ("t", " 不变"))},
            {"node": _nlabel(("t", "④ 在 "), ("m", r"B|_{V_0}"),
                             ("t", " 里找特征向量"))},
        ],
    }


class Part2(BaseScene):

    # ============================================================
    def construct(self):
        self.begin()
        self.s1_open()
        self.ch1_prop662()
        self.ch2_example662()
        self.ch3_example664()
        self.s_end()

    # ---------- 思路导图页（下集新镜头，每道大题一次） ----------
    def mini_map_page(self, data, head_text, sub_text, color=GOLD,
                      node_rt=0.34, hold=1.3):
        mm, i2n = build_mini_map(data)
        self.hard_clear()
        bar = self.head(head_text, color=color)
        self.grow_map(i2n, node_rt=node_rt, order=sorted(i2n.keys()))
        self.wait(0.5)
        self.sub_in(sub_text, 0.3)
        self.wait(hold)
        self.wipe()

    # ============================================================
    # 片头（下集：快速接上，无大地图）
    # ============================================================
    def s1_open(self):
        t1 = Text("抖音粉丝点题 · 高等代数", font=SONG, font_size=34,
                  color=RED, weight="BOLD")
        t1.move_to([0, 2.45, 0])
        t2 = song("不变子空间 · 下集", size=92, color="#8B8BE8")
        t2.move_to([0, 0.9, 0])
        t2.set_stroke(WHITE, 2, background=True)
        r1 = mixed(("t", "上集：定义 · 三兄弟 · 根子空间 · 范德蒙拆解", GRAY),
                   ts=34, ms=40)
        r1.move_to([0, -0.85, 0])
        r2 = mixed(("t", "今天全是实战 —— ", INK), ("t", "两道考研真题", RED),
                   ts=42, ms=48)
        r2.move_to([0, -1.85, 0])
        self.play(Write(t1), run_time=0.8)
        self.play(Write(t2), run_time=1.0)
        self.play(Write(r1), run_time=0.7)
        self.play(Write(r2), run_time=0.8)
        self.reg(t1, t2, r1, r2)
        self.sub_in("工具上集全备齐了，直接开打", 0.3)
        self.wait(1.4)
        self.wipe()

    # ============================================================
    # 第1章  命题 6.6.2（下集全靠它）
    # ============================================================
    def ch1_prop662(self):
        # ---- 抄题 ----
        bar = self.head("命题 6.6.2", color=BLUE)
        rows = [
            mixed(("m", r"\mathcal{A},\ \mathcal{B}", INK),
                  ("t", " 是线性空间 ", INK), ("m", r"V", INK),
                  ("t", " 上的两个线性变换，", INK), ts=34, ms=44),
            mixed(("t", "满足 ", INK), ("m", r"\mathcal{A}\mathcal{B}=\mathcal{B}\mathcal{A}", RED),
                  ("t", "．", INK), ts=34, ms=48),
            mixed(("t", "则 ", INK), ("m", r"\mathcal{A}", GOLD),
                  ("t", " 的特征子空间都是 ", INK),
                  ("m", r"\mathcal{B}", GOLD),
                  ("t", " 的不变子空间．", GOLD), ts=34, ms=44),
        ]
        card = problem_card("命题 6.6.2（教材原文）", rows, color=BLUE)
        card.move_to([0, 0.55, 0])
        self.show_rows([card], rt=1.5)
        self.wait(0.7)
        self.sub_in("下集两道大题，全靠这条命题打头阵", 0.3)
        self.wait(1.5)
        self.wipe()

        # ---- 证明 · 第一页 ----
        self.head("证明 · 第一步", color=BLUE)
        rows1 = [
            mixed(("t", "① 任取 ", INK), ("m", r"\mathcal{A}", INK),
                  ("t", " 的特征值 ", INK), ("m", r"\lambda", RED),
                  ("t", "，对应特征子空间 ", INK), ("m", r"V_\lambda", RED),
                  ts=34, ms=46),
            mixed(("t", "② ", INK), ("m", r"\forall\,d\in V_\lambda", INK),
                  ("t", "，则 ", INK), ("m", r"\mathcal{A}d=\lambda d", INK),
                  ts=34, ms=46),
            mixed(("t", "③ 下证：", INK), ("m", r"\mathcal{B}(d)\in V_\lambda", GOLD),
                  ts=34, ms=46),
            mixed(("m", r"(\mathcal{A}-\lambda E)\,\mathcal{B}(d)"
                        r"=\mathcal{A}\mathcal{B}d-\lambda\mathcal{B}(d)", INK),
                  ts=34, ms=44),
        ]
        flow1 = VGroup(*rows1).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        flow1.move_to([0, 0.35, 0])
        for r in rows1:
            self.play(Write(r), run_time=0.75)
            self.reg(r)
        self.wait(0.8)
        self.sub_in([("t", "目标是算出 "), ("m", r"(A-\lambda E)\,\mathcal{B}(d)"),
                     ("t", "，看它落不落在 "), ("m", r"V_\lambda"), ("t", " 里")], 0.3)
        self.wait(1.4)
        self.wipe()

        # ---- 证明 · 第二页（关键交换） ----
        self.head("证明 · 第二步（关键一换）", color=GOLD)
        rows2 = [
            mixed(("m", r"=\mathcal{B}\mathcal{A}d-\lambda\mathcal{B}(d)", INK),
                  ("t", "　← 用 ", INK), ("m", r"\mathcal{A}\mathcal{B}=\mathcal{B}\mathcal{A}", RED),
                  ts=34, ms=46),
            mixed(("m", r"=\lambda\,\mathcal{B}(d)-\lambda\mathcal{B}(d)=0", INK),
                  ("t", "　← 用 ", INK), ("m", r"\mathcal{A}d=\lambda d", RED),
                  ts=34, ms=46),
            mixed(("t", "⇒ ", INK), ("m", r"\mathcal{B}(d)\in\ker(\mathcal{A}-\lambda E)=V_\lambda", GREEN),
                  ts=34, ms=44),
            mixed(("t", "⇒ ", INK), ("m", r"V_\lambda", GOLD),
                  ("t", " 为 ", INK), ("m", r"\mathcal{B}", GOLD),
                  ("t", " 不变子空间　", INK), ts=34, ms=46),
        ]
        flow2 = VGroup(*rows2).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        flow2.move_to([0, 0.35, 0])
        for r in rows2:
            self.play(Write(r), run_time=0.75)
            self.reg(r)
        note = kaimix(("t", "两行交换，直接把 "), ("m", r"\mathcal{B}(d)"),
                      ("t", " 捡回 "), ("m", r"V_\lambda"), ("t", " 里"), ts=30, ms=34)
        note.move_to([0, -1.95, 0])
        nb = note_box(note)
        self.play(Write(nb), run_time=0.9)
        self.reg(nb)
        self.sub_in([("m", r"\mathcal{A}\mathcal{B}"), ("t", " 和 "),
                     ("m", r"\mathcal{B}\mathcal{A}"), ("t", " 能换位置，"),
                     ("m", r"\mathcal{B}"), ("t", " 就弄不歪 "),
                     ("m", r"\mathcal{A}"), ("t", " 的特征方向")], 0.3)
        self.wait(1.6)
        self.wipe()

        # ---- 可视化：双色罩子 ----
        self.head(mixlabel(("t", "看图："), ("m", r"\mathcal{B}", ORANGE),
                          ("t", " 摸不歪 "), ("m", r"\mathcal{A}", BLUE),
                          ("t", " 的特征方向"), color=PURPLE, ts=48, ms=50), color=PURPLE)
        base = np.array([-2.6, 0.2, 0])
        hood_m = hood(rx=3.1, ry=2.0, color=BLUE)
        hood_m.remove(hood_m[1])   # 去掉自带 W 标签，避免与 V_λ 重复
        hood_m.move_to(base)
        self.play(GrowFromCenter(hood_m), run_time=0.55)
        self.reg(hood_m)
        d_dir = np.array([np.cos(0.48), np.sin(0.48), 0])
        ln = Line(base - 2.2 * d_dir, base + 2.2 * d_dir).set_stroke(BLUE, 2.6)
        arr = Arrow(base, base + 1.45 * d_dir, buff=0, stroke_width=5.5,
                    color=RED, max_tip_length_to_length_ratio=0.26)
        lab = mt(r"d", size=44, color=RED).next_to(arr.get_end(), UP, buff=0.14)
        lam = mt(r"V_\lambda", size=40, color=BLUE).move_to(base + [-1.55, 1.05, 0])
        self.play(FadeIn(ln), GrowArrow(arr), Write(lab), Write(lam), run_time=1.0)
        self.reg(ln, arr, lab, lam)
        self.sub_in([("m", r"d"), ("t", " 是 "), ("m", r"\mathcal{A}"),
                     ("t", " 的特征向量，躺在特征子空间 "), ("m", r"V_\lambda"),
                     ("t", " 里")], 0.28)
        self.wait(1.0)

        # B 作用：整条线只是伸缩，仍在这条直线上
        orange_ring = Ellipse(width=7.0, height=4.7)
        orange_ring.set_stroke(ORANGE, 3.0).set_fill(ORANGE, 0.05)
        orange_ring.move_to(base)
        bl = mt(r"\mathcal{B}", size=40, color=ORANGE).move_to(base + [2.5, 1.75, 0])
        self.play(FadeIn(orange_ring), Write(bl), run_time=0.8)
        self.reg(orange_ring, bl)
        arr2 = Arrow(base, base + 2.15 * d_dir, buff=0, stroke_width=5.5,
                     color=RED, max_tip_length_to_length_ratio=0.24)
        lab2 = mt(r"\mathcal{B}d", size=40, color=RED).next_to(arr2.get_end(), UP, buff=0.14)
        self.play(Transform(arr, arr2), Transform(lab, lab2), run_time=1.1)
        self.reg(arr2, lab2)
        ring = glow_ring(rx=3.1, ry=2.0, color=GOLD, times=3).move_to(base)
        self.play(FadeIn(ring), run_time=0.22)
        self.play(ring.animate.scale(1.22).set_opacity(0), run_time=0.65)
        st = stamp("✔ 还在里面", color=GREEN, size=34).move_to([3.9, -1.5, 0])
        self.play(GrowFromCenter(st), run_time=0.45)
        self.reg(st)
        self.sub_in([("m", r"\mathcal{B}"),
                     ("t", " 只能沿特征方向伸缩 —— 出不去，这就是交换性的威力")], 0.3)
        self.wait(1.7)
        self.wipe()

    # ============================================================
    # 第2章  例 6.6.2（公共特征向量，双解法）
    # ============================================================
    def ch2_example662(self):
        # ---- ② 抄题 ----
        bar = self.head("例 6.6.2", color=GOLD)
        rows = [
            mixed(("m", r"V", INK), ("t", " 是复数域上 ", INK), ("m", r"n", INK),
                  ("t", " 维线性空间，", INK), ("m", r"A,B", INK),
                  ("t", " 为 ", INK), ("m", r"V", INK),
                  ("t", " 上线性变换，", INK), ts=34, ms=44),
            mixed(("t", "有 ", INK), ("m", r"AB=BA", RED), ("t", "．", INK),
                  ts=34, ms=48),
            mixed(("t", "证明：", INK), ("m", r"A,B", GOLD),
                  ("t", " 有", INK), ("t", "公共特征向量", GOLD), ("t", "．", INK),
                  ts=34, ms=46),
        ]
        card = problem_card("例 6.6.2（题面）", rows, color=GOLD)
        card.move_to([0, 0.55, 0])
        self.show_rows([card], rt=1.5)
        self.wait(0.7)
        self.sub_in("复数域 + 交换 —— 条件就这两个，怎么挖出公共特征向量？", 0.3)
        self.wait(1.5)
        self.wipe()

        # ---- ② 思路导图（题目看清楚了再列打法）----
        self.mini_map_page(
            map_data_ex662(), "例 6.6.2 · 思路导图",
            "题目到手，打法四步走：用交换性 → 缩进去 → 找特征值 → 到手", color=GOLD)

        # ---- ③ 解法一（变换语言）----
        self.head("解法一 · 变换语言", color=BLUE)
        rows1 = [
            mixed(("t", "① ", INK), ("m", r"AB=BA", RED),
                  ("t", " ⇒ ", INK), ("m", r"A", INK),
                  ("t", " 的特征子空间都是 ", INK), ("m", r"B", INK),
                  ("t", " 的不变子空间", INK),
                  ("t", "（命题 6.6.2）", GRAY), ts=32, ms=42),
            mixed(("t", "② 取 ", INK), ("m", r"A", INK),
                  ("t", " 的特征子空间 ", INK), ("m", r"V_\lambda", RED),
                  ts=34, ms=46),
            mixed(("t", "③ ", INK), ("m", r"V_\lambda", RED),
                  ("t", " 在 ", INK), ("m", r"B", INK),
                  ("t", " 下不变 ⇒ 可把 ", INK), ("m", r"B", INK),
                  ("t", " 限制上去：", INK),
                  ("m", r"B|_{V_\lambda}", GOLD), ts=32, ms=46),
        ]
        flow1 = VGroup(*rows1).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        flow1.move_to([0, 0.55, 0])
        for r in rows1:
            self.play(Write(r), run_time=0.8)
            self.reg(r)
        self.sub_in([("t", "老命题直接把战场圈进 "), ("m", r"V_\lambda"),
                     ("t", " —— 在里面 "), ("m", r"\mathcal{B}"),
                     ("t", " 随便折腾都出不去")], 0.3)
        self.wait(1.5)
        self.wipe()

        self.head("解法一 · 收网", color=GREEN)
        rows2 = [
            mixed(("t", "④ 复数域 ⇒ ", INK), ("m", r"B|_{V_\lambda}", GOLD),
                  ("t", " 必有特征值 ", INK), ("m", r"\lambda_0", RED), ts=32, ms=46),
            mixed(("m", r"B|V_\lambda(d_0)=\lambda_0 d_0", INK), ts=34, ms=48),
            mixed(("t", "⑤ ", INK), ("m", r"d_0", GOLD),
                  ("t", " 在 ", INK), ("m", r"V_\lambda", RED),
                  ("t", " 里 ⇒ 是 ", INK), ("m", r"A", INK),
                  ("t", " 的特征向量", INK), ts=32, ms=44),
            mixed(("t", "⑥ 又是 ", INK), ("m", r"B|_{V_\lambda}", GOLD),
                  ("t", " 的特征向量 ⇒ 也是 ", INK), ("m", r"B", INK),
                  ("t", " 的特征向量", INK), ts=32, ms=44),
        ]
        flow2 = VGroup(*rows2).arrange(DOWN, buff=0.46, aligned_edge=LEFT)
        flow2.move_to([0, 0.35, 0])
        for r in rows2:
            self.play(Write(r), run_time=0.75)
            self.reg(r)
        nb = note_box(kai("「必有特征值」的依据：复数域上特征多项式必有复根（代数基本定理）",
                          size=26).move_to([0, -2.15, 0]))
        self.play(Write(nb), run_time=0.9)
        self.reg(nb)
        self.sub_in([("t", "缩进去找一个特征值，它同时是 "), ("m", r"\mathcal{A}"),
                     ("t", " 和 "), ("m", r"\mathcal{B}"),
                     ("t", " 的 —— 公共特征向量到手")], 0.3)
        self.wait(1.6)
        self.wipe()

        # ---- 可视化：降维打击 ----
        self.head("看图：降维打击", color=PURPLE)
        big = vector_cloud(n=16, rmax=2.9, seed=21, w=2.4)
        big.move_to([0, 0.25, 0])
        vlab = mt(r"V", size=52, color=GRAY).move_to([6.1, 2.6, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in big], lag_ratio=0.05),
                  Write(vlab), run_time=1.2)
        self.reg(big, vlab)
        self.sub_in([("t", "整个大空间 "), ("m", r"V"),
                     ("t", " 里乱找，方向太多了")], 0.28)
        self.wait(1.0)

        base = np.array([0, 0.25, 0])
        hood_m = hood(rx=1.95, ry=1.25, color=BLUE)
        hood_m.remove(hood_m[1])   # 去掉自带 W 标签
        hood_m.move_to(base)
        lam = mt(r"V_\lambda", size=40, color=BLUE).move_to(base + [-0.95, 0.55, 0])
        self.play(GrowFromCenter(hood_m), Write(lam), run_time=0.8)
        self.reg(hood_m, lam)
        # 罩外压暗
        self.play(big.animate.set_opacity(0.12), vlab.animate.set_opacity(0.25),
                  run_time=0.8)
        self.sub_in([("t", "缩进 "), ("m", r"V_\lambda"),
                     ("t", " —— 罩外的世界不用看了")], 0.28)
        self.wait(0.9)
        # 罩内特征方向 + 金箭头诞生
        d_dir = np.array([np.cos(0.5), np.sin(0.5), 0])
        ln = Line(base - 1.5 * d_dir, base + 1.5 * d_dir).set_stroke(BLUE, 2.4)
        gold = Arrow(base, base + 1.15 * d_dir, buff=0, stroke_width=6.5,
                     color=GOLD, max_tip_length_to_length_ratio=0.26)
        self.play(FadeIn(ln), run_time=0.4)
        self.play(GrowArrow(gold), run_time=0.6)
        self.reg(ln, gold)
        ring1 = glow_ring(rx=1.95, ry=1.25, color=GOLD, times=2).move_to(base)
        self.play(FadeIn(ring1), run_time=0.2)
        self.play(ring1.animate.scale(1.3).set_opacity(0), run_time=0.55)
        st = stamp("✔ A、B 公共", color=GOLD, size=32).move_to([4.6, -1.9, 0])
        self.play(GrowFromCenter(st), run_time=0.45)
        self.reg(st)
        self.sub_in([("t", "罩内长出来的这支金箭头，同时姓 "), ("m", r"\mathcal{A}"),
                     ("t", " 也姓 "), ("m", r"\mathcal{B}")], 0.3)
        self.wait(1.6)
        self.wipe()

        # ---- ④ 解法二（矩阵语言）----
        self.head("解法二 · 矩阵语言（把它真造出来）", color=GREEN)
        rows1 = [
            mixed(("t", "① 取 ", INK), ("m", r"B", INK),
                  ("t", " 的特征值 ", INK), ("m", r"\lambda", RED),
                  ("t", " ⇒ 特征子空间 ", INK),
                  ("m", r"V_\lambda^{\,\mathcal{B}}", RED),
                  ("t", "（不变子空间思想）", GRAY), ts=32, ms=42),
            mixed(("t", "② ", INK), ("m", r"\forall d\in V_\lambda^{\,\mathcal{B}}", INK),
                  ("t", "，", INK),
                  ("m", r"(B-\lambda E)(Ad)=0\Rightarrow Ad\in V_\lambda^{\,\mathcal{B}}", INK),
                  ts=30, ms=42),
            mixed(("t", "③ 取 ", INK), ("m", r"V_\lambda^{\,\mathcal{B}}", RED),
                  ("t", " 的基 ", INK), ("m", r"\eta_1,\eta_2,\dots,\eta_s", GOLD),
                  ("t", "，", INK), ("m", r"s=\dim V_\lambda^{\,\mathcal{B}}", INK),
                  ts=30, ms=42),
        ]
        flow1 = VGroup(*rows1).arrange(DOWN, buff=0.56, aligned_edge=LEFT)
        flow1.move_to([0, 0.5, 0])
        for r in rows1:
            self.play(Write(r), run_time=0.8)
            self.reg(r)
        self.sub_in([("t", "这次换 "), ("m", r"\mathcal{B}"),
                     ("t", " 的特征子空间当战场 —— "), ("m", r"\mathcal{A}d"),
                     ("t", " 也跑不出去")], 0.3)
        self.wait(1.5)
        self.wipe()

        # 方程组页
        self.head(mixlabel(("t", "把 "), ("m", r"A"), ("t", " 在基上写开"),
                          color=GREEN, ts=48, ms=50), color=GREEN)
        s1 = mt(r"A\eta_1=k_{11}\eta_1+k_{21}\eta_2+\cdots+k_{s1}\eta_s", size=38)
        s2 = mt(r"A\eta_2=k_{12}\eta_1+k_{22}\eta_2+\cdots+k_{s2}\eta_s", size=38)
        sv = mt(r"\vdots", size=30)
        s3 = mt(r"A\eta_s=k_{1s}\eta_1+k_{2s}\eta_2+\cdots+k_{ss}\eta_s", size=38)
        sysg = VGroup(s1, s2, sv, s3).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        sysg.move_to([-1.3, 0.35, 0])
        for r in [s1, s2, sv, s3]:
            self.play(Write(r), run_time=0.7)
            self.reg(r)
        # 合成矩阵等式
        eq = mt(r"(A\eta_1,\cdots,A\eta_s)=(\eta_1,\cdots,\eta_s)\,k", size=42, color=INK)
        eq.move_to([0, -1.9, 0])
        self.play(Write(eq), run_time=1.2)
        self.reg(eq)
        rb = mixed(("m", r"k", RED),
                   ("t", " 相当于不变子空间对应的矩阵", RED), ts=26, ms=34)
        rb.move_to([0, -2.62, 0])
        self.play(Write(rb), run_time=0.8)
        self.reg(rb)
        self.sub_in([("m", r"k"), ("t", " 就是 "), ("m", r"\mathcal{A}"),
                     ("t", " 限制在 "), ("m", r"V_\lambda^{\,\mathcal{B}}"),
                     ("t", " 上的矩阵 —— 不变子空间用来缩小矩阵")], 0.3)
        self.wait(1.6)
        self.wipe()

        # 阶数梗小页
        self.head(mixlabel(("t", "一个小注：为什么讲不了 "), ("m", r"A\circ k"),
                          color=ORANGE, ts=48, ms=50), color=ORANGE)
        big_sq = Square(side_length=2.5).set_stroke(BLUE, 3.0).set_fill(CB, 0.12)
        big_sq.move_to([-3.4, 0.3, 0])
        bl1 = mt(r"n\times n", size=44, color=BLUE).move_to(big_sq)
        bl2 = mt(r"A", size=52, color=BLUE).next_to(big_sq, UP, buff=0.2)
        small_sq = Square(side_length=1.15).set_stroke(GREEN, 3.0).set_fill(CG, 0.12)
        small_sq.move_to([1.7, 0.3, 0])
        gl1 = mt(r"s\times s", size=34, color=GREEN).move_to(small_sq)
        gl2 = mt(r"k", size=48, color=GREEN).next_to(small_sq, UP, buff=0.2)
        self.play(FadeIn(big_sq), Write(bl1), Write(bl2), run_time=1.0)
        self.play(FadeIn(small_sq), Write(gl1), Write(gl2), run_time=0.9)
        self.reg(big_sq, bl1, bl2, small_sq, gl1, gl2)
        cross = VGroup(Line([-0.32, -0.32, 0], [0.32, 0.32, 0]),
                       Line([-0.32, 0.32, 0], [0.32, -0.32, 0])) \
            .set_stroke(RED, 6).move_to([4.0, 0.3, 0])
        why = mixed(("t", "阶数不同，乘不到一起", RED), ts=34, ms=42)
        why.move_to([4.0, -0.75, 0])
        self.play(GrowFromCenter(cross), Write(why), run_time=0.9)
        self.reg(cross, why)
        sad = stick_man(0.62, mood="sad").move_to([4.0, 1.85, 0])
        self.play(FadeIn(sad, shift=UP * 0.25), run_time=0.4)
        self.reg(sad)
        self.sub_in([("m", r"A"), ("t", " 是 "), ("m", r"n"), ("t", " 阶、"),
                     ("m", r"k"), ("t", " 是 "), ("m", r"s"),
                     ("t", " 阶 —— 别硬乘，往下换招")], 0.3)
        self.wait(1.4)
        self.wipe()

        # 收网页
        self.head(mixlabel(("m", r"k", GOLD),
                          ("t", " 必有复特征值 ⇒ 构造公共特征向量", GOLD),
                          color=GOLD, ts=48, ms=50), color=GOLD)
        r1 = mixed(("t", "④ ", INK), ("m", r"k", GOLD),
                   ("t", " 是 ", INK), ("m", r"s\times s", GOLD),
                   ("t", " 方阵 ⇒ 至少有一个复特征值 ", INK),
                   ("m", r"\lambda_0", RED), ts=32, ms=44)
        r2 = mixed(("t", "⑤ 设 ", INK), ("m", r"k\,x_0=\lambda_0 x_0", INK),
                   ("t", "（", INK), ("m", r"x_0\neq 0", INK), ("t", "）", INK),
                   ts=32, ms=46)
        flow = VGroup(r1, r2).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        flow.move_to([0, 1.35, 0])
        for r in [r1, r2]:
            self.play(Write(r), run_time=0.75)
            self.reg(r)
        r3 = mt(r"A(\eta_1,\cdots,\eta_s)\,x_0=(\eta_1,\cdots,\eta_s)\,k\,x_0"
                r"=\lambda_0(\eta_1,\cdots,\eta_s)\,x_0", size=38)
        r3.move_to([0, -0.15, 0])
        r4 = mixed(("t", "记 ", INK), ("m", r"\eta_0=(\eta_1,\cdots,\eta_s)\,x_0"
                                        r"=x_1\eta_1+\cdots+x_s\eta_s", GOLD),
                   ts=32, ms=44)
        r4.move_to([0, -1.15, 0])
        for r in [r3, r4]:
            self.play(Write(r), run_time=0.8)
            self.reg(r)
        self.sub_in([("t", "把 "), ("m", r"\eta_0"),
                     ("t", " 拆开看：它是基的线性组合，系数就是特征向量 "),
                     ("m", r"x_0")], 0.3)
        self.wait(1.5)
        self.wipe()

        self.head("双重身份验明正身", color=GOLD)
        q1 = mixed(("t", "⑥ ", INK), ("m", r"A\,\eta_0=\lambda_0\,\eta_0", GREEN),
                   ("t", " ⇒ ", INK), ("m", r"\eta_0", GOLD),
                   ("t", " 是 ", INK), ("m", r"A", INK),
                   ("t", " 的特征向量", INK), ts=32, ms=46)
        q2 = mixed(("t", "⑦ ", INK), ("m", r"\eta_0\in V_\lambda^{\,\mathcal{B}}", RED),
                   ("t", " ⇒ ", INK), ("m", r"B\,\eta_0=\lambda\,\eta_0", GREEN),
                   ("t", "，也是 ", INK), ("m", r"B", INK),
                   ("t", " 的特征向量", INK), ts=32, ms=44)
        q3 = mixed(("t", "（", INK), ("m", r"\eta_0\neq 0", INK),
                   ("t", "：", INK), ("m", r"x_0\neq 0", INK),
                   ("t", " 且基线性无关）", INK), ts=26, ms=36)
        flow = VGroup(q1, q2, q3).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        flow.move_to([0, 0.75, 0])
        for r in [q1, q2, q3]:
            self.play(Write(r), run_time=0.75)
            self.reg(r)
        final = mixed(("t", "⇒ ", GOLD), ("m", r"A,B", GOLD),
                      ("t", " 的公共特征向量 ", GOLD),
                      ("m", r"\eta_0", GOLD), ("t", " 构造完毕！", GOLD),
                      ts=36, ms=50)
        final.move_to([0, -1.35, 0])
        hb = hilite(final, color=GOLD)
        self.play(Write(hb), run_time=1.0)
        self.reg(hb)
        st = stamp("✔ 公共特征向量", color=GOLD, size=34).move_to([4.4, -2.2, 0])
        self.play(GrowFromCenter(st), run_time=0.45)
        self.reg(st)
        self.sub_in("解法一是「找到它」，解法二是「把它造出来」", 0.3)
        self.wait(1.7)
        self.wipe()

    # ============================================================
    # 第3章  例 6.6.4（苏州大学真题）
    # ============================================================
    def ch3_example664(self):
        # ---- ② 抄题 ----
        bar = self.head("例 6.6.4（苏州大学）", color=RED)
        rows = [
            mixed(("m", r"A,B", INK), ("t", " 为 ", INK), ("m", r"n", INK),
                  ("t", " 阶复方阵，", INK), ts=36, ms=48),
            mixed(("m", r"AB-BA=A", RED), ("t", "．", INK), ts=36, ms=52),
            mixed(("t", "证明：", INK), ("m", r"A,B", GOLD),
                  ("t", " 有", INK), ("t", "公共特征向量", GOLD), ("t", "．", INK),
                  ts=36, ms=48),
        ]
        card = problem_card("例 6.6.4（题面）", rows, color=RED)
        card.move_to([0, 0.55, 0])
        self.show_rows([card], rt=1.5)
        tag = stamp("考研真题", color=RED, size=30, angle=-0.14) \
            .move_to(card.get_corner(UR) + [-1.1, 0.35, 0])
        self.play(GrowFromCenter(tag), run_time=0.45)
        self.reg(tag)
        self.wait(0.6)
        self.sub_in([("t", "注意：条件是 "), ("m", r"AB-BA=A"),
                     ("t", "，不是上题的 "), ("m", r"AB=BA")], 0.3)
        self.wait(1.6)
        self.wipe()

        # ---- ② 思路导图（题目看清楚了再列打法）----
        self.mini_map_page(
            map_data_ex664(), "例 6.6.4 · 思路导图",
            "题目看完了 —— 它漂亮就漂亮在：先带你撞一次墙，再教你翻墙", color=RED)

        # ---- ③ 死胡同 ----
        self.head(mixlabel(("t", "先走老路：证 "), ("m", r"V_\lambda"),
                          ("t", " 是 "), ("m", r"\mathcal{B}", BLUE),
                          ("t", " 不变？"), color=BLUE, ts=48, ms=50), color=BLUE)
        rows1 = [
            mixed(("t", "① ", INK), ("m", r"\forall d\in V_\lambda", INK),
                  ("t", "，", INK), ("m", r"(A-\lambda E)d=0", INK),
                  ("t", "，想证 ", INK), ("m", r"Bd\in V_\lambda", GOLD),
                  ts=32, ms=44),
            mixed(("m", r"(A-\lambda E)Bd=ABd-\lambda Bd", INK), ts=34, ms=46),
            mixed(("m", r"=(BA+A)d-\lambda Bd", INK),
                  ("t", "　← 用 ", INK), ("m", r"AB=BA+A", RED), ts=32, ms=42),
        ]
        flow1 = VGroup(*rows1).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        flow1.move_to([0, 0.6, 0])
        for r in rows1:
            self.play(Write(r), run_time=0.8)
            self.reg(r)
        self.wait(0.6)
        self.sub_in("套路跟上题一样 —— 看着很有希望", 0.28)
        self.wait(1.2)
        self.wipe()

        self.head("…… 卡住了", color=RED)
        rows2 = [
            mixed(("m", r"=BAd+Ad-\lambda Bd", INK), ts=34, ms=46),
            mixed(("m", r"=\lambda Bd+Ad-\lambda Bd=Ad", INK),
                  ("t", "　（", INK), ("m", r"BAd=\mathcal{B}(\mathcal{A}d)=\lambda Bd", GRAY),
                  ("t", "）", INK), ts=32, ms=42),
        ]
        flow2 = VGroup(*rows2).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        flow2.move_to([-1.2, 1.25, 0])
        for r in rows2:
            self.play(Write(r), run_time=0.8)
            self.reg(r)
        # 红批 + 大红叉
        red = mixed(("m", r"Ad", RED), ("t", " 一定为 0 吗？", INK),
                    ("t", "仅当 ", RED), ("m", r"\lambda=0", RED),
                    ("t", " 时才行！", RED), ts=34, ms=46)
        red.move_to([0, -0.1, 0])
        cross = VGroup(Line([-0.34, -0.34, 0], [0.34, 0.34, 0]),
                       Line([-0.34, 0.34, 0], [0.34, -0.34, 0])) \
            .set_stroke(RED, 7).move_to([-4.6, -0.1, 0])
        self.play(Write(red), GrowFromCenter(cross), run_time=0.9)
        self.reg(red, cross)

        # 火柴人撞墙彩蛋
        wall = Rectangle(width=0.35, height=1.9)
        wall.set_stroke(INK, 2.6).set_fill("#DDD3C4", 1)
        wall.move_to([4.55, 0.75, 0])
        wl = mt(r"Ad=0\ ?", size=30, color=INK)
        wl.next_to(wall, UP, buff=0.16)
        man = stick_man(0.7).move_to([3.4, 0.15, 0])
        self.play(FadeIn(wall), Write(wl), FadeIn(man), run_time=0.8)
        self.play(man.animate.move_to([4.15, 0.15, 0]), run_time=0.45)
        self.play(man.animate.move_to([3.92, 0.15, 0]).rotate(-0.5), run_time=0.4)
        self.reg(wall, wl, man)
        self.sub_in([("t", "卡死了："), ("m", r"Ad"), ("t", " 凭什么等于 "),
                     ("m", r"0"), ("t", "？除非 "), ("m", r"\lambda=0")], 0.3)
        self.wait(1.3)

        # 转折
        turn = mixed(("t", "那就先证明：", INK), ("m", r"A", RED),
                     ("t", " 的特征值全为 ", INK), ("m", r"0", RED),
                     ts=40, ms=48)
        turn.move_to([0, -1.5, 0])
        self.play(Write(turn), run_time=1.0)
        self.reg(turn)
        self.sub_in([("t", "换个思路：先逼出 "), ("m", r"\lambda=0"),
                     ("t", "，再回来走老路")], 0.3)
        self.wait(1.5)
        self.wipe()

        # ---- ④ 迹技巧 ----
        self.head("杀手锏：迹", color=GOLD)
        t1 = mixed(("m", r"\operatorname{tr}(A)=\operatorname{tr}(AB)-\operatorname{tr}(BA)=0", INK),
                   ts=32, ms=44)
        t2 = mixed(("m", r"A^2=A(AB-BA)=A^2B-ABA", INK), ts=32, ms=44)
        t3 = mixed(("m", r"\operatorname{tr}(A^2)=\operatorname{tr}(A^2B)-\operatorname{tr}(ABA)=0", INK),
                   ts=32, ms=44)
        flow = VGroup(t1, t2, t3).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        flow.move_to([0, 0.95, 0])
        for r in [t1, t2, t3]:
            self.play(Write(r), run_time=0.8)
            self.reg(r)
        self.sub_in([("m", r"AB-BA=A"), ("t", " 两边取迹："),
                     ("m", r"\operatorname{tr}(AB)=\operatorname{tr}(BA)"),
                     ("t", "，一减就是 "), ("m", r"0")], 0.3)
        self.wait(1.4)
        self.wipe()

        self.head("推广到任意次幂", color=GOLD)
        u1 = mixed(("m", r"A^n=A^{n-1}(AB-BA)=A^nB-A^{n-1}BA", INK), ts=32, ms=44)
        u2 = mixed(("m", r"\operatorname{tr}(A^{n-1}BA)=\operatorname{tr}(A^nB)", RED),
                   ("t", "　（迹的循环性）", GRAY), ts=32, ms=42)
        u3 = mixed(("t", "⇒ ", INK),
                   ("m", r"\operatorname{tr}(A^k)=0,\quad k=1,2,\dots,n", GOLD),
                   ts=32, ms=46)
        flow = VGroup(u1, u2, u3).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        flow.move_to([-0.6, 0.85, 0])
        for r in [u1, u2, u3]:
            self.play(Write(r), run_time=0.8)
            self.reg(r)
        nb = note_box(kaimix(("t", "迹的循环性："),
                             ("m", r"\operatorname{tr}(XYZ)=\operatorname{tr}(ZXY)"
                                   r"=\operatorname{tr}(YZX)"),
                             ("t", " —— 矩阵转圈圈，迹不变"), ts=26, ms=32)
                      .move_to([0.6, -1.7, 0]))
        self.play(Write(nb), run_time=0.9)
        self.reg(nb)
        self.sub_in([("m", r"A"), ("t", " 的所有次幂，迹全被逼成 "),
                     ("m", r"0")], 0.3)
        self.wait(1.4)
        self.wipe()

        # 迹转圈可视化
        self.head("看图：迹的循环性 —— 矩阵转圈圈", color=PURPLE)
        cyc = mt(r"\operatorname{tr}(XYZ)=\operatorname{tr}(ZXY)=\operatorname{tr}(YZX)",
                 size=46, color=INK)
        cyc.move_to([0, 2.1, 0])
        self.play(Write(cyc), run_time=1.1)
        self.reg(cyc)
        R = 1.78
        center = np.array([0.3, -0.4, 0])
        angles = [np.pi / 2, np.pi / 2 + 2 * np.pi / 3, np.pi / 2 + 4 * np.pi / 3]
        labels = ["X", "Y", "Z"]
        blocks = VGroup()
        for a, s in zip(angles, labels):
            sq = RoundedRectangle(corner_radius=0.14, width=1.0, height=1.0)
            sq.set_stroke(PURPLE, 3.0).set_fill("#F0E9F8", 1)
            sq.move_to(center + R * np.array([np.cos(a), np.sin(a), 0]))
            tx = mt(s, size=44, color=PURPLE).move_to(sq)
            blocks.add(VGroup(sq, tx))
        self.play(LaggedStart(*[GrowFromCenter(b) for b in blocks], lag_ratio=0.15),
                  run_time=0.8)
        self.reg(blocks)
        self.wait(0.5)
        # 转一格
        blocks2 = VGroup()
        for i, (a, s) in enumerate(zip(angles, ["Z", "X", "Y"])):
            sq = RoundedRectangle(corner_radius=0.14, width=1.0, height=1.0)
            sq.set_stroke(PURPLE, 3.0).set_fill("#F0E9F8", 1)
            sq.move_to(center + R * np.array([np.cos(a), np.sin(a), 0]))
            tx = mt(s, size=44, color=PURPLE).move_to(sq)
            blocks2.add(VGroup(sq, tx))
        self.play(Transform(blocks, blocks2), run_time=1.1)
        flash = Circle(radius=2.4).set_stroke(GOLD, 5, opacity=0.55).set_fill(opacity=0)
        flash.move_to(center)
        self.play(FadeIn(flash), run_time=0.2)
        self.play(flash.animate.scale(1.25).set_opacity(0), run_time=0.6)
        self.sub_in("转一圈，乘积顺序变了，迹纹丝不动", 0.3)
        self.wait(1.4)
        self.wipe()

        # ---- ⑤ 引理 + 范德蒙回归 ----
        self.head(mixlabel(("t", "引理：迹全为零 "), ("m", r"\Rightarrow"),
                          ("t", " 特征值全为零"), color=GOLD, ts=48, ms=50), color=GOLD)
        rows = [
            mixed(("t", "若 ", INK),
                  ("m", r"\operatorname{tr}(A^k)=0\ (k=1,2,\dots,n)", INK),
                  ("t", "，则 ", INK), ("m", r"A", RED),
                  ("t", " 的特征值全为 ", INK), ("m", r"0", RED), ts=32, ms=44),
            mixed(("t", "设 ", INK), ("m", r"A", INK),
                  ("t", " 的非零特征值共 ", INK), ("m", r"s", INK),
                  ("t", " 种：", INK), ("m", r"\lambda_1,\dots,\lambda_s", RED),
                  ("t", "（互异），重数 ", INK), ("m", r"m_1,\dots,m_s", INK),
                  ts=30, ms=42),
            mixed(("m", r"\operatorname{tr}(A^k)=\sum_{i=1}^{s}m_i\lambda_i^k=0,"
                        r"\quad k=1,\dots,s", INK), ts=32, ms=44),
        ]
        flow = VGroup(*rows).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        flow.move_to([0, 0.6, 0])
        for r in rows:
            self.play(Write(r), run_time=0.8)
            self.reg(r)
        nb = note_box(kaimix(("t", "全部特征值（含重数）= "),
                             ("m", r"\lambda_1,\dots,\lambda_s"), ("t", " 各 "),
                             ("m", r"m_i"), ("t", " 重加上若干个 "), ("m", r"0"),
                             ("t", "，所以迹 "),
                             ("m", r"=\sum_i m_i\lambda_i^k"), ts=25, ms=30)
                      .move_to([0, -1.85, 0]))
        self.play(Write(nb), run_time=0.9)
        self.reg(nb)
        self.sub_in([("m", r"s"), ("t", " 个未知数 "),
                     ("m", r"m_1,\dots,m_s"), ("t", "，"), ("m", r"s"),
                     ("t", " 条方程 —— 该矩阵上场了")], 0.3)
        self.wait(1.4)
        self.wipe()

        # 范德蒙第二次登场
        self.head("写成矩阵 —— 老朋友回来了", color=GOLD)
        lam = [r"\lambda_1", r"\lambda_2", r"\lambda_3", r"\lambda_s"]
        V = vander_matrix(lam, cell_w=0.72, gap=0.05, n_rows=4)
        L = vec_col([r"m_1\lambda_1", r"m_2\lambda_2", r"\cdots", r"m_s\lambda_s"],
                    cell_w=1.15, gap=0.05, color=CG, fill=CFG, font_size=28)
        R = vec_col([r"0", r"0", r"0", r"0"], cell_w=0.62, gap=0.05,
                    color=CR, fill=CFR, font_size=30)
        eq1 = mt(r"\cdot", size=44, color=INK)
        eq2 = mt(r"=", size=44, color=INK)
        eqg = VGroup(V, eq1, L, eq2, R).arrange(RIGHT, buff=0.22)
        eqg.move_to([-1.6, -0.1, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.85) for c in V[0]], lag_ratio=0.05),
                  run_time=0.85)
        self.play(FadeIn(V[1]), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in L[0]], lag_ratio=0.08),
                  FadeIn(eq1), run_time=0.6)
        self.play(FadeIn(L[1]), run_time=0.25)
        self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in R[0]], lag_ratio=0.08),
                  FadeIn(eq2), run_time=0.5)
        self.play(FadeIn(R[1]), run_time=0.25)
        self.reg(eqg)
        hello = kai("上集那块范德蒙矩阵，又见面了", size=28)
        hello.move_to([-4.9, -2.5, 0])
        self.play(Write(hello), run_time=0.8)
        self.reg(hello)
        det = mixed(("m", r"\lambda_i", GOLD), ("t", " 互异 ", GOLD),
                    ("m", r"\Rightarrow", GOLD), ("t", " 可逆", GOLD), ts=30, ms=38)
        det.move_to([5.2, 1.3, 0])
        self.play(Write(det), run_time=0.8)
        self.reg(det)
        st = stamp("可逆", color=PURPLE, size=44).move_to([5.2, -0.5, 0])
        self.play(GrowFromCenter(st), run_time=0.5)
        self.reg(st)
        self.sub_in([("t", "第 "), ("m", r"k"),
                     ("t", " 行乘上未知数，正好就是 "),
                     ("m", r"\operatorname{tr}(A^k)=0")], 0.3)
        self.wait(1.5)
        self.wipe()

        # 引理结论
        self.head("齐次方程只有零解", color=GREEN)
        c1 = mixed(("m", r"\Rightarrow m_1\lambda_1=m_2\lambda_2=\cdots=m_s\lambda_s=0", INK),
                   ts=32, ms=44)
        c2 = mixed(("t", "又 ", INK), ("m", r"\lambda_i\neq 0", RED),
                   ("t", " ⇒ ", INK), ("m", r"m_1=m_2=\cdots=m_s=0", GOLD), ts=32, ms=46)
        c3 = mixed(("t", "⇒ 非零特征值重数全为 0 ⇒ ", INK),
                   ("m", r"A", RED), ("t", " 只有 ", RED), ("m", r"0", RED),
                   ("t", " 特征值", RED), ts=34, ms=46)
        flow = VGroup(c1, c2, c3).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        flow.move_to([0, 0.55, 0])
        for r in [c1, c2, c3]:
            self.play(Write(r), run_time=0.8)
            self.reg(r)
        hb = hilite_box(c3, color=GOLD)
        self.play(Write(hb), run_time=0.9)
        self.reg(hb)
        self.sub_in([("t", "翻墙成功："), ("m", r"A"),
                     ("t", " 的特征值全被逼成 "), ("m", r"0")], 0.3)
        self.wait(1.5)
        self.wipe()

        # ---- ⑥ 回到 V₀ 收尾 ----
        self.head(mixlabel(("t", "回到 "), ("m", r"V_0"),
                          ("t", "，老路通了"), color=GREEN, ts=48, ms=50), color=GREEN)
        rows1 = [
            mixed(("t", "① 此时 ", INK), ("m", r"A", INK),
                  ("t", " 的特征子空间只有 ", INK),
                  ("m", r"V_0=\ker A", RED), ts=32, ms=46),
            mixed(("t", "（", INK), ("m", r"\det A=0", INK),
                  ("t", " ⇒ ", INK), ("m", r"V_0\neq\{0\}", INK),
                  ("t", "，有东西可找）", GRAY), ts=28, ms=38),
            mixed(("t", "② ", INK), ("m", r"\forall d\in V_0:\ A(Bd)=(AB)d", INK),
                  ts=32, ms=44),
            mixed(("m", r"=(BA+A)d=B(Ad)+Ad=B\cdot 0+0=0", GREEN),
                  ("t", " ⇒ ", INK), ("m", r"Bd\in V_0", GOLD), ts=30, ms=44),
        ]
        flow1 = VGroup(*rows1).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        flow1.move_to([0, 0.45, 0])
        for r in rows1:
            self.play(Write(r), run_time=0.75)
            self.reg(r)
        nb = note_box(kai("这一行笔记里跳掉了，补上 —— 不补就算跳步", size=25)
                      .move_to([0, -1.95, 0]))
        self.play(Write(nb), run_time=0.9)
        self.reg(nb)
        self.sub_in([("m", r"\lambda=0"), ("t", " 时 "), ("m", r"Ad=0"),
                     ("t", " 恒成立 —— 死胡同瞬间变通途")], 0.3)
        self.wait(1.6)
        self.wipe()

        self.head("最后一击", color=GOLD)
        rows2 = [
            mixed(("t", "③ ", INK), ("m", r"V_0", RED), ("t", " 是 ", INK),
                  ("m", r"B", INK), ("t", " 不变 ⇒ 限制 ", INK),
                  ("m", r"B|_{V_0}", GOLD), ts=32, ms=46),
            mixed(("t", "④ 复数域 ⇒ ", INK), ("m", r"B|_{V_0}", GOLD),
                  ("t", " 有特征值 ", INK), ("m", r"\mu_0", RED),
                  ("t", "，特征向量 ", INK), ("m", r"\eta_0", GOLD), ts=32, ms=44),
            mixed(("t", "⑤ ", INK), ("m", r"\eta_0\in V_0", RED),
                  ("t", " ⇒ 是 ", INK), ("m", r"A", INK),
                  ("t", " 的特征向量；又是 ", INK), ("m", r"B", INK),
                  ("t", " 的特征向量", INK), ts=32, ms=44),
            mixed(("t", "⇒ ", INK), ("m", r"A,B", GOLD),
                  ("t", " 有公共特征向量", GOLD),
                  ("t", "　∎", INK), ts=36, ms=50),
        ]
        flow2 = VGroup(*rows2).arrange(DOWN, buff=0.44, aligned_edge=LEFT)
        flow2.move_to([0, 0.4, 0])
        for r in rows2:
            self.play(Write(r), run_time=0.75)
            self.reg(r)
        st = stamp("✔ 公共特征向量", color=GOLD, size=32).move_to([4.3, -2.0, 0])
        self.play(GrowFromCenter(st), run_time=0.45)
        self.reg(st)
        self.sub_in("和上题同一个终点：限制到不变子空间上，再找一个特征值", 0.3)
        self.wait(1.7)
        self.wipe()

        # 收尾可视化：V₀ 小罩 + η₀ 诞生
        self.head(mixlabel(("t", "看图："), ("m", r"\eta_0"),
                          ("t", " 的诞生"), color=PURPLE, ts=48, ms=50), color=PURPLE)
        base = np.array([-2.6, 0.15, 0])
        hood_m = hood(rx=2.9, ry=1.85, color=GREEN)
        hood_m.remove(hood_m[1])   # 去掉自带 W 标签
        hood_m.move_to(base)
        lab = mt(r"V_0", size=42, color=GREEN).move_to(base + [-1.5, 0.95, 0])
        self.play(GrowFromCenter(hood_m), Write(lab), run_time=0.8)
        self.reg(hood_m, lab)
        d_dir = np.array([np.cos(0.45), np.sin(0.45), 0])
        gold = Arrow(base, base + 1.35 * d_dir, buff=0, stroke_width=6.5,
                     color=GOLD, max_tip_length_to_length_ratio=0.26)
        gl = mt(r"\eta_0", size=42, color=GOLD).next_to(gold.get_end(), UP, buff=0.14)
        self.play(GrowArrow(gold), Write(gl), run_time=0.9)
        self.reg(gold, gl)
        oring = Ellipse(width=6.4, height=4.3)
        oring.set_stroke(ORANGE, 3.0).set_fill(ORANGE, 0.04)
        oring.move_to(base)
        ol = mt(r"\mathcal{B}", size=38, color=ORANGE).move_to(base + [2.3, 1.6, 0])
        self.play(FadeIn(oring), Write(ol), run_time=0.8)
        self.reg(oring, ol)
        ring = glow_ring(rx=2.9, ry=1.85, color=GOLD, times=3).move_to(base)
        self.play(FadeIn(ring), run_time=0.22)
        self.play(ring.animate.scale(1.25).set_opacity(0), run_time=0.6)
        st = stamp("✔ A、B 公共", color=GOLD, size=30).move_to([3.9, -1.4, 0])
        self.play(GrowFromCenter(st), run_time=0.45)
        self.reg(st)
        self.sub_in([("t", "绿色罩子（"), ("m", r"A"),
                     ("t", " 的核）里长出的金箭头，两个变换都拿它没办法")], 0.3)
        self.wait(1.7)
        self.wipe()

    # ============================================================
    # 结尾（无大地图：金句收尾）
    # ============================================================
    def s_end(self):
        t1 = mixed(("t", "不变子空间 = 线性变换的", INK),
                   ("t", "「舒适区」", GOLD), ts=46, ms=52)
        t1.move_to([0, 1.35, 0])
        t2 = mixed(("t", "找它，就是为了", INK),
                   ("t", "把大问题切成小问题", RED), ts=46, ms=52)
        t2.move_to([0, 0.15, 0])
        self.play(Write(t1), run_time=1.0)
        self.play(Write(t2), run_time=1.0)
        self.reg(t1, t2)
        self.sub_in("两道真题，一个思想：缩进去，再找特征值", 0.3)
        self.wait(1.8)

        man = stick_man(0.85, mood="happy").move_to([0, -1.75, 0])
        arm = man[2]  # 右手臂挥手
        self.play(FadeIn(man), run_time=0.4)
        self.reg(man)
        t3 = Text("下一期想看什么？评论区点题", font=SONG, font_size=38,
                  color=PURPLE, weight="BOLD")
        t3.move_to([0, -0.95, 0])
        self.play(Write(t3), run_time=0.9)
        self.reg(t3)
        self.play(Rotate(arm, angle=0.7, about_point=man.get_center() + [0, -0.3 * 0.85, 0]),
                  run_time=0.35)
        self.play(Rotate(arm, angle=-0.7, about_point=man.get_center() + [0, -0.3 * 0.85, 0]),
                  run_time=0.35)
        self.wait(1.6)
        self.wipe()
