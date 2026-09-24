# 不变子空间 · Manim 动画讲解片（源码）

用 **Manim** 制作的线性代数科普动画：讲「不变子空间」。素材来自考研手写笔记，
全片分上下两集，风格为**米白纸面 + 浅网格 + 宋体定理片（若尔当标准型风格）+ 彩色格子矩阵 + 白场转场**。

| | 内容 | 时长 |
|---|---|---|
| **上集** `inv_part1.py` | 定义 → 定理 6.6.1（核 / 值域 / 特征子空间三兄弟）→ 命题 6.6.1（一维情形）→ 根子空间 → 例 6.6.1（范德蒙矩阵拆解） | 3:00 |
| **下集** `inv_part2.py` | 命题 6.6.2（可交换）→ 例 6.6.2（公共特征向量，双解法）→ 例 6.6.4（苏州大学真题：迹 + 范德蒙回归） | 3:10 |

成片规格：`1920×1080 · 60fps`。

> ⚠️ **要做同类片子，请先读 [`注意事项与踩坑记录.md`](./注意事项与踩坑记录.md)**
> —— 里面记着用户提出的全部修改要求（逐字写出、正文字体、VGroup 混排、抄题顺序……）
> 和所有踩过的技术坑。那份文档比源码更值得先看。

---

## 目录结构

```
.
├── README.md                    ← 本文件
├── 注意事项与踩坑记录.md          ← ★ 铁律 + 踩坑清单（先读这个）
├── render.sh                    ← 渲染脚本
└── src/
    ├── inv_lib.py               ← 组件库（字体 / 混排 / 抄题卡 / 罩子 / 火柴人 / 思维导图 / 场景基类）
    ├── inv_part1.py             ← 上集
    └── inv_part2.py             ← 下集
```

---

## 环境

| 项目 | 版本 / 位置 |
|---|---|
| Manim | **CE 0.21.0**（Python 3.12） |
| `manim-mindmap` | 0.1.3（思路导图 / 知识地图） |
| ffmpeg / ffprobe | 9.x |
| 中文字体 | **Songti SC**（标题 + 正文）· **Kaiti SC**（手写感批注） |

字体是 macOS 系统字体。在其它平台跑，需要把 `inv_lib.py` 顶部的
`SONG / KAI` 换成等价字体（Windows 可用 `SimSun` / `KaiTi`），并注意字重参数。

---

## 渲染

```bash
# 低清预览（480p15，排错用）
manim src/inv_part2.py Part2 -ql --media_dir ./media

# 1080p60 正式渲染（下集）；上集把 Part2 → Part1、inv_part2 → inv_part1
manim src/inv_part2.py Part2 -pqh --media_dir ./media

# 成品导出
cp media/videos/inv_part2/1080p60/Part2.mp4 "out/不变子空间_下集_1080p60.mp4"
```

或直接用脚本：

```bash
./render.sh          # 上集 低清预览
./render.sh 2        # 下集 低清预览
./render.sh h 2      # 下集 1080p60 → 自动拷进 out/
./render.sh n 5 60   # 只重渲第 5~60 号动画（增量，省时间）
```

**注意**：渲染务必带 `--media_dir ./media`，把中间产物锁在项目内，别散落到别处。
`media/` 与 `out/` 属于可清理的中间产物/成品，`src/` 才是要长期保留的源码。

---

## 代码要点

脚本顶部必须保留这两行（否则某些沙箱环境会在渲染中途因"批量删除保护"被中断）：

```python
config["no_latex_cleanup"] = True     # 不让 manim 反复删 .aux/.log/.dvi
config["max_files_cached"] = 1000000  # 拉高片段缓存上限
```

汉字与公式混排**必须用 VGroup 封装**，公式一律走 `MathTex`（LaTeX 斜体）：

```python
mixed(("t", " 的特征子空间都是 ", INK), ("m", r"B", INK), ("t", " 的不变子空间", INK),
      ts=32, ms=42)          # 正文行
mixlabel(("t", "看图："), ("m", r"\mathcal{B}"), ("t", " 摸不歪 A 的特征方向"))   # 标题
subs(("t", "缩进 "), ("m", r"V_\lambda"), ("t", " —— 罩外的世界不用看了"))       # 字幕
kaimix(("t", "捡回 "), ("m", r"V_\lambda"), ("t", " 里"))                      # 批注
```

文字/公式入场一律 `Write()`（逐字从左往右写出），只有图形类才用
`GrowFromCenter` / `GrowArrow` / `FadeIn(lag_ratio=…)`。

---

## 风格来源

- 骨架与视觉：Manim 宋体定理片（若尔当标准型风格）—— 米白纸面 + 浅网格 + 宋体加粗标题 +
  彩色圆角格子矩阵 + 白场转场。
- 公式排版：横屏大字公式规范 —— 16:9 / 每页 ≤4 行 / 中文与公式用 VGroup 混排 /
  `MathTex` 内严禁 `\text{中文}`。

---

## License

仅供学习交流使用。
