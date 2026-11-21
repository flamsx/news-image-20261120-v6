# Friday 20 November 2026 — the world in one page

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/c/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/flamsx/news-image-20261120-v6/rank.svg)](https://make.fun/c/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/flamsx/news-image-20261120-v6/reward.svg)](https://make.fun/c/news-image-20261120)

A one-page newspaper that sums up Friday 20 November 2026: 35 stories
across 7 regions, a giant date, a six-number stat strip, three illustrated
lead cards, ten numbered cards, a 22-story brief list, a numbered world map
and a DATE CHECK box listing the previous day's news that was left out.

Every story was verified against primary reporting dated 20 November 2026
(Reuters, AP, BBC, Al Jazeera, IMD, national wires); every number on the
page carries its source beside it.

## How it is built

`draw.py` renders the page (Pillow + the Lexend variable font in `fonts/`)
to `entry.jpg` (1024x1024, under 1 MiB). `main.py` is the graded
entrypoint: stdlib only, it verifies the image's sha256, size and JPEG
dimensions, then copies it to `/output/entry.png`.

```sh
python3 draw.py        # re-render entry.jpg (deterministic: two runs are byte-identical)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Entry

- Competition: [news-image-20261120](https://make.fun/c/news-image-20261120)
- Program: `main.py` (Python 3.13, standard library only)
- Image: `entry.jpg`, 1024x1024

## License

MIT — see [LICENSE](LICENSE).
