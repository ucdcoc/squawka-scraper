import pandas as pd
import re
from lxml import etree


class SquawkaReport:

    def __init__(self, path):
        self.__time_slice_events = [
            'action_areas',
            'all_passes',
            'balls_out',
            'blocked_events',
            'cards',
            'clearances',
            'competition',
            'corners',
            'crosses',
            'extra_heat_maps',
            'fouls',
            'goal_keeping',
            'goals_attempts',
            'headed_duals',
            'interceptions',
            'keepersweeper',
            'kickoff',
            'match_id',
            'offside',
            'oneonones',
            'setpieces',
            'tackles',
            'takeons',
        ]
        self.path = path
        self.xml = self.read_xml(path)

    # See: https://stackoverflow.com/questions/10967551/
    # how-do-i-dynamically-create-properties-in-python
    def __getattr__(self, name):
        if name in self.__time_slice_events:
            return self._parse_timeslice(name)
        else:
            msg = "'{0}' object has no attribute '{1}'"
            raise AttributeError(msg.format(type(self).__name__, name))

    @staticmethod
    def read_xml(path):
        with open(path, 'r') as f:
            data = f.read()
        xml = etree.fromstring(data)
        return xml

    def _parse_timeslice(self, filter_type):
        xpath = '/squawka/data_panel/filters/{filter_type}/time_slice/event'
        return self._get_elements(xpath.format(filter_type=filter_type))

    def _get_elements(self, xpath):
        elements = self.xml.xpath(xpath)
        if elements:
            return self._parse_elements(elements)
        else:
            return None

    def _parse_elements(self, elements):
        parsed = [dict({c.tag: c.text for c in
                        e.getchildren()}.items() + e.attrib.items())
                  for e in elements]
        return parsed

    @property
    def competition(self):
        return re.findall("/(.*)_\d*.xml", self.p)[0]

    @property
    def filters(self):
        filters_element = self.xml.xpath('/squawka/data_panel/filters')
        if filters_element:
            return [ch.tag for ch in filters_element[0].getchildren()]
        # Some match reports don't have data.
        else:
            return None

    @property
    def kickoff(self):
        date = self.xml.xpath("/squawka/data_panel/game/kickoff/text()")[0]
        return pd.to_datetime(date)

    @property
    def match_id(self):
        return int(re.findall("/.*_(\d+).xml", self.path)[0])

    @property
    def name(self):
        return self.xml.xpath("/squawka/data_panel/game/name/text()")[0]

    @property
    def players(self):
        xpath = '/squawka/data_panel/players/player'
        return self._get_elements(xpath)

    @property
    def teams(self):
        xpath = '/squawka/data_panel/game/team'
        return self._get_elements(xpath)

    @property
    def venue(self):
        return self.xml.xpath("/squawka/data_panel/game/venue/text()")[0]
