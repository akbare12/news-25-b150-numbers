# Wednesday 25 November 2026 — 50 Stories in One Image

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/akbare12/news-25-b150-numbers/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/akbare12/news-25-b150-numbers/reward.svg)](https://make.fun/bounty/news-image-20261125)

One 1024×1024 image summing up Wednesday 25 November 2026: **50 stories** —
3 heroes, 10 cards, 37 more in ALSO. Every story is dated 25 November 2026;
the footer DATE CHECK lists exactly the five near-miss stories left out.

## Heroes

1. **Trump tariffs hit 14 partners** — USTR proposes new duties after an
   8-month probe. China faces 20%, the highest, and up to 40% if the trade
   truce fails.
2. **Kospi −6.16% in chip rout** — Samsung −9.87%, Hynix −11.05% as tariff
   fears hit Seoul.
3. **Shenzhou-24 docks with first foreign astronaut** — liftoff 08:18
   Beijing, docking about 3.5 hours later. Pakistan's Ali, 40, joins the
   Tiangong crew.

## How to read it

- `C` = confirmed, `R` = reported, `CL` = claim — every card and ALSO item
  carries one.
- **DATE CHECK** (footer): all 50 stories are dated 25 Nov. Left out on
  purpose: Huawei verdict 24 Nov, PIF Tower strike 24 Nov, Sudan strikes
  24 Nov, Nvidia CEO reinstated 23 Nov, Hormuz mine claims 23-24 Nov.
- The map **WHERE IT HAPPENED** pins every hero and card story.

## Build

`gen.py` (Pillow, build time only) renders `entry.png`. `main.py` is
stdlib-only and copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

```sh
python3 gen.py   # renders entry.png (1024x1024, Pillow build-time only)
python3 main.py  # stdlib-only copy to $MAKEFUN_OUTPUT_DIR/entry.png
```
