# -*- coding: utf-8 -*-
"""
《不变子空间》动画讲解片 · 组件库
风格：Manim 宋体定理片（若尔当标准型风格）× 横屏大字公式规范

★ 字体规范（2026-09-24 定稿，全片统一）：
  正文汉字 + 标题 + 字幕 → 宋体 Songti SC（加粗）；手写感批注 → 楷体 Kaiti SC。
  （原先正文用 PingFang SC 黑体，用户反馈「方方正正、不护眼」，已统一为宋体。）
★ 汉字 + 公式混排必须 VGroup 封装（用户强调多次）：
  mixed() 正文行 / mixlabel() 标题 / subs() 字幕 / kaimix() 批注；
  公式一律 MathTex（LaTeX 斜体），绝不允许写进 Text 字符串。
★ 文字/公式入场一律 Write() 逐字写出；图形类才用 GrowFromCenter / FadeIn(lag_ratio)。
"""
import numpy as np
from manim import *

# ================= 全局配置 =================
config.pixel_width, config.pixel_height = 1920, 1080
config.frame_width, config.frame_height = 16.0, 9.0
config.background_color = "#FBF6EF"
config.media_dir = "./media"

# ---- 沙箱兼容（重要）----
# manim 每编译一次公式都会调用 delete_nonsvg_files() 删掉 .aux/.log/.dvi 等辅助文件，
# 一部片子上千次删除会触发本机沙箱的"批量删除保护"而中断渲染。
# 这些辅助文件留在原地完全无害（LaTeX 会覆盖重写），故关掉该清理动作；
# 同时把 partial movie 的缓存上限拉高，避免渲染中途删旧片段。
config["no_latex_cleanup"] = True
config["max_files_cached"] = 1000000

# ================= 调色板 =================
BG = "#FBF6EF"
RED = "#E8535A"
BLUE = "#4A9DE8"
GREEN = "#2BB89A"
PURPLE = "#8B7BE8"
GOLD = "#E8A84B"
CYAN2 = "#35B8B0"
INK = "#3A3A3C"
GRIDC = "#E8E0D6"
GRAY = "#A9A29A"

CB, CFB = "#4A9DE8", "#EAF3FC"
CR, CFR = "#E8535A", "#FBE9E9"
CG, CFG = "#2BB89A", "#E9F7F1"
CGR, CFGR = "#B8AFA5", "#F6F1EA"

CELL = 0.92
SONG = "Songti SC"     # ★ 全片统一字体：标题 / 正文 / 字幕（加粗）
HEI = "PingFang SC"    # 已弃用：黑体笔画均匀，用户嫌"方方正正"，仅留作兜底
KAI = "Kaiti SC"       # 手写感批注（note_box 里）

# ================= 文字与公式 =================
# ★ 2026-09-24 用户要求：正文汉字字体与标题统一 —— 全部用宋体 Songti SC（黑体太方正、不护眼）。
#   大小（font_size）保持不变，只换字体。公式一律走 MathTex（LaTeX 斜体），不进 Text。
def zh(s, size=38, color=INK, weight=NORMAL, font=SONG):
    return Text(s, font=font, font_size=size, color=color, weight=weight)

def song(s, size=44, color=INK, weight="BOLD"):
    return Text(s, font=SONG, font_size=size, color=color, weight=weight)

def kai(s, size=32, color=GOLD):
    return Text(s, font=KAI, font_size=size, color=color)

def mt(s, size=52, color=INK, sw=1):
    return MathTex(s, font_size=size, color=color, stroke_width=sw)

def mixed(*items, ts=38, ms=46, color=INK, buff=0.12, weight="BOLD"):
    """
    ★ 汉字 + 公式混排的**唯一正确方式：VGroup 封装**（用户强调多次，不许用 Text 硬拼公式）。
      汉字 → Text(宋体 Songti SC 加粗 = 与标题同款字体)；公式 → MathTex（LaTeX 斜体，绝不用正体）。
    items: ('t', 中文, 颜色) 或 ('m', latex, 颜色)
    """
    parts = []
    for kind, content, col in items:
        c = col if col else color
        if kind == "t":
            parts.append(zh(content, size=ts, color=c, weight=weight))
        else:
            parts.append(mt(content, size=ms, color=c))
    return VGroup(*parts).arrange(RIGHT, buff=buff)


def subs(*items, ts=29, ms=34, buff=0.10):
    """底部字幕专用混排：汉字（宋体加粗白字）+ 公式（MathTex 斜体白字），VGroup 封装。"""
    parts = []
    for it in items:
        kind, content = it[0], it[1]
        if kind == "t":
            parts.append(Text(content, font=SONG, font_size=ts, color=WHITE, weight="BOLD"))
        else:
            parts.append(MathTex(content, font_size=ms, color=WHITE, stroke_width=1.6))
    return VGroup(*parts).arrange(RIGHT, buff=buff)


def kaimix(*items, ts=26, ms=30, color=GOLD, buff=0.10):
    """补注混排：汉字用楷体 Kaiti SC（手写感），公式用 MathTex，VGroup 封装。"""
    parts = []
    for it in items:
        kind, content = it[0], it[1]
        c = it[2] if len(it) > 2 else color
        if kind == "t":
            parts.append(Text(content, font=KAI, font_size=ts, color=c))
        else:
            parts.append(MathTex(content, font_size=ms, color=c))
    return VGroup(*parts).arrange(RIGHT, buff=buff)

def fit(mob, width=None, height=None):
    tw = width if width is not None else config.frame_width - 1.2
    th = height if height is not None else config.frame_height - 1.0
    if mob.width > tw:
        mob.scale_to_fit_width(tw)
    if mob.height > th:
        mob.scale_to_fit_height(th)
    return mob

# ================= 背景网格（永驻） =================
def make_grid():
    grid = VGroup()
    for x in np.arange(-8, 8.01, 0.8):
        grid.add(Line([x, -4.6, 0], [x, 4.6, 0]).set_stroke(GRIDC, 1.2, 0.8))
    for y in np.arange(-4.4, 4.61, 0.8):
        grid.add(Line([-8, y, 0], [8, y, 0]).set_stroke(GRIDC, 1.2, 0.8))
    return grid

# ================= 标题栏 / 字幕 =================
def title_bar(text, color=BLUE, size=48, font=SONG, weight="BOLD"):
    """标题栏。text 传字符串（纯中文标题）或 Mobject（汉字+公式混排的 VGroup）。"""
    if isinstance(text, str):
        t = Text(text, font=font, font_size=size, color=color, weight=weight)
    else:
        t = text
    t.to_edge(UP, buff=0.34)
    return VGroup(t)


def mixlabel(*items, color=BLUE, ts=40, ms=44, buff=0.12):
    """
    ★ 标题里的「汉字 + 公式」必须 VGroup 封装（用户强调多次）：
      汉字走 Text(宋体加粗)、公式走 MathTex（LaTeX 斜体），
      绝不允许把公式写进 Text 字符串 —— 那样既不是斜体、也没法正确排版。
    items: ('t', 中文) 或 ('m', latex)，第三项可覆盖该项颜色。
    """
    parts = []
    for it in items:
        kind, content = it[0], it[1]
        col = it[2] if len(it) > 2 else color
        if kind == "t":
            parts.append(zh(content, size=ts, color=col, weight="BOLD"))
        else:
            parts.append(mt(content, size=ms, color=col))
    return VGroup(*parts).arrange(RIGHT, buff=buff)

def sub_bar(text, size=29):
    """底部硬字幕：深色圆角底条 + 白字。
    text 可传字符串，或「汉字 + 公式」混排的 VGroup（公式必须是 MathTex 斜体）。"""
    if isinstance(text, str):
        t = Text(text, font=SONG, font_size=size, color=WHITE, weight="BOLD")
    else:
        t = text
    bg = RoundedRectangle(corner_radius=0.16, width=t.width + 0.66, height=t.height + 0.34)
    bg.set_fill("#2C2C2A", 1).set_stroke(width=0)
    bg.move_to(t)
    g = VGroup(bg, t)
    if g.width > 15.0:
        g.scale_to_fit_width(15.0)
    g.move_to([0, -3.5, 0])
    return g

# ================= 彩色格子矩阵 =================
def cell(sym, edge, fill, cell_w=CELL, font_size=38, sym_color=None):
    sq = RoundedRectangle(corner_radius=0.13, width=cell_w, height=cell_w)
    sq.set_stroke(edge, 2.4).set_fill(fill, 1)
    t = MathTex(sym, font_size=int(font_size * cell_w / CELL),
                color=sym_color or edge).move_to(sq.get_center())
    return VGroup(sq, t)

def bracket(h, color=BLUE, sw=3.4, w=0.0):
    """矩阵括号；w 为矩阵总宽度（★必须传，否则括号会叠在中间）"""
    half, arm = h / 2, 0.22
    ww = w if w > 0 else h * 0.42
    L = VGroup(
        Line([0, -half, 0], [0, half, 0]).set_stroke(color, sw),
        Line([0, half, 0], [arm, half, 0]).set_stroke(color, sw),
        Line([0, -half, 0], [arm, -half, 0]).set_stroke(color, sw),
    ).move_to([-ww / 2, 0, 0])
    R = VGroup(
        Line([0, -half, 0], [0, half, 0]).set_stroke(color, sw),
        Line([0, half, 0], [-arm, half, 0]).set_stroke(color, sw),
        Line([0, -half, 0], [-arm, -half, 0]).set_stroke(color, sw),
    ).move_to([ww / 2, 0, 0])
    return VGroup(L, R)

def grid_matrix(entries, cell_w=CELL, gap=0.06, font_size=38, br_color=BLUE):
    """entries: n×m 的 (sym, edge, fill)；返回整体（格子+括号），几何中心在原点"""
    n, m = len(entries), len(entries[0])
    cells = VGroup()
    for i in range(n):
        for j in range(m):
            sym, edge, fill = entries[i][j]
            c = cell(sym, edge, fill, cell_w=cell_w, font_size=font_size)
            c.move_to([(j - (m - 1) / 2) * (cell_w + gap),
                       ((n - 1) / 2 - i) * (cell_w + gap), 0])
            cells.add(c)
    side_w = m * cell_w + (m - 1) * gap
    side_h = n * cell_w + (n - 1) * gap
    br = bracket(side_h + 0.16, color=br_color, w=side_w + 0.14)
    return VGroup(cells, br)

def vander_matrix(lam_labels, cell_w=0.86, gap=0.05, n_rows=None):
    """范德蒙矩阵：行依次为 1, λ_i, λ_i^2, ...（λ 用给定标签渲染）"""
    m = len(lam_labels)
    rows = n_rows if n_rows else m
    entries = []
    for r in range(rows):
        row = []
        for c in range(m):
            sym = "1" if r == 0 else (
                lam_labels[c] if r == 1 else rf"{lam_labels[c]}^{{{r}}}")
            row.append((sym, CB, CFB))
        entries.append(row)
    return grid_matrix(entries, cell_w=cell_w, gap=gap, font_size=34)

def vec_col(syms, cell_w=0.86, gap=0.05, color=CR, fill=CFR, font_size=40):
    entries = [[(s, color, fill)] for s in syms]
    return grid_matrix(entries, cell_w=cell_w, gap=gap,
                       font_size=font_size, br_color=color)

# ================= 印章 / 补注框 / 高亮 =================
def stamp(text, color=RED, size=40, angle=-0.18):
    """印章：粗描边圆角方框 + 宋体字"""
    t = Text(text, font=SONG, font_size=size, color=color, weight="BOLD")
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.5, height=t.height + 0.3)
    box.set_stroke(color, 4.5).set_fill(color, 0.10)
    box.move_to(t)
    g = VGroup(box, t).rotate(angle)
    return g

def note_box(mob, color=GOLD, pad=0.16):
    """补注虚线框：把我的补注与笔记原文区分开"""
    r = RoundedRectangle(corner_radius=0.12,
                         width=mob.width + 2 * pad, height=mob.height + 2 * pad)
    r.set_stroke(color, 2.0).set_fill(color, 0.07)
    r.move_to(mob)
    return VGroup(DashedVMobject(r, num_dashes=42), mob)

def hilite(mob, color=GOLD, pad=0.14):
    """毛玻璃高亮框（把文字一起包进去）"""
    r = RoundedRectangle(corner_radius=0.12,
                         width=mob.width + 2 * pad, height=mob.height + 2 * pad)
    r.set_stroke(color, 3.2).set_fill(color, 0.22)
    r.move_to(mob)
    return VGroup(r, mob)

def hilite_box(mob, color=GOLD, pad=0.16):
    """只返回高亮框本身（不包裹 mob）—— 对象已经在场景里时用这个，
    避免「把已入场的 mob 重新塞进新 VGroup」造成的重复引用与淡出残影。"""
    r = RoundedRectangle(corner_radius=0.13,
                         width=mob.width + 2 * pad, height=mob.height + 2 * pad)
    r.set_stroke(color, 3.2).set_fill(color, 0.20)
    r.move_to(mob)
    return r

# ================= 抄题卡片（本项目核心：先抄题再证明） =================
def problem_card(label, lines, color=BLUE, fill=None, pad=0.34,
                 tag_size=32, line_buff=0.30, max_w=13.8):
    """
    抄题卡片：左上角标签（如「定理 6.6.1」）+ 题面若干行
    lines: list of Mobject（每行一个，中文用 Text、公式用 MathTex，或 VGroup 混排）
    """
    fill = fill or ManimColor(color).interpolate(ManimColor(WHITE), 0.90)
    body = VGroup(*lines).arrange(DOWN, buff=line_buff, aligned_edge=LEFT)
    if body.width > max_w - 2 * pad:
        body.scale_to_fit_width(max_w - 2 * pad)
    tag = Text(label, font=SONG, font_size=tag_size, color=color, weight="BOLD")
    inner_w = max(body.width, tag.width) + 2 * pad
    inner_h = body.height + tag.height + 2 * pad + 0.24
    box = RoundedRectangle(corner_radius=0.18, width=inner_w, height=inner_h)
    box.set_fill(fill, 1).set_stroke(color, 2.8)
    tag.move_to(box.get_corner(UL) + [pad + tag.width / 2, -pad - tag.height / 2, 0])
    body.next_to(tag, DOWN, buff=0.26).align_to(tag, LEFT)
    return VGroup(box, tag, body)

def proof_flow(rows, color=INK, buff=0.46, align_left=True):
    """证明过程的逐行流（左对齐）"""
    g = VGroup(*rows)
    g.arrange(DOWN, buff=buff, aligned_edge=LEFT if align_left else ORIGIN)
    return g

# ================= 罩子 / 向量云 / 火柴人 =================
def hood(rx=3.3, ry=2.2, color=BLUE, label="W", label_pos=UP):
    """不变子空间的「罩子」：半透明发光区域"""
    e = Ellipse(width=2 * rx, height=2 * ry)
    e.set_stroke(color, 3.2).set_fill(color, 0.10)
    t = MathTex(label, font_size=44, color=color).move_to(e.get_center() + label_pos * ry * 0.78)
    return VGroup(e, t)

def glow_ring(rx=3.3, ry=2.2, color=GOLD, times=3):
    rings = VGroup()
    for i in range(times):
        e = Ellipse(width=2 * rx, height=2 * ry)
        e.set_stroke(color, 5 - i, opacity=0.55 - 0.15 * i).set_fill(opacity=0)
        rings.add(e)
    return rings

def vector_cloud(n=12, rmax=1.0, seed=7, color=None, w=3.0, tip=0.16):
    """从原点散出的向量箭头"""
    rng = np.random.default_rng(seed)
    cols = [BLUE, GREEN, PURPLE, CYAN2, GOLD, RED]
    g = VGroup()
    for i in range(n):
        a = rng.uniform(0, 2 * np.pi)
        r = rng.uniform(0.55, 1.0) * rmax
        col = color or cols[i % len(cols)]
        p = np.array([np.cos(a) * r, np.sin(a) * r, 0])
        ar = Arrow(ORIGIN, p, buff=0, stroke_width=w,
                   max_tip_length_to_length_ratio=0.30,
                   color=col, tip_length=tip)
        ar.set_opacity(0.92)
        g.add(ar)
    return g

def transform_cloud(cloud, mat):
    """把向量云按 2×2 矩阵线性变换，返回新的向量云（箭头形状不变）"""
    m = np.array(mat, dtype=float)
    g = VGroup()
    for ar in cloud:
        p = ar.get_end()[:2]
        q = m @ p
        v = np.array([q[0], q[1], 0])
        g.add(Arrow(ORIGIN, v, buff=0,
                    stroke_width=ar.get_stroke_width(),
                    max_tip_length_to_length_ratio=0.30,
                    color=ar.get_color(), tip_length=0.16))
    for k, ar in enumerate(g):
        ar.set_opacity(cloud[k].get_stroke_opacity())
    return g

def stick_man(scale=1.0, color=INK, mood="happy"):
    """火柴人：圆头 + 躯干 + 手脚"""
    head = Circle(radius=0.16).set_stroke(color, 2.6).set_fill(WHITE, 1)
    body = Line([0, -0.14, 0], [0, -0.62, 0]).set_stroke(color, 2.6)
    if mood == "happy":
        arm_l = Line([0, -0.30, 0], [-0.26, -0.12, 0])
        arm_r = Line([0, -0.30, 0], [0.26, -0.12, 0])
    elif mood == "sad":
        arm_l = Line([0, -0.30, 0], [-0.24, -0.52, 0])
        arm_r = Line([0, -0.30, 0], [0.24, -0.52, 0])
    else:
        arm_l = Line([0, -0.30, 0], [-0.30, -0.30, 0])
        arm_r = Line([0, -0.30, 0], [0.30, -0.30, 0])
    leg_l = Line([0, -0.62, 0], [-0.20, -0.94, 0]).set_stroke(color, 2.6)
    leg_r = Line([0, -0.62, 0], [0.20, -0.94, 0]).set_stroke(color, 2.6)
    g = VGroup(head, body,
               arm_l.set_stroke(color, 2.6), arm_r.set_stroke(color, 2.6),
               leg_l, leg_r).scale(scale)
    return g

def ripple(color=GOLD, layers=4):
    g = VGroup()
    for i in range(layers):
        g.add(Circle(radius=0.6 + i * 0.55)
              .set_stroke(color, width=0, opacity=0).set_fill(color, 0.18 - i * 0.035))
    return g

def gold_seam(points, color=GOLD, w=4.5):
    """金色缝合折线"""
    m = VMobject().set_points_as_corners([np.array(p) for p in points]).set_stroke(color, w)
    return m

# ================= 知识地图（manim-mindmap） =================
# ★ 视觉规范（2026-09-23 按用户要求定稿）：
#   节点 = 实心深色长方形 + 白色文字（跟米白背景强对比，手机上看得清）。
#   「点亮」= 底色更黑 + 金色描边 + 文字变金；「未讲」= 深灰底 + 暖白字。
#   ★ 绝对不要用透明度去压暗（半透明深底+半透明白字在米白纸面上会糊成一片）。
MAP_BOX_ROOT = "#1C1A17"
MAP_BOX_L2 = "#302C26"
MAP_BOX_L3 = "#403A32"
MAP_BOX_DIM = "#56504A"
MAP_BOX_TODO = "#8C857B"

MAP_TXT = "#FAF6EF"
MAP_TXT_LIT = "#FFD27A"
MAP_TXT_DIM = "#E9E3D8"
MAP_TXT_TODO = "#F2EDE4"

MAP_EDGE_DIM = "#8A8278"
MAP_EDGE_LIT = GOLD
MAP_EDGE_TODO = "#7A736A"

# 每关一个 key，点亮是「累积」的：讲过的节点一直保持亮
MAP_LIT_ORDER = ["def", "trio", "one", "radical", "ex1",
                 "comm", "ex2", "ex4"]

# 逐节点生长时的出场顺序（深度优先 = 正好就是讲课顺序）
MAP_DFS_ORDER = [
    (0,),                                        # 不变子空间
    (0, 0),                                      # 定义
    (0, 1), (0, 1, 0), (0, 1, 1), (0, 1, 2),     # 天然三兄弟 → 核/值域/特征子空间
    (0, 2),                                      # 一维情形
    (0, 3),                                      # 根子空间
    (0, 4),                                      # 例6.6.1
    (0, 5), (0, 6), (0, 7),                      # 可交换 / 例6.6.2 / 例6.6.4
]


def _nlabel(*parts, size=27, color=MAP_TXT, ms=30):
    """节点标签：中文用 Text(宋体)、公式用 MathTex，混排（VGroup 封装）"""
    g = VGroup()
    for kind, content in parts:
        if kind == "t":
            g.add(Text(content, font=SONG, font_size=size, color=color, weight="BOLD"))
        else:
            g.add(MathTex(content, font_size=ms, color=color))
    return g.arrange(RIGHT, buff=0.14)


def knowledge_map_data():
    """返回 (map_dict, key2id)：key2id 用于后续「点亮」某个节点"""
    root = {
        "node": Text("不变子空间", font=SONG, font_size=44,
                     color=MAP_TXT, weight="BOLD"),
        "child": [],
    }
    root["child"] = [
        {"node": _nlabel(("t", "定义"), ("m", r"\forall\alpha\in W,\ A\alpha\in W"))},
        {"node": _nlabel(("t", "天然三兄弟 · 定理6.6.1")), "child": [
            {"node": _nlabel(("t", "核"), ("m", r"\ker A"))},
            {"node": _nlabel(("t", "值域"), ("m", r"\mathrm{Im}\,A"))},
            {"node": _nlabel(("t", "特征子空间"), ("m", r"V_\lambda"))},
        ]},
        {"node": _nlabel(("t", "一维情形 · 命题6.6.1"))},
        {"node": _nlabel(("t", "根子空间"), ("m", r"\ker(A-\lambda E)^k"))},
        {"node": _nlabel(("t", "例6.6.1 · 范德蒙拆解"))},
        {"node": _nlabel(("t", "可交换 · 命题6.6.2"))},
        {"node": _nlabel(("t", "例6.6.2 · 公共特征向量"))},
        {"node": _nlabel(("t", "例6.6.4 · 苏州大学真题"))},
    ]
    key2id = {
        "root": (0,),
        "def": (0, 0),
        "trio": (0, 1),
        "ker": (0, 1, 0), "im": (0, 1, 1), "eig": (0, 1, 2),
        "one": (0, 2),
        "radical": (0, 3),
        "ex1": (0, 4),
        "comm": (0, 5),
        "ex2": (0, 6),
        "ex4": (0, 7),
    }
    return root, key2id


def _map_node_style():
    """节点/连线样式：实心深底 + 白字（level 从 1 开始，故索引 0 是占位）"""
    from manim_mindmap import NodeStyle
    return NodeStyle(
        node_style=[
            {"color": MAP_BOX_DIM, "fill_color": MAP_BOX_DIM,
             "fill_opacity": 1.0, "stroke_width": 2.0},                      # 0 占位
            {"color": MAP_BOX_ROOT, "fill_color": MAP_BOX_ROOT,
             "fill_opacity": 1.0, "stroke_width": 3.2},                      # 1 根
            {"color": MAP_BOX_L2, "fill_color": MAP_BOX_L2,
             "fill_opacity": 1.0, "stroke_width": 2.6},                      # 2 二级
            {"color": MAP_BOX_L3, "fill_color": MAP_BOX_L3,
             "fill_opacity": 1.0, "stroke_width": 2.2},                      # 3 三级
        ],
        line_style=[
            {"color": MAP_EDGE_DIM, "stroke_width": 2.0},
            {"color": MAP_EDGE_DIM, "stroke_width": 3.0},
            {"color": MAP_EDGE_DIM, "stroke_width": 2.6},
            {"color": MAP_EDGE_DIM, "stroke_width": 2.2},
        ],
        text_style=[{"color": MAP_TXT, "font_size": 30}] * 4,
    )


def build_knowledge_map(fit_h=6.4, fit_w=15.2, y_shift=0.34):
    """构建知识地图；返回 (MindMap, key2id, id2node)"""
    from manim_mindmap import MindMap
    data, key2id = knowledge_map_data()
    mm = MindMap(data, buff=0.16, level_spacing=1.35, node_spacing=0.52,
                 node_style=_map_node_style())
    if mm.height > fit_h:
        mm.scale_to_fit_height(fit_h)
    if mm.width > fit_w:
        mm.scale_to_fit_width(fit_w)
    mm.move_to([0, y_shift, 0])
    id2node = dict(mm.node_data_dict)   # ID -> NodeMobject(vmobject, surr_rect, connector, text)

    # ★ 关键：重排绘制顺序为「方框 → 连线 → 文字」。
    #   插件默认的顺序是每个节点 [文字, 方框, 连线]，方框排在文字后面；
    #   方框一旦有填充色就会把文字整块盖住（表现为「一排空框」）。
    boxes, conns, texts = Group(), Group(), Group()
    for nd in id2node.values():
        texts.add(nd.vmobject)
        boxes.add(nd.surr_rect)
        if nd.connector is not None:
            conns.add(nd.connector)
    mm.remove(*list(mm.submobjects))
    mm.add(boxes, conns, texts)
    return mm, key2id, id2node


def base_box_color(nid):
    """按层级取底色"""
    lv = len(nid)
    return MAP_BOX_ROOT if lv == 1 else (MAP_BOX_L2 if lv == 2 else MAP_BOX_L3)


def build_mini_map(data, fit_h=4.7, fit_w=12.6, y=0.15,
                   level_spacing=1.15, node_spacing=0.48):
    """
    ★ 下集新增：每道大题开讲前的「思路导图」（小而快，不是全片大地图）。
    data 结构与 knowledge_map_data() 相同：{'node': VMobject, 'child': [...]}
    返回 (MindMap, id2node)；生长顺序 = sorted(ID)（元组字典序恰好就是 DFS 先序）。
    同样做了「方框 → 连线 → 文字」图层重排（上集踩过的坑）。
    """
    from manim_mindmap import MindMap
    mm = MindMap(data, buff=0.18, level_spacing=level_spacing,
                 node_spacing=node_spacing, node_style=_map_node_style())
    if mm.height > fit_h:
        mm.scale_to_fit_height(fit_h)
    if mm.width > fit_w:
        mm.scale_to_fit_width(fit_w)
    mm.move_to([0, y, 0])
    id2node = dict(mm.node_data_dict)
    boxes, conns, texts = Group(), Group(), Group()
    for nd in id2node.values():
        texts.add(nd.vmobject)
        boxes.add(nd.surr_rect)
        if nd.connector is not None:
            conns.add(nd.connector)
    mm.remove(*list(mm.submobjects))
    mm.add(boxes, conns, texts)
    return mm, id2node


def paint_map(id2node, lit_ids=(), todo_ids=()):
    """
    直接设置整张地图的配色 —— 不走 .animate。
    原因：对插件 Group 的内部对象做 animate，会让 surr_rect 与文字不同步
    （曾出现「空框 + 文字错位」的严重事故）。这里直接改属性，稳定可靠。
    """
    lit_ids, todo_ids = set(lit_ids), set(todo_ids)
    for nid, nd in id2node.items():
        if nid in lit_ids:
            nd.vmobject.set_color(MAP_TXT_LIT)
            nd.surr_rect.set_fill(base_box_color(nid), 1).set_stroke(MAP_EDGE_LIT, 3.2)
        elif nid in todo_ids:
            nd.vmobject.set_color(MAP_TXT_TODO)
            nd.surr_rect.set_fill(MAP_BOX_TODO, 1).set_stroke(MAP_EDGE_TODO, 1.8)
        else:
            nd.vmobject.set_color(MAP_TXT_DIM)
            nd.surr_rect.set_fill(base_box_color(nid), 1).set_stroke(MAP_EDGE_DIM, 2.2)


def lit_ids_upto(key, key2id):
    """累积点亮：讲到 key 时，之前所有节点都保持亮"""
    if key == "root":
        return [(0,)]
    ids = [(0,)]
    for k in MAP_LIT_ORDER:
        ids.append(key2id[k])
        if k == "trio":
            ids += [key2id["ker"], key2id["im"], key2id["eig"]]
        if k == key:
            break
    return ids


# ================= 场景基类 =================
class BaseScene(Scene):
    """统一：网格背景 + cur 登记 + 白场转场 + 字幕管理"""

    # ★ 时长校准系数：只拉长"停留时间"，动画本身的节奏（run_time）不变。
    #   配音定稿后改这一个数字就能把画面时长对上，不必动任何场景代码。
    PACE = 1.0

    def wait(self, duration=1.0, **kwargs):
        return super().wait(duration * self.PACE, **kwargs)

    def make_bg(self):
        return make_grid()

    def begin(self):
        self.bg_grid = make_grid()
        self.add(self.bg_grid)
        self.cur = []
        self.sub_mob = None

    def reg(self, *mobs):
        self.cur.extend([m for m in mobs if m is not None])

    def wipe(self, t_out=0.26):
        """
        白场转场：清掉「除背景网格外的一切」。
        ★ 不再依赖 self.cur 登记表 —— 只要漏登记一个元素，它就会变成残影飘到下一页
          （实测吃过两次：上一页的 note_box / hilite 底框飘到地图页和推论页上，正压着文字）。
        做法：先把 self.mobjects 去重，再排除「是别人子孙」的对象（交给祖先统一淡出），
        避免对同一对象重复 FadeOut。（CE 0.21 没有 Mobject.parents，故用 get_family 反推。）
        """
        keep = getattr(self, "bg_grid", None)
        cand, seen = [], set()
        for m in self.mobjects:
            if m is keep or id(m) in seen:
                continue
            seen.add(id(m))
            cand.append(m)
        inner = set()
        for m in cand:
            for sub in m.get_family()[1:]:
                inner.add(id(sub))
        drops = [m for m in cand if id(m) not in inner]
        if drops:
            self.play(*[FadeOut(m) for m in drops], run_time=t_out)
        self.cur = []
        self.sub_mob = None

    def hard_clear(self, t=0.24):
        """同 wipe()，保留此名以便地图页语义清晰（干净背景板）"""
        self.wipe(t_out=t)

    def grow_map(self, i2n, node_rt=0.6, lag=1.0, order=None):
        """
        ★ 知识地图「逐节点生长」——一个节点一个节点地出现，不是一口气铺上。
        每个节点 = 文字淡入 + 方框淡入（+ 连线从左到右画出来）。
        node_rt：单个节点的动画时长；总时长 ≈ node_rt * (1 + lag*(节点数-1))。
        默认 lag=1.0 → 节点正好首尾相接、不重叠，最像"一笔一笔画出来"。

        注意：连线自带 updater（每帧 become 完整形状），会把 Create 的绘制进度盖掉，
        所以生长前先 clear_updaters()。
        """
        order = order or MAP_DFS_ORDER
        for nd in i2n.values():
            if nd.connector is not None:
                nd.connector.clear_updaters()
        anims = []
        for nid in order:
            nd = i2n[nid]
            # ★ 顺序即图层：先方框 → 再连线 → 最后文字。
            #   这里是逐个 FadeIn 到场景里，加入顺序 = 绘制顺序；
            #   若把方框放在文字之后，方框会把文字整块盖住（表现为「一排骨牌空框」）。
            parts = [FadeIn(nd.surr_rect, run_time=node_rt)]
            if nd.connector is not None:
                parts.append(Create(nd.connector, run_time=node_rt))
            parts.append(FadeIn(nd.vmobject, run_time=node_rt))
            anims.append(AnimationGroup(*parts, run_time=node_rt))
        self.play(LaggedStart(*anims, lag_ratio=lag))

    def sub_in(self, text, run_time=0.28):
        """
        text 三种写法：
          1) 纯汉字字符串 → 宋体白字
          2) [('t', 汉字), ('m', latex), ...] 清单 → 内部 VGroup 封装（★推荐，公式走 MathTex 斜体）
          3) 已建好的 Mobject
        """
        if getattr(self, "sub_mob", None) is not None:
            self.play(FadeOut(self.sub_mob), run_time=0.16)
            if self.sub_mob in self.cur:
                self.cur.remove(self.sub_mob)
        if isinstance(text, str):
            s = sub_bar(text)
        elif isinstance(text, (list, tuple)) and text and isinstance(text[0], (list, tuple)):
            s = sub_bar(subs(*text))
        else:
            s = sub_bar(text)
        self.play(FadeIn(s, shift=UP * 0.12), run_time=run_time)
        self.reg(s)
        self.sub_mob = s
        return s

    def head(self, text, color=BLUE):
        """章节标题栏。text 可传纯中文串，或 mixlabel(...) 生成的「汉字+公式」VGroup。"""
        bar = title_bar(text, color=color)
        self.play(Write(bar), run_time=0.8)
        self.reg(bar)
        return bar

    def show_rows(self, rows, rt=0.85, lag=0.0):
        """逐行淡入一组内容"""
        for r in rows:
            self.play(Write(r), run_time=rt)
            self.reg(r)


