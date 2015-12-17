# Squawka scraper

Scrapy crawler to get Opta football match reports from [Squawka](http://www.squawka.com). 
Match reports are saved as XML-files (Squawka's own format) containing all rendered Detailed Match Stats, such as _goal attempts_ (location, player, result, etc.) and general match info.

The scraper crawls Squawka for game IDs and uses those to download XML match reports from Squawka's S3 bucket. 
For example, [this match page](http://world-cup-2014.squawka.com/spain-vs-netherlands/13-06-2014/world-cup/matches) is generated using [this XML file](http://s3-irl-world-cup.squawka.com/dp/ingame/7247).


## Requirements
* Python 2.7
* [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)


## Usage

1. Clone repo

2. Install packages:
```sh
cd squawka-scraper/
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run scraper:


- from the command line:

```bash
cd crawlers/
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


### Utilities

Class `SquawkaReport` in `squawka.utils` is an interface for the XML-files (see the code for all properties).
In `IPython`:

```python
In [1]: from squawka.utils import SquawkaReport
In [2]: report = SquawkaReport('data/world-cup_7247.xml')
In [3]: goals_attempts = pd.DataFrame(report.goals_attempts)
In [4]: goals_attempts[goals_attempts['type'] == 'goal']
Out[4]:
   action_type assist_1 coordinates        end headed injurytime_play middle  \
5       Attack      NaN        None    88.5,50    NaN             NaN    NaN
7       Attack     7674        None  84.8,50.9   true               0    NaN
10      Attack     7674        None  89.4,47.8    NaN             NaN    NaN
12      Attack      NaN        None    99,45.2    NaN             NaN    NaN
17      Attack      NaN        None  89.6,45.6    NaN             NaN    NaN
18      Attack      186        None  91.2,54.2    NaN             NaN    NaN

   mins minsec                                          passlinks player_id  \
5    26   1597  [{"type":"completed_pass","sub_type":"","swere...       301
7    43   2605  [{"type":"failed_pass","sub_type":"","swere":"...       195
10   52   3122  [{"type":"interceptions","end_x":65.7,"end_y":...       189
12   63   3834  [{"type":"completed_pass","sub_type":"","swere...      7828
17   71   4310  [{"type":"take-on-fail","sub_type":"","start_x...       195
18   79   4772  [{"type":"take-on-fail","sub_type":"","start_x...       189

   secs  shot      start swere team_id  type         uid
5    37  true   53.4,2.5   NaN      28  goal  1134620981
7    25   NaN  46.5,20.3   NaN      19  goal   742916879
10    2  true  50.0,13.9   NaN      19  goal  1228414874
12   54  true   48.5,3.8   NaN      19  goal   263418566
17   50  true   48.4,0.6   NaN      19  goal  1306339755
18   32  true  46.6,22.8   NaN      19  goal  1276756239
```
