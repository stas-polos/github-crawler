## GitHub Crawler

1. [Installation](#installation)
2. [Configuration](#configuration)
4. [CLI](#cli)


### Installation
Clone the repository
```bash
git clone https://github.com/stas-polos/github-crawler.git
```

Change into the project directory
```bash
cd github-crawler
```

### Configuration

Copy the appropriate file and rename it, removing the name ".dist"
```bash
cd .dist.env .env
```

Set configuration options to `.env`
* Settings for docker image
  * PYTHON_IMAGE_VERSION - version of python image (default: 3.11.6-slim-bullseye)
* Settings for logging
  * LOG_LEVEL - level of logging

### CLI

For build image, run command:
```bash
docker compose build github-crawler
```

For run crawler need run command:
```bash
docker compose run --rm github-crawler python /app/src/cli.py searcher crawl \
  --keywords keyword1 \
  --keywords keyword2 \
  --proxies 194.126.37.94:8080 \
  --proxies 13.78.125.167:8080 \
  --search-type repositories
```
Expected result:
```bash
2024-07-11 00:00:00 [searcher] INFO: Input task: {
  "keywords": [
    "keyword1",
    "keyword2"
  ],
  "proxies": [
    "91.225.201.57:9901"
  ],
  "type": "repositories"
}
2024-07-11 00:00:00 [searcher] INFO: Formatted url: https://github.com/search?q=keyword1+OR+keyword2&type=repositories
2024-07-11 00:00:00 [searcher] INFO: Search results: [
  {
    "url": "https://github.com/clarkbynum/a-ORIG",
    "extra": {
      "owner": "clarkbynum",
      "language_stats": {
        "JavaScript": 99.1,
        "Shell": 0.9
      }
    }
  },
  {
    "url": "https://github.com/wecacuee/keyword2cmdline",
    "extra": {
      "owner": "wecacuee",
      "language_stats": {
        "Python": 100.0
      }
    }
  },
  {
    "url": "https://github.com/bearmi/mgrep",
    "extra": {
      "owner": "bearmi",
      "language_stats": {
        "C": 100.0
      }
    }
  },
  {
    "url": "https://github.com/zhangnn520/keyword2textgenration",
    "extra": {
      "owner": "zhangnn520",
      "language_stats": {
        "Jupyter Notebook": 76.3,
        "Python": 23.4,
        "Shell": 0.3
      }
    }
  },
  {
    "url": "https://github.com/gh-silent/Keyword1",
    "extra": {
      "owner": "gh-silent",
      "language_stats": null
    }
  },
  {
    "url": "https://github.com/ucon19/keyword2024",
    "extra": {
      "owner": "ucon19",
      "language_stats": null
    }
  },
  {
    "url": "https://github.com/AzzaSalahEldin/KEYWORD1",
    "extra": {
      "owner": "AzzaSalahEldin",
      "language_stats": {
        "Groovy": 100.0
      }
    }
  },
  {
    "url": "https://github.com/UjjwalaChaudhari/keyword1",
    "extra": {
      "owner": "UjjwalaChaudhari",
      "language_stats": {
        "HTML": 51.3,
        "Java": 35.5,
        "CSS": 8.0,
        "JavaScript": 5.2
      }
    }
  },
  {
    "url": "https://github.com/anantj-optimus/keyword1",
    "extra": {
      "owner": "anantj-optimus",
      "language_stats": null
    }
  },
  {
    "url": "https://github.com/namechk1/keyword1",
    "extra": {
      "owner": "namechk1",
      "language_stats": null
    }
  }
]
```
