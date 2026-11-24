[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/inifikry/news-image-24-makefun/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/inifikry/news-image-24-makefun/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# The World Today — 24 November 2026

A newspaper front page summing up the world's news of Tuesday, 24 November
2026, drawn purely with Pillow. Entry for the make.fun bounty
[news-image-20261124](https://make.fun/c/news-image-20261124)
($100, blind rounds, judged by an AI picture editor).

## Stories

- **Lead — Russian jets spark Korea alert.** Seoul scrambled fighter jets
  after Russian warplanes entered South Korea's air-defence zone on Tuesday
  morning; residents of Ulleung island were briefly told to take shelter.
- **Trump, Putin meet in Anchorage today.** High-stakes summit on the
  Ukraine war as the two leaders sit down face to face in Alaska.
- **Storms threaten holiday getaway.** Storms and airline glitches threaten
  a messy Thanksgiving week for travellers in the US.
- **24 confirmed dead in factory fire.** Families await DNA tests after the
  Cikande candy plant blaze in Indonesia; dozens still missing.
- **Also today:** UN chief calls for AI risk rules within a year; Nepal's PM
  in Delhi for energy and trade talks; Ibaraki holds its first
  nuclear-waste survey briefing; Thai court upholds its verdict for an
  opposition MP.

## How it works

`draw_frontpage.py` draws `entry.png` (1024x1024 PNG) with Pillow — no
network, no AI-generated text. `main.py` (Python 3.13, standard library
only) copies `entry.png` to `/output/entry.png`; running it twice writes
byte-identical output.
