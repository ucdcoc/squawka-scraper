# Squawka scraper

Scrapy crawler to get match reports from [Squawka](http://www.squawka.com). Match reports are saved as XML-files (Squawka's own format) containing all rendered Detailed Match Stats, such as _goal attempts_ (location, player, result, etc.) and general match info.

The scraper crawls Squawka for game IDs and uses those to download XML match reports from Squawka's S3 bucket. As an example, [this match page](http://world-cup-2014.squawka.com/spain-vs-netherlands/13-06-2014/world-cup/matches) is generated using [this XML file](http://s3-irl-world-cup.squawka.com/dp/ingame_rdp/7247).


## Requirements
* Python 2.7
* Scrapy (tested with version 1.0.3)


## Usage
1. Clone repo

2. Run scraper:


- from the command line:

```bash
scrapy crawl squawka -a competition_id=9 -a season=2014
```

- in a Python script:

```python
from crawlers.spiders.squawka import SquawkaSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(SquawkaSpider, competition_id=9, season=2014)
process.start()
```

XML-files are saved to folder `data/`. Log is written to `squawka.log` (see `crawlers/settings.py`). More info can be found in the [Scrapy documentation](http://doc.scrapy.org/en/1.0/). Please be nice to Squawka and don't decrease the limits too much.

Note: scraper may not all work for all competition ID's. Scraper will scrape matches from other competitions/years if found (e.g. start page EPL is always scraped).


### Squawka competition ID's:
* 4: World Cup
* 5: Champions League
* 6: Europa League
* 8: English Barclays Premier League
* 9: Dutch Eredivisie
* 10: Football League Championship
* 21: Italian Serie A
* 22: German Bundesliga
* 23: Spanish La Liga
* 24: French Ligue 1
* 98: US Major League Soccer
* 114: Turkish Super Lig
* 129: Russian Premier League
* 199: Mexican Liga MX - Apertura
* 214: Australian A-League
* 363: Brazilian Serie A
* 385: Mexican Liga MX - Clausura
