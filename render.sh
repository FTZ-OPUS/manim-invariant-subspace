#!/bin/zsh
# 不变子空间动画 · 渲染脚本
# 所有中间产物都锁在本文件夹的 media/ 里，不在别处生成。
#
# 用法:
#   ./render.sh                  # 上集 低清预览 (480p15)
#   ./render.sh 2                # 下集 低清预览
#   ./render.sh h                # 上集 1080p60 -> 自动拷进 out/
#   ./render.sh h 2              # 下集 1080p60 -> 自动拷进 out/
#   ./render.sh n 5 60           # 只渲第 5~60 号动画（增量重渲，省时间）

set -e
MANIM=/Users/fengtianzhu/venvs/manim/bin/manim
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
mkdir -p out

part_name() {
  if [ "$1" = "2" ]; then echo "inv_part2.py Part2 下集"; else echo "inv_part1.py Part1 上集"; fi
}

run_hi() {
  local p="$1"
  local cls=$([ "$p" = "2" ] && echo "Part2" || echo "Part1")
  local src=$([ "$p" = "2" ] && echo "src/inv_part2.py" || echo "src/inv_part1.py")
  local outname=$([ "$p" = "2" ] && echo "不变子空间_下集_1080p60.mp4" || echo "不变子空间_上集_1080p60.mp4")
  "$MANIM" "$src" "$cls" -pqh --media_dir ./media
  cp "media/videos/${src##*/}/${cls}.mp4" "out/$outname" 2>/dev/null || \
  cp "media/videos/${src##*/}/1080p60/${cls}.mp4" "out/$outname"
  echo "✅ 成品 -> out/$outname"
}

case "${1:-1}" in
  h)
    run_hi "${2:-1}"
    ;;
  n)
    P="${4:-1}"
    SRC=$([ "$P" = "2" ] && echo "src/inv_part2.py" || echo "src/inv_part1.py")
    CLS=$([ "$P" = "2" ] && echo "Part2" || echo "Part1")
    "$MANIM" "$SRC" "$CLS" -ql --media_dir ./media -n "${2:-0},${3:-50}"
    echo "✅ 增量渲染完成（第 ${2:-0}~${3:-50} 号动画）"
    ;;
  2)
    "$MANIM" src/inv_part2.py Part2 -ql --media_dir ./media
    ;;
  *)
    "$MANIM" src/inv_part1.py Part1 -ql --media_dir ./media
    ;;
esac
