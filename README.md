[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![make.fun · rank](https://make.fun/badge/news-image-20261124/inifikry/news-image-24-makefun/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![make.fun · reward](https://make.fun/badge/news-image-20261124/inifikry/news-image-24-makefun/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# The World Today — Tuesday, 24 November 2026

A one-page newspaper front page that sums up 24 November 2026's world
news in a single 1024x1024 image, drawn entirely with Pillow (no AI
text, no network at runtime).

34 stories across 8 regions and 9 topics: 3 lead stories with drawn
illustrations, 12 picture cards, a world map with numbered pins, and a
19-item IN BRIEF list. A big-numbers strip, a coverage strip, a DATE
CHECK box (big stories left out because they happened on another day),
a WHAT WE DON'T KNOW YET box, and a HOW SURE legend round it out.

Every story is dated 24 November 2026 in its local time zone, with
named sources. See BUILD_REPORT.md for the full story list with date
evidence.

## Run

```
python3 draw_frontpage_v2.py   # draws entry.png
python3 main.py                # copies entry.png to /output/entry.png
```

`main.py` is deterministic: two runs produce byte-identical output.
