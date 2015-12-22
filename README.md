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

XML-files are saved to folder `data/`.
The log is written to `squawka.log` (see `crawlers/settings.py`).
More info can be found in the [Scrapy documentation](http://doc.scrapy.org/en/1.0/).
Please be nice to Squawka and don't decrease the limits too much.

Note: scraper may not all work for all competition ID's.
Scraper will scrape matches from other competitions/years if found (e.g. start page EPL is always scraped).


### Squawka competition ID's
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

(See `squawka.utils.COMPETITIONS`.)


### Utilities

Class `SquawkaReport` in `squawka.utils` is an interface for the XML-files (see the code and `utils.ALL_STATISTICS` for all properties).
In `IPython`:

```python
In [1]: import pandas as pd
In [2]: from squawka.utils import SquawkaReport
In [3]: report = SquawkaReport('data/world-cup_7247.xml')
In [4]: goals_attempts = pd.DataFrame(report.goals_attempts)
In [5]: goals_attempts[goals_attempts['type'] == 'goal']
Out[5]:
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

Alternatively, use `utils.stats_from_file` or `utils.stats_from_report`:
```python
In [1]: from squawka.utils import stats_from_file
In [2]: goals_attempts = stats_from_file('data/world-cup_7247.xml', 'goals_attempts')
```

To convert all XML-files in a folder to CSV use `utils.export_all_stats` (could take > 1 hour):
```python
In [1]: from squawka.utils import export_all_stats
In [2]: export_all_stats('data/', 'out/')
In [3]: ls out/
Out [3]:
action_areas.csv  blocked_events.csv  corners.csv          fouls.csv           headed_duals.csv   offside.csv    setpieces.csv  teams.csv
all_passes.csv    cards.csv           crosses.csv          goal_keeping.csv    interceptions.csv  oneonones.csv  tackles.csv
balls_out.csv     clearances.csv      extra_heat_maps.csv  goals_attempts.csv  keepersweeper.csv  players.csv    takeons.csv
In [4]:!head out/goals_attempts.csv
Out [4]:
action_type,assist_1,competition,coordinates,headed,injurytime_play,is_own,kickoff,match_id,mins,minsec,passlinks,player_id,secs,shot,swere,team_id,type,uid,end_x,end_y,middle_x,middle_y,start_x,start_y
Attack,,seriea,,False,,False,2014-05-18 19:45:00 +0100,4791,9,,,4069,36,True,right,114,save,,79.5,31.0,51,32.3,99.0,50.4
Attack,,seriea,,False,,False,2014-05-18 19:45:00 +0100,4791,8,,,2622,40,True,,114,save,,69.2,59.0,53.4,13.3,98.8,52.7
Attack,,seriea,,False,,False,2014-05-18 19:45:00 +0100,4791,14,,,2595,32,True,,114,blocked,,70.8,58.1,0,0,75.6,57.4
Attack,,seriea,,False,,False,2014-05-18 19:45:00 +0100,4791,11,,,3017,25,True,,127,blocked,,96.0,64.3,0,0,97.7,60.8
Attack,,seriea,,False,,False,2014-05-18 19:45:00 +0100,4791,11,,,3701,23,True,,127,blocked,,75.2,53.2,0,0,77.5,52.7
Attack,,seriea,,False,,False,2014-05-18 19:45:00 +0100,4791,15,,,2614,18,True,,114,blocked,,75.9,31.4,0,0,90.2,43.9
Attack,,seriea,,False,,False,2014-05-18 19:45:00 +0100,4791,23,,,2612,53,True,,114,save,,72.6,29.8,48.3,28.5,98.5,47.8
Attack,,seriea,,False,,False,2014-05-18 19:45:00 +0100,4791,28,,,2833,26,True,,127,save,,85.8,27.4,46.5,3.8,98.6,46.2
Attack,,seriea,,False,,False,2014-05-18 19:45:00 +0100,4791,32,,,2934,26,True,left,127,off_target,,72.5,49.7,,,59.9,36.1
```
