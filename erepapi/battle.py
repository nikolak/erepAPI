# Copyright (c) 2013 Nikola Kovacevic   <nikolak@outlook.com>,

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# SOFTWARE
import api
from time import strftime, localtime


class Battle(object):
    """docstring for Battle"""

    def __init__(self, battleID):
        super(Battle, self).__init__()
        self.id = str(battleID)
        self.__resource = "battle"
        self.__action = "index"
        self.__params = "battleId=" + self.id
        if not self.id.isdigit():
            raise ValueError(self.id)
        else:
            self.__url = api._construct_url(self.__resource, self.__action, self.__params)
            self.__headers = api._construct_headers(self.__url)
        self.data = api._load(self.__url, self.__headers)

        self.is_resistance = self.data["battle"]["is_resistance"] == "true"

        # Region
        self.region_id = int(self.data["battle"]["region"]["id"])
        self.region_name = self.data["battle"]["region"]["name"]

        # Progress
        self.start = self._format_time(self.data["battle"]["progress"]["started-at"])
        self.end = self._format_time(self.data["battle"]["progress"]["finished-at"])
        self.finish_reason = self.data["battle"]["progress"]["finished-reason"]

        # Defenders
        self.defender_id = int(self.data["battle"]["progress"]["countries"]["victim_country"]["id"])
        self.defender_initials = self.data["battle"]["progress"]["countries"]["victim_country"]["initials"]
        self.defender_allies = {}
        for item in self.data["battle"]["progress"]["countries"]["victim_country"]["allies"]:
            country_name = item["country"]["name"]
            country_id = int(item["country"]["allied_country_id"])
            country_initials = item["country"]["initials"]
            self.defender_allies[country_name] = {"id": country_id,
                                                  "initials": country_initials
            }

        # Invaders
        self.attacker_id = int(self.data["battle"]["progress"]["countries"]["invader_country"]["id"])
        self.attacker_initials = self.data["battle"]["progress"]["countries"]["invader_country"]["initials"]
        self.attacker_allies = {}
        for item in self.data["battle"]["progress"]["countries"]["invader_country"]["allies"]:
            country_name = item["country"]["name"]
            country_id = int(item["country"]["allied_country_id"])
            country_initials = item["country"]["initials"]
            self.attacker_allies[country_name] = {"id": country_id,
                                                  "initials": country_initials
            }

    def _format_time(self, api_time):
        if api_time.isdigit() is False:
            return None
        else:
            return strftime('%Y-%m-%d %H:%M:%S', localtime(int(api_time)))
