# -*- coding: utf-8 -*-
"""
《不变子空间》上集 —— 从定义到范德蒙（抖音粉丝点题）
风格：Manim 宋体定理片 · 米白纸面 + 浅网格 + 彩色格子矩阵 + 白场转场
素材：博主考研手写笔记（一行不跳、先抄题再证明）

渲染：
  manim src/inv_part1.py Part1 -ql --media_dir ./media     # 低清预览
  manim src/inv_part1.py Part1 -pqh --media_dir ./media    # 1080p60
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inv_lib import *

RNG = np.random.default_rng(20260923)


class Part1(BaseScene):

    # ============================================================
    def construct(self):
        self.begin()
        self.s1_open()
        self.s2_map(first=True)
        self.ch1_definition()
        self.ch1_hood()
        self.ch1_counter()
        self.ch2_theorem661()
        self.ch3_prop661()
        self.ch4_radical()
        self.ch5_example661()
        self.s_end()

    # ---------- 地图常驻：累积点亮当前节点 ----------
    def map_light(self, key, hold=1.1, pulse=2):
        """
        镜头回到知识地图，把到 key 为止的节点全部点亮。
        ★ 配色一律用 paint_map 直接设，绝不对插件内部对象做 .animate
          （否则 surr_rect 会与文字错位，出现「空框 + 文字跑掉」的事故）。
        """
        mm, k2i, i2n = build_knowledge_map()
        paint_map(i2n, lit_ids=lit_ids_upto(key, k2i))
        self.hard_clear()
        # 回顾时也逐节点长出来，但节奏快（每节点 0.22s，全长约 2.6s）
        self.grow_map(i2n, node_rt=0.22)

        target = i2n[k2i[key]]
        for _ in range(pulse):
            ring = glow_ring(rx=target.surr_rect.width * 0.60,
                             ry=target.surr_rect.height * 0.88,
                             color=GOLD, times=2)
            ring.move_to(target.surr_rect.get_center())
            self.play(FadeIn(ring), run_time=0.16)
            self.play(ring.animate.scale(1.65).set_opacity(0), run_time=0.42)
        self.wait(hold)
        self.wipe(t_out=0.4)

    # ---------- S1 片头 ----------
    def s1_open(self):
        t1 = Text("抖音粉丝点题 · 高等代数", font=HEI, font_size=34,
                  color=RED, weight="BOLD")
        t1.move_to([0, 2.55, 0])
        t2 = song("不变子空间", size=104, color="#8B8BE8")
        t2.move_to([0, 0.75, 0])
        t2.set_stroke(WHITE, 2, background=True)
        self.play(FadeIn(t1, lag_ratio=0.10), run_time=0.5)
        self.play(FadeIn(t2, scale=1.12), run_time=0.55)

        # 火柴人走进罩子
        hood_m = hood(rx=1.85, ry=1.12, color=BLUE)
        hood_m.move_to([0, -1.85, 0])
        man = stick_man(0.72).move_to([-5.6, -1.95, 0])
        self.play(FadeIn(hood_m), run_time=0.4)
        self.play(man.animate.move_to([0, -2.05, 0]), run_time=0.9)
        ring = glow_ring(rx=1.85, ry=1.12, color=GOLD, times=3).move_to(hood_m.get_center())
        self.play(FadeIn(ring), run_time=0.2)
        self.play(ring.animate.scale(1.35).set_opacity(0), run_time=0.6)
        self.reg(t1, t2, hood_m, man)
        self.sub_in("住进去就出不来 —— 这就是不变子空间", 0.3)
        self.wait(0.8)
        self.wipe()
        return

    # ---------- S2 总览地图 ----------
    def s2_map(self, first=True):
        mm, k2i, i2n = build_knowledge_map()
        paint_map(i2n, lit_ids=[(0,)], todo_ids=[k2i[k] for k in MAP_LIT_ORDER])
        self.hard_clear()
        # ★ 全片最重要的一次「铺地图」：一个节点一个节点慢慢长出来
        #   12 个节点 × 0.70s ≈ 8.4 秒，观众能跟着一个一个看
        self.grow_map(i2n, node_rt=0.70)
        self.wait(0.6)
        self.sub_in("这是今天的路线图 —— 每讲一段，我就点亮一个节点", 0.3)
        self.wait(1.4)
        self.wipe()

    # ---------- 第1章 定义 ----------
    def ch1_definition(self, first=True):
        self.map_light("def")

        bar = self.head("6.6 不变子空间 · 定义", color=BLUE)
        rows = [
            mixed(("t", "设 ", INK), ("m", r"V", INK),
                  ("t", " 是数域 ", INK), ("m", r"P", INK),
                  ("t", " 上的线性空间，", INK), ("m", r"\mathcal{A}", INK),
                  ("t", " 是 ", INK), ("m", r"V", INK),
                  ("t", " 上的一个线性变换", INK), ts=34, ms=40),
            mixed(("t", "W", INK), ("t", " 是 ", INK), ("m", r"V", INK),
                  ("t", " 的子空间，如果对任意的 ", INK),
                  ("m", r"\alpha\in W", INK),
                  ("t", " 都有 ", INK), ("m", r"\mathcal{A}\alpha\in W", RED),
                  ts=34, ms=42),
            mixed(("t", "则称 ", INK), ("m", r"W", GOLD),
                  ("t", " 是 ", INK), ("m", r"\mathcal{A}", GOLD),
                  ("t", " 的不变子空间，简称为 ", INK),
                  ("m", r"\mathcal{A}", GOLD), ("t", "-子空间", GOLD), ts=34, ms=44),
        ]
        card = problem_card("定义（教材 6.6 原文）", rows, color=BLUE)
        card.move_to([0, 0.35, 0])
        self.show_rows([card], rt=1.0)
        self.wait(0.6)

        # 突出核心四个字
        core = card[2][1]  # 第二行（含 Aα ∈ W）整体
        self.play(Indicate(core, color=RED, scale_factor=1.06), run_time=1.0)
        self.wait(0.5)

        self.sub_in("核心就一句话：从 W 里出发，走一步 A，还在 W 里", 0.3)
        self.wait(1.6)
        self.wipe()

        # 笔记补充
        bar2 = self.head("笔记批注", color=PURPLE)
        rows2 = [
            mt(r"\forall\,\alpha\in W,\quad A(\alpha)\in W", size=50, color=INK),
            mixed(("t", "", INK), ("m", r"W", GOLD), ("t", " 称 ", INK),
                  ("m", r"A", GOLD), ("t", "-子空间", GOLD), ts=34, ms=48),
            mixed(("t", "此时可把 ", INK), ("m", r"A", BLUE),
                  ("t", " 限制到 ", INK), ("m", r"W", BLUE),
                  ("t", " 上，记为 ", INK), ("m", r"A|W", RED), ts=34, ms=48),
            mixed(("t", "", INK), ("m", r"A|W", RED),
                  ("t", " 为 ", INK), ("m", r"W\to W", RED),
                  ("t", " 线性变换", INK), ts=34, ms=48),
        ]
        flow = VGroup(*rows2).arrange(DOWN, buff=0.62).next_to(bar2, DOWN, buff=0.85)
        for r in rows2:
            self.play(FadeIn(r), run_time=0.7)
            self.reg(r)
        self.wait(0.7)
        self.sub_in("A 被限制在 W 上，成了 W 自己的变换，记作 A|W", 0.3)
        self.wait(1.6)
        self.wipe()

    # ---------- 第1章 · 罩子判定（主心骨镜头） ----------
    def ch1_hood(self):
        bar = self.head("什么叫「不变」？看这把箭头", color=BLUE)

        hood_m = hood(rx=3.35, ry=2.25, color=BLUE)
        hood_m.move_to([0, 0.45, 0])
        cloud = vector_cloud(n=12, rmax=1.05, seed=11)
        cloud.move_to([0, 0.45, 0])
        self.play(GrowFromCenter(hood_m), run_time=0.6)
        self.play(LaggedStart(*[GrowArrow(a) for a in cloud], lag_ratio=0.06), run_time=0.9)
        self.reg(hood_m, cloud)

        # 高亮一支 α
        alpha_idx = 0
        a0 = cloud[alpha_idx]
        alpha = Arrow(ORIGIN, a0.get_end() - a0.get_start(), buff=0,
                      stroke_width=6, color=RED,
                      max_tip_length_to_length_ratio=0.28).move_to(
            (a0.get_start() + a0.get_end()) / 2)
        self.play(GrowArrow(alpha), run_time=0.5)
        self.reg(alpha)
        self.sub_in("任取一个 α ∈ W", 0.28)
        self.wait(1.0)

        # 施加 A
        A_MAT = [[1.32, 0.26], [0.06, 1.12]]
        cloud2 = transform_cloud(cloud, A_MAT)
        cloud2.move_to(cloud2.get_center())
        shop = cloud2.get_center() - cloud.get_center()
        cloud2.shift(-shop)
        amat = grid_matrix(
            [[("1.32", CB, CFB), ("0.26", CB, CFB)],
             [("0.06", CB, CFB), ("1.12", CB, CFB)]], cell_w=0.66, font_size=30)
        amat.move_to([5.9, 1.55, 0])
        lbl = mixed(("m", r"A=", BLUE), ts=30, ms=40)
        lbl.next_to(amat, LEFT, buff=0.18)
        self.play(FadeIn(amat), FadeIn(lbl), run_time=0.5)
        self.reg(amat, lbl)

        self.play(Transform(cloud, cloud2), run_time=1.5)

        # 全部仍在罩内 → 金框 + 印章
        ring = glow_ring(rx=3.35, ry=2.25, color=GOLD, times=3).move_to(hood_m.get_center())
        self.play(FadeIn(ring), run_time=0.25)
        self.play(ring.animate.scale(1.22).set_opacity(0), run_time=0.7)
        st = stamp("✔ 不变", color=GREEN, size=40).move_to([0, -2.9, 0])
        self.play(GrowFromCenter(st), run_time=0.5)
        self.reg(st)
        self.sub_in("A(W) ⊆ W —— 变完还在里面，这才叫不变子空间", 0.3)
        self.wait(1.8)
        self.wipe()

    # ---------- 第1章 · 反例 ----------
    def ch1_counter(self):
        bar = self.head("换个 W，就飞出去了", color=RED)
        ang = np.pi / 3
        d = np.array([np.cos(ang), np.sin(ang), 0])
        ln = Line(-3.4 * d, 3.4 * d).set_stroke(BLUE, 3.2)
        lbl = mt(r"W=L(\alpha)", size=42, color=BLUE).move_to([-4.3, 2.05, 0])
        alpha = Arrow(ORIGIN, 1.85 * d, buff=0, stroke_width=6, color=RED,
                      max_tip_length_to_length_ratio=0.26)
        self.play(FadeIn(ln), FadeIn(lbl), GrowArrow(alpha), run_time=0.8)
        self.reg(ln, lbl, alpha)
        self.sub_in("W 是一条过原点的直线（一维子空间）", 0.28)
        self.wait(0.9)

        A_MAT = [[1.32, 0.26], [0.06, 1.12]]
        q = np.array(A_MAT) @ (1.85 * d[:2])
        moved = Arrow(ORIGIN, np.array([q[0], q[1], 0]), buff=0,
                      stroke_width=6, color=GREEN,
                      max_tip_length_to_length_ratio=0.26)
        self.play(Transform(alpha, moved), run_time=1.2)
        # 飞出直线的虚线提示
        ghost = DashedLine(alpha.get_end(), 1.85 * d, dash_length=0.12) \
            .set_stroke(RED, 3.0)
        self.play(Create(ghost), run_time=0.5)
        cross = VGroup(
            Line([-0.3, -0.3, 0], [0.3, 0.3, 0]),
            Line([-0.3, 0.3, 0], [0.3, -0.3, 0]),
        ).set_stroke(RED, 6).move_to([-4.3, 2.05, 0])
        self.play(ln.animate.set_stroke(RED, 3.2), GrowFromCenter(cross), run_time=0.5)
        self.reg(ghost, cross)

        sad = stick_man(0.6, mood="sad").move_to([3.9, -2.5, 0])
        self.play(FadeIn(sad, shift=UP * 0.3), run_time=0.4)
        self.reg(sad)
        self.sub_in("同样是 A，换个子空间就飞出去了 —— 关键在 W 选得对不对", 0.3)
        self.wait(1.8)
        self.wipe()

    # ============================================================
    # 第2章  定理 6.6.1
    # ============================================================
    def ch2_theorem661(self):
        self.map_light("trio")

        bar = self.head("定理 6.6.1", color=BLUE)
        rows = [
            mixed(("t", "", INK), ("m", r"V", INK),
                  ("t", " 上线性变换 ", INK), ("m", r"\mathcal{A}", INK),
                  ("t", " 的", INK), ("m", r"\ker", RED), ("t", "核与值域", RED),
                  ts=36, ms=46),
            mixed(("t", "", INK), ("m", r"\mathcal{A}", INK),
                  ("t", " 的", INK), ("m", r"V_\lambda", GREEN),
                  ("t", " 特征子空间", GREEN),
                  ("t", "都是 ", INK), ("m", r"\mathcal{A}", GOLD),
                  ("t", "-子空间．", GOLD), ts=36, ms=46),
        ]
        card = problem_card("定理 6.6.1（教材原文）", rows, color=BLUE)
        card.move_to([0, 0.6, 0])
        self.show_rows([card], rt=1.0)
        self.wait(0.6)
        self.sub_in("数学直接送我们三个天然的不变子空间，一个都不用自己造", 0.3)
        self.wait(1.6)
        self.wipe()

        # ---- 三兄弟逐个验证 ----
        trio = ["核 ker A", "值域 Im A", "特征子空间 V_λ"]
        cols = [RED, GREEN, PURPLE]
        # 核
        self._verify_one("①核", r"\ker A", cols[0],
                         lambda: self._demo_kernel())
        # 值域
        self._verify_one("②值域", r"\mathrm{Im}\,A", cols[1],
                         lambda: self._demo_image())
        # 特征子空间
        self._verify_one("③特征子空间", r"V_\lambda", cols[2],
                         lambda: self._demo_eigen())

    def _verify_one(self, label, sym, color, demo_fn):
        self.head(f"{label} 是不变子空间", color=color)
        demo_fn()
        st = stamp("✔", color=color, size=38).move_to([5.6, -2.55, 0])
        self.play(GrowFromCenter(st), run_time=0.4)
        self.reg(st)
        self.wait(0.9)
        self.wipe()

    def _demo_kernel(self):
        hood_m = hood(rx=2.6, ry=1.6, color=RED).move_to([-1.6, 0.5, 0])
        cloud = vector_cloud(n=8, rmax=0.85, seed=3, w=2.6).move_to([-1.6, 0.5, 0])
        self.play(GrowFromCenter(hood_m), LaggedStart(*[GrowArrow(a) for a in cloud],
                                                      lag_ratio=0.05), run_time=0.8)
        self.reg(hood_m, cloud)
        zero = Dot([-1.6, 0.5, 0], radius=0.11, color=INK)
        self.play(*[a.animate.scale(0.02).move_to([-1.6, 0.5, 0]) for a in cloud],
                  run_time=1.0)
        self.play(FadeIn(zero, scale=2.0), run_time=0.4)
        self.reg(zero)
        txt = mt(r"A(\ker A)=\{0\}\subseteq\ker A", size=46, color=RED)
        txt.move_to([3.5, 0.5, 0])
        self.play(FadeIn(txt), run_time=0.5)
        self.reg(txt)
        self.sub_in("核里的向量全被压成 0 向量 —— 0 当然还在罩子里", 0.28)

    def _demo_image(self):
        hood_m = hood(rx=2.7, ry=1.65, color=GREEN).move_to([-1.6, 0.5, 0])
        cloud = vector_cloud(n=8, rmax=0.8, seed=5, w=2.6).move_to([-1.6, 0.5, 0])
        self.play(GrowFromCenter(hood_m), LaggedStart(*[GrowArrow(a) for a in cloud],
                                                      lag_ratio=0.05), run_time=0.8)
        self.reg(hood_m, cloud)
        c2 = transform_cloud(cloud, [[1.28, 0.22], [0.05, 1.10]])
        c2.shift(np.array([-1.6, 0.5, 0]) - c2.get_center())
        self.play(Transform(cloud, c2), run_time=1.2)
        txt = mixed(("m", r"A(\mathrm{Im}\,A)\subseteq \mathrm{Im}\,A", GREEN), ts=34, ms=48)
        txt.move_to([3.7, 0.5, 0])
        self.play(FadeIn(txt), run_time=0.5)
        self.reg(txt)
        self.sub_in("值域是「输出的集合」，输出再被 A 作用，当然还是输出", 0.28)

    def _demo_eigen(self):
        hood_m = hood(rx=2.7, ry=1.65, color=PURPLE).move_to([-1.6, 0.5, 0])
        d = np.array([np.cos(0.5), np.sin(0.5), 0])
        ln = Line(-1.6 * d, 1.6 * d).set_stroke(PURPLE, 2.6)
        ln.shift([-1.6, 0.5, 0])
        arr = Arrow([-1.6, 0.5, 0], np.array([-1.6, 0.5, 0]) + 1.5 * d,
                    buff=0, stroke_width=5.5, color=PURPLE,
                    max_tip_length_to_length_ratio=0.26)
        self.play(GrowFromCenter(hood_m), FadeIn(ln), GrowArrow(arr), run_time=0.8)
        self.reg(hood_m, ln, arr)
        arr2 = Arrow([-1.6, 0.5, 0], np.array([-1.6, 0.5, 0]) + 2.35 * d,
                     buff=0, stroke_width=5.5, color=PURPLE,
                     max_tip_length_to_length_ratio=0.26)
        self.play(Transform(arr, arr2), run_time=1.1)
        txt = mt(r"A\alpha=\lambda\alpha", size=50, color=PURPLE).move_to([3.7, 0.5, 0])
        self.play(FadeIn(txt), run_time=0.5)
        self.reg(txt)
        self.sub_in("特征子空间里的向量只被拉长缩短、方向不动 —— 那更出不去了", 0.28)

    # ============================================================
    # 第3章  命题 6.6.1
    # ============================================================
    def ch3_prop661(self):
        self.map_light("one")

        bar = self.head("命题 6.6.1", color=BLUE)
        rows = [
            mixed(("t", "已知 ", INK), ("m", r"\mathcal{A}", INK),
                  ("t", " 是数域 ", INK), ("m", r"P", INK),
                  ("t", " 上的线性空间 ", INK), ("m", r"V", INK),
                  ("t", " 上的线性变换", INK), ts=32, ms=40),
            mixed(("m", r"\alpha\in V", INK),
                  ("t", " 是一个非零向量，则 ", INK),
                  ("m", r"L(\alpha)", GOLD),
                  ("t", " 是 ", INK), ("m", r"\mathcal{A}", GOLD),
                  ("t", "-子空间的", INK), ts=32, ms=44),
            mixed(("t", "充要条件", RED), ("t", "是 ", INK),
                  ("m", r"\alpha", RED),
                  ("t", " 是 ", INK), ("m", r"\mathcal{A}", RED),
                  ("t", " 的一个特征向量．", RED), ts=32, ms=44),
        ]
        card = problem_card("命题 6.6.1（教材原文）", rows, color=BLUE)
        card.move_to([0, 0.7, 0])
        self.show_rows([card], rt=1.0)
        self.wait(0.6)
        self.sub_in("一维子空间 想不变，等价于它整个方向就是特征方向", 0.3)
        self.wait(1.5)
        self.wipe()

        # 充分性
        self.head("① 充分性：α 是特征向量 ⟹ L(α) 不变", color=GREEN)
        hood_m = hood(rx=3.0, ry=1.9, color=GREEN).move_to([-2.4, 0.3, 0])
        self.play(GrowFromCenter(hood_m), run_time=0.5)
        self.reg(hood_m)
        line_dir = np.array([np.cos(0.42), np.sin(0.42), 0])
        base = np.array([-2.4, 0.3, 0])
        ln = Line(base - 2.3 * line_dir, base + 2.3 * line_dir).set_stroke(GREEN, 3.0)
        arr = Arrow(base, base + 1.5 * line_dir, buff=0, stroke_width=5.5,
                    color=GREEN, max_tip_length_to_length_ratio=0.26)
        self.play(FadeIn(ln), GrowArrow(arr), run_time=0.6)
        self.reg(ln, arr)
        arr2 = Arrow(base, base + 2.1 * line_dir, buff=0, stroke_width=5.5,
                     color=GREEN, max_tip_length_to_length_ratio=0.26)
        self.play(Transform(arr, arr2), run_time=1.0)
        eq = mt(r"A\alpha=\lambda\alpha", size=52, color=GREEN).move_to([3.9, 0.9, 0])
        note = mixed(("t", "还在这条直线上", INK), ts=32, ms=40).move_to([3.9, -0.2, 0])
        self.play(FadeIn(eq), run_time=0.4)
        self.play(FadeIn(note), run_time=0.4)
        self.reg(eq, note)
        self.sub_in("A 只是把 α 拉长/缩短，直线纹丝不动", 0.28)
        self.wait(1.3)
        self.wipe()

        # 必要性
        self.head("② 必要性：L(α) 不变 ⟹ α 是特征向量", color=RED)
        hood2 = hood(rx=3.0, ry=1.9, color=RED).move_to([-2.4, 0.3, 0])
        self.play(GrowFromCenter(hood2), run_time=0.5)
        self.reg(hood2)
        ln2 = Line(base - 2.3 * line_dir, base + 2.3 * line_dir).set_stroke(RED, 3.0)
        wild = Arrow(base, base + 1.9 * np.array([np.cos(0.95), np.sin(0.95), 0]),
                     buff=0, stroke_width=5.5, color=BLUE,
                     max_tip_length_to_length_ratio=0.26)
        self.play(FadeIn(ln2), GrowArrow(wild), run_time=0.7)
        self.reg(ln2, wild)
        self.play(Indicate(ln2, color=RED, scale_factor=1.04), run_time=0.8)
        x = VGroup(Line([-0.26, -0.26, 0], [0.26, 0.26, 0]),
                   Line([-0.26, 0.26, 0], [0.26, -0.26, 0])) \
            .set_stroke(RED, 5.5).move_to([3.9, 0.9, 0])
        self.play(GrowFromCenter(x), run_time=0.4)
        eq2 = mixed(("t", "那就必须 ", INK), ("m", r"A\alpha=\lambda\alpha", RED),
                    ts=32, ms=48).move_to([3.9, -0.2, 0])
        self.play(FadeIn(eq2), run_time=0.5)
        self.reg(x, eq2)
        self.sub_in("所以「一维不变子空间」和「特征向量」根本是同一件事", 0.3)
        self.wait(1.5)
        self.wipe()

    # ============================================================
    # 第4章  定理 1：根子空间是不变子空间
    # ============================================================
    def ch4_radical(self):
        self.map_light("radical")

        bar = self.head("定理 1：根子空间是 A 的不变子空间", color=GREEN)
        rows = [
            mixed(("t", "根子空间 ", INK), ("m", r"\ker(A-\lambda E)^k", GREEN),
                  ("t", " 是 ", INK), ("m", r"A", GREEN),
                  ("t", "-不变子空间．", GREEN), ts=36, ms=50),
        ]
        card = problem_card("定理 1（笔记）", rows, color=GREEN)
        card.move_to([0, 1.1, 0])
        self.show_rows([card], rt=0.9)
        self.wait(0.5)

        # 证明逐行（严格抄笔记）
        p1 = mt(r"\forall\,\alpha\in \ker\{(A-\lambda E)^k\}\ \Rightarrow\ (A-\lambda E)^k(\alpha)=0",
                size=44)
        p2 = mixed(("t", "则 ", INK),
                   ("m", r"(A-\lambda E)^k A(\alpha)=A(A-\lambda E)^k(\alpha)=0", RED),
                   ts=34, ms=44)
        p1.move_to([0, -0.95, 0])
        p2.move_to([0, -1.85, 0])
        self.play(FadeIn(p1), run_time=0.8)
        self.reg(p1)
        self.play(FadeIn(p2), run_time=0.9)
        self.reg(p2)

        # "交换" 这一步单独立一拍
        note = kai("← 这一步靠 A 与 (A-λE)^k 可交换", size=30)
        note.move_to([0, -2.62, 0])
        nb = note_box(note)
        self.play(FadeIn(nb), run_time=0.5)
        self.reg(nb)
        self.sub_in("A 和 (A-λE) 可交换，所以能把 A 提到括号外面", 0.3)
        self.wait(1.5)
        self.wipe()

        # 洋葱圈（左中位置 + 右侧文字说明，构图左右平衡）
        bar2 = self.head("根子空间是一颗洋葱", color=GREEN)
        base_c = np.array([-2.9, 0.18, 0])
        layers = VGroup()
        for i in range(3):
            e = Ellipse(width=2.5 + i * 1.55, height=1.5 + i * 1.0)
            e.set_stroke(GREEN, 3.0 - i * 0.55).set_fill(GREEN, 0.05 + i * 0.035)
            e.move_to(base_c)
            layers.add(e)
        cap = mixed(("t", "从里到外，一层套一层：", GREEN), ts=32, ms=40)
        cap.move_to([4.35, 1.85, 0])
        lbls = VGroup(
            mixed(("m", r"\ker(A-\lambda E)", GREEN),
                  ("t", "　最内层", GRAY), ts=26, ms=32),
            mixed(("m", r"\ker(A-\lambda E)^2", GREEN),
                  ("t", "　套两层", GRAY), ts=26, ms=32),
            mixed(("m", r"\ker(A-\lambda E)^k", GREEN),
                  ("t", "　套 k 层（最外层）", GRAY), ts=26, ms=32),
        )
        for i, l in enumerate(lbls):
            l.move_to([4.35, 0.95 - i * 0.85, 0])
        self.play(LaggedStart(*[GrowFromCenter(e) for e in layers], lag_ratio=0.16),
                  run_time=1.0)
        self.reg(layers)
        self.play(FadeIn(cap), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(l) for l in lbls], lag_ratio=0.14), run_time=0.7)
        self.reg(cap, lbls)
        nest = mixed(("t", "越往外，被捶的次数越多", GRAY), ts=28, ms=36)
        nest.move_to([4.35, -1.55, 0])
        self.play(FadeIn(nest), run_time=0.4)
        self.reg(nest)

        # 向量被捶 k 次
        v = Dot(base_c, radius=0.08, color=RED)
        self.play(FadeIn(v, scale=2.0), run_time=0.3)
        self.reg(v)
        for _ in range(2):
            self.play(Indicate(layers[0], color=RED, scale_factor=1.05), run_time=0.5)
        self.play(v.animate.scale(0.02).set_opacity(0.2), run_time=0.7)
        self.wait(0.4)

        # A 作用：整组洋葱圈不变
        ring = glow_ring(rx=2.85, ry=1.78, color=GOLD, times=3).move_to(base_c)
        self.play(FadeIn(ring), run_time=0.25)
        self.play(ring.animate.scale(1.25).set_opacity(0), run_time=0.7)
        st = stamp("✔ 整体不变", color=GOLD, size=32).move_to([4.35, -2.45, 0])
        self.play(GrowFromCenter(st), run_time=0.5)
        self.reg(st)
        self.sub_in("被 (A-λE) 反复捶 k 次会碎成 0 的向量，全住在一起 —— A 拆不开这个家", 0.3)
        self.wait(1.8)
        self.wipe()

    # ============================================================
    # 第5章  例 6.6.1（范德蒙矩阵）
    # ============================================================
    def ch5_example661(self):
        self.map_light("ex1")

        # ---- 抄题 ----
        bar = self.head("例 6.6.1", color=GOLD)
        rows = [
            mixed(("t", "设 ", INK), ("m", r"W", BLUE),
                  ("t", " 是线性变换 ", INK), ("m", r"A", BLUE),
                  ("t", " 的不变子空间，", INK), ("m", r"d\in W", BLUE),
                  ("t", "．", INK), ts=34, ms=44),
            mixed(("t", "若 ", INK), ("m", r"d=d_1+d_2+\cdots+d_m", GOLD),
                  ("t", "，", INK), ts=34, ms=46),
            mixed(("t", "其中 ", INK), ("m", r"d_1,d_2,\dots,d_m", GOLD),
                  ("t", " 分别是 ", INK), ("m", r"A", INK),
                  ("t", " 的属于", INK), ("t", "互不相同", RED),
                  ("t", "的特征值 ", INK),
                  ("m", r"\lambda_1,\lambda_2,\dots,\lambda_m", RED),
                  ("t", " 的特征向量，", INK), ts=32, ms=42),
            mixed(("t", "则每个 ", INK), ("m", r"d_i\in W", GREEN),
                  ("t", "（", INK), ("m", r"i=1,2,\dots,m", INK),
                  ("t", "）．", INK), ts=34, ms=46),
        ]
        card = problem_card("例 6.6.1（题面）", rows, color=GOLD)
        card.move_to([0, 0.45, 0])
        self.show_rows([card], rt=0.95)
        self.wait(0.7)
        self.sub_in("拼出来的 d 落在 W 里 —— 想知道能不能反过来，把每个 dᵢ 都揪出来", 0.3)
        self.wait(1.6)
        self.wipe()

        # ---- 可视化：d = Σ dᵢ ----
        bar = self.head("先看这个和是怎么拼出来的", color=GOLD)
        hood_m = hood(rx=3.5, ry=2.3, color=BLUE).move_to([-3.5, 0.35, 0])
        self.play(GrowFromCenter(hood_m), run_time=0.6)
        self.reg(hood_m)
        base = np.array([-3.5, 0.35, 0])
        dirs = [0.30, 1.05, 1.95, 2.90]
        cols = [GREEN, PURPLE, CYAN2, GOLD]
        labs = [r"\lambda_1", r"\lambda_2", r"\lambda_3", r"\lambda_4"]
        parts = VGroup()
        cur = base.copy()
        for i, (a, c) in enumerate(zip(dirs, cols)):
            nxt = cur + 0.72 * np.array([np.cos(a), np.sin(a), 0])
            parts.add(Arrow(cur, nxt, buff=0, stroke_width=5, color=c,
                            max_tip_length_to_length_ratio=0.30))
            cur = nxt
        self.play(LaggedStart(*[GrowArrow(a) for a in parts], lag_ratio=0.18),
                  run_time=1.2)
        self.reg(parts)
        for i, (a, l, c) in enumerate(zip(dirs, labs, cols)):
            m = mt(l, size=30, color=c).move_to(base + 0.95 * np.array([np.cos(a), np.sin(a), 0]))
            self.play(FadeIn(m), run_time=0.25)
            self.reg(m)
        d_arr = Arrow(base, cur, buff=0, stroke_width=6, color=RED,
                      max_tip_length_to_length_ratio=0.22)
        self.play(GrowArrow(d_arr), run_time=0.6)
        dl = mt(r"d", size=46, color=RED).next_to(d_arr.get_end(), RIGHT, buff=0.14)
        self.play(FadeIn(dl), run_time=0.3)
        self.reg(d_arr, dl)
        eq = mt(r"d=d_1+d_2+\cdots+d_m\ \in W", size=48, color=INK)
        eq.move_to([3.6, 0.6, 0])
        inw = mixed(("t", "d 落在罩子里", BLUE), ts=32, ms=40).move_to([3.6, -0.5, 0])
        self.play(FadeIn(eq), run_time=0.5)
        self.play(FadeIn(inw), run_time=0.4)
        self.reg(eq, inw)
        self.sub_in("四个不同方向的箭头拼成 d —— d 在 W 里", 0.28)
        self.wait(1.5)
        self.wipe()

        # ---- 钥匙：A^k d ∈ W ----
        bar = self.head("钥匙：A 怎么捶，d 都跑不出 W", color=BLUE)
        hood_m = hood(rx=3.2, ry=2.05, color=BLUE).move_to([-3.6, 0.35, 0])
        self.play(GrowFromCenter(hood_m), run_time=0.5)
        self.reg(hood_m)
        chain = VGroup()
        cur = np.array([-3.6, 0.35, 0])
        for i in range(4):
            nxt = cur + 0.62 * np.array([np.cos(0.45 + 0.55 * i),
                                         np.sin(0.45 + 0.55 * i), 0])
            chain.add(Arrow(cur, nxt, buff=0, stroke_width=5.5,
                            color=[RED, CYAN2, PURPLE, GOLD][i],
                            max_tip_length_to_length_ratio=0.28))
            cur = nxt
        self.play(LaggedStart(*[GrowArrow(a) for a in chain], lag_ratio=0.22),
                  run_time=1.3)
        self.reg(chain)
        chain_lab = mt(r"d,\ Ad,\ A^2d,\ \dots,\ A^{m-1}d\ \in W", size=46, color=RED)
        chain_lab.move_to([3.9, 0.75, 0])
        self.play(FadeIn(chain_lab), run_time=0.6)
        self.reg(chain_lab)
        self.sub_in("W 是不变子空间 ⇒ d∈W，Ad∈W，… ，A^{m-1}d 全都在 W 里", 0.3)
        self.wait(1.6)
        self.wipe()

        # ---- 两边转置 + 方程组 ----
        bar = self.head("两边转置，再让 k 取遍 0,1,…,m-1", color=PURPLE)
        t1 = mt(r"\sum_{i=1}^{m} d_i=d", size=48, color=INK)
        t2 = mt(r"\sum_{i=1}^{m} d_i'=d'", size=48, color=PURPLE)
        t1.move_to([-3.4, 1.6, 0])
        t2.move_to([3.4, 1.6, 0])
        self.play(FadeIn(t1), run_time=0.5)
        self.play(FadeIn(t2), run_time=0.5)
        self.reg(t1, t2)
        tr = mixed(("t", "两边转置", ORANGE), ts=30, ms=40).move_to([0, 2.35, 0])
        arr = Arrow([-0.7, 1.6, 0], [0.7, 1.6, 0], buff=0, stroke_width=4,
                    color=ORANGE, max_tip_length_to_length_ratio=0.26)
        self.play(FadeIn(tr), GrowArrow(arr), run_time=0.5)
        self.reg(tr, arr)

        sys_rows = [
            mt(r"\sum_{i=1}^{m}\lambda_i d_i'=Ad'", size=42),
            mt(r"\sum_{i=1}^{m}\lambda_i^2 d_i'=A^2d'", size=42),
            mt(r"\vdots", size=36),
            mt(r"\sum_{i=1}^{m}\lambda_i^{m-1} d_i'=A^{m-1}d'", size=42),
        ]
        sysg = VGroup(*sys_rows).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        sysg.move_to([-1.0, -1.25, 0])
        brace = Brace(sysg, LEFT, color=PURPLE)
        brace.next_to(sysg, LEFT, buff=0.10)
        self.play(FadeIn(sysg), run_time=0.9)
        self.reg(sysg, brace)
        kk = mt(r"k=0,1,2,\dots,m-1", size=42, color=PURPLE)
        kk.move_to([5.0, -0.9, 0])
        self.play(FadeIn(kk), run_time=0.4)
        self.reg(kk)
        self.sub_in("每代一个 k，就得到一个方程 —— 一共 m 个方程", 0.28)
        self.wait(1.6)
        self.wipe()

        # ---- 范德蒙矩阵登场 ★ 高潮 ----
        bar = self.head("写成矩阵等式 —— 救兵到场", color=GOLD)
        lam = [r"\lambda_1", r"\lambda_2", r"\lambda_3", r"\lambda_4"]
        V = vander_matrix(lam, cell_w=0.80, gap=0.05, n_rows=4)
        L = vec_col([r"d_1'", r"d_2'", r"d_3'", r"d_4'"],
                    cell_w=0.80, gap=0.05, color=CG, fill=CFG, font_size=36)
        R = vec_col([r"d'", r"(Ad)'", r"(A^2d)'", r"(A^3d)'"],
                    cell_w=0.80, gap=0.05, color=CR, fill=CFR, font_size=30)
        eq1 = mt(r"\cdot", size=46, color=INK)      # 矩阵 × 向量：这里是乘号，不是等号
        eq2 = mt(r"=", size=46, color=INK)          # 向量 = 向量
        eqg = VGroup(V, eq1, L, eq2, R).arrange(RIGHT, buff=0.24)
        eqg.move_to([-2.3, -0.35, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.85) for c in V[0]],
                              lag_ratio=0.05), run_time=0.9)
        self.play(FadeIn(V[1]), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in L[0]], lag_ratio=0.08),
                  FadeIn(eq1), run_time=0.6)
        self.play(FadeIn(L[1]), run_time=0.25)
        self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in R[0]], lag_ratio=0.08),
                  FadeIn(eq2), run_time=0.6)
        self.play(FadeIn(R[1]), run_time=0.25)
        self.reg(eqg)

        nm = mixed(("t", "范德蒙矩阵", GOLD), ts=32, ms=40)
        nm.next_to(V, UP, buff=0.22)
        self.play(FadeIn(nm), run_time=0.4)
        self.reg(nm)
        ex = mixed(("t", "（这里以 m = 4 为例）", GRAY), ts=26, ms=32)
        ex.next_to(nm, UP, buff=0.16)
        self.play(FadeIn(ex), run_time=0.35)
        self.reg(ex)

        det = mt(r"\det =\prod_{i<j}(\lambda_j-\lambda_i)\neq 0", size=44, color=GOLD)
        det.move_to([4.15, 1.15, 0])
        self.play(FadeIn(det), run_time=0.6)
        self.reg(det)
        st = stamp("可逆", color=GOLD, size=44).move_to([4.3, -1.5, 0])
        self.play(GrowFromCenter(st), run_time=0.55)
        self.reg(st)
        self.sub_in("λᵢ 互不相同 ⇒ 这个矩阵可逆 ⇒ 方程能解出唯一解", 0.3)
        self.wait(1.7)
        self.wipe()

        # ---- 结论 ----
        bar = self.head("解出来的东西，全在 W 里", color=GREEN)
        l1 = mixed(("t", "① 因为矩阵可逆，每个 ", INK), ("m", r"d_i", GREEN),
                   ("t", " 都可由 ", INK), ("m", r"d,\ Ad,\ \dots,\ A^{m-1}d", RED),
                   ("t", " 线性组合", INK), ts=32, ms=42)
        l2 = mixed(("t", "② 而右边这些向量", GREEN),
                   ("m", r"\in W", GREEN), ("t", "（上一拍刚证过）", GREEN),
                   ts=32, ms=44)
        l3 = mixed(("t", "③ W 对线性组合封闭 ⇒ ", INK),
                   ("m", r"d_i\in W", GOLD), ("t", "，i = 1,2,…,m", INK),
                   ts=32, ms=46)
        flow = VGroup(l1, l2, l3).arrange(DOWN, buff=0.62, aligned_edge=LEFT)
        flow.move_to([0, 0.2, 0])
        for r in [l1, l2, l3]:
            self.play(FadeIn(r), run_time=0.8)
            self.reg(r)
        box = hilite_box(l3, color=GOLD)
        self.play(FadeIn(box), run_time=0.5)
        self.reg(box)
        self.sub_in("范德蒙矩阵可逆 ⇒ 把每个 dᵢ 一个个解出来 ⇒ 解出来的全在 W 里", 0.3)
        self.wait(1.8)
        self.wipe()

        # ---- 补注：推论（全节主线） ----
        bar = self.head("顺便说一句，这才是本题真正的意义", color=PURPLE)
        c1 = mixed(("t", "① 任何含 ", INK), ("m", r"d", INK),
                   ("t", " 的不变子空间，都必须包含 ", INK),
                   ("m", r"d,A d,\dots,A^{m-1}d", INK),
                   ("t", " ⇒ 必须包含每个 ", INK), ("m", r"d_i", BLUE), ts=30, ms=42)
        c2 = mixed(("t", "② 而 ", INK), ("m", r"L(d_1,\dots,d_m)", BLUE),
                   ("t", " 本身也是 ", INK), ("m", r"A", BLUE),
                   ("t", "-不变的，且含 ", INK), ("m", r"d", BLUE), ts=30, ms=42)
        c3 = mixed(("t", "③ 所以它就是", INK),
                   ("m", r"L(d_1,\dots,d_m)", GOLD),
                   ("t", " —— 含 d 的", INK), ("t", "最小", RED),
                   ("t", "不变子空间", INK), ts=30, ms=44)
        c4 = mixed(("t", "④ 取基 ", INK), ("m", r"(d_1,\dots,d_m)", GOLD),
                   ("t", "，则 ", INK), ("m", r"A|W = \mathrm{diag}(\lambda_1,\dots,\lambda_m)", GOLD),
                   ts=30, ms=44)
        cflow = VGroup(c1, c2, c3, c4).arrange(DOWN, buff=0.58, aligned_edge=LEFT)
        cflow.move_to([0, 0.15, 0])
        for r in [c1, c2, c3, c4]:
            rr = note_box(r)
            self.play(FadeIn(rr), run_time=0.7)
            self.reg(rr)
        self.sub_in("不变子空间的终极用途：把 A 的矩阵化简成（准）对角块", 0.3)
        self.wait(1.9)
        self.wipe()

    # ============================================================
    # 上集结尾：地图点亮 + 敬请期待下期
    # ============================================================
    def s_end(self):
        mm, k2i, i2n = build_knowledge_map()
        done_keys = ["def", "trio", "one", "radical", "ex1"]
        todo_keys = ["comm", "ex2", "ex4"]
        paint_map(i2n, lit_ids=lit_ids_upto("ex1", k2i),
                  todo_ids=[k2i[k] for k in todo_keys])
        self.hard_clear()
        # 结尾再长一遍（比开场快一点，每节点 0.42s ≈ 5.5s），然后逐个脉冲点亮
        self.grow_map(i2n, node_rt=0.42)
        for k in done_keys:
            nd = i2n[k2i[k]]
            ring = glow_ring(rx=nd.surr_rect.width * 0.60,
                             ry=nd.surr_rect.height * 0.88, color=GOLD, times=2)
            ring.move_to(nd.surr_rect.get_center())
            self.play(FadeIn(ring), run_time=0.10)
            self.play(ring.animate.scale(1.7).set_opacity(0), run_time=0.34)
        self.sub_in("上集讲完了定义、三兄弟、根子空间、范德蒙拆解", 0.28)
        self.wait(1.5)

        # 下集预告：用一块半透明纸面板压住地图，保证文字清晰
        # （★ 不改地图本身颜色的透明度 —— 那会让黑框白字糊成一片）
        panel = RoundedRectangle(corner_radius=0.22, width=13.6, height=3.9)
        panel.set_fill(BG, 1.0).set_stroke(GOLD, 2.6)
        panel.move_to([0, 0.25, 0])
        self.play(FadeIn(panel), run_time=0.45)
        self.reg(panel)
        t1 = song("下集预告", size=62, color=PURPLE)
        t2 = Text("不变子空间在更难的题里有多好用？", font=HEI, font_size=40,
                  color=INK, weight="BOLD")
        t3 = mixed(("t", "比如 ", INK), ("m", r"AB=BA", GOLD),
                   ("t", " 的公共特征向量问题", GOLD), ts=40, ms=52)
        g = VGroup(t1, t2, t3).arrange(DOWN, buff=0.5).move_to([0, 0.25, 0])
        self.play(FadeIn(t1, scale=1.1), run_time=0.6)
        self.play(FadeIn(t2), run_time=0.5)
        self.play(FadeIn(t3), run_time=0.5)
        self.reg(t1, t2, t3)
        self.sub_in("敬请期待下一期", 0.28)
        self.wait(2.2)
        self.wipe()







