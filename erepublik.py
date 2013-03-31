# Copyright (c) 2013 Nikola Kovacevic   <nikolak@outlook.com>,
#                                       <nikola.kovacevic91@gmail.com>

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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

import hmac
import json
import urllib2
from hashlib import sha256
from time import strftime, gmtime, localtime


api_url = "http://api.erepublik.com/"
public_key = "public_key"
private_key = "private_key"


def _construct_url(resource, action, params=None):
    """
    Constructs rest of API url based on resource, action and parameters.

    Multiple parameters must be a list.

    Single parameters must be a single string

    Internal usage
    """
    final_url = '{}/{}'.format(resource, action)
    if type(params) == list:
        final_url += '?'
        for i in xrange(len(params)):
            if i < len(params) - 1:
                final_url += params[i] + '&'
            else:
                final_url += params[i]
    elif type(params) == str:
        final_url += '?{}'.format(params)
    else:
        pass
    return final_url


def _construct_headers(url):
    """
    Constructs headers to send with request.
    Internal usage.

    The Date header needs to be the current date and
    time of the request in RFC1123 format (e.g. Tue, 04 Sep 2012 15:57:48)

    The Auth header structure is {public_key}/{digest} where {public_key}
    is your public key provided by eRepublik and {digest}
    is a hash that represents an encrypted value of a concatenated string
    formed from {resource}, {action}, {params} (if they exist),
    and {date} (the same value Date header has).
    """
    header = {"Auth": public_key + '/'}
    date = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    header["Date"] = date
    to_digest = (url.replace('/', ':').replace('?', ':') + ':').lower()
    to_digest += date
    header["Auth"] += hmac.new(private_key, to_digest, sha256).hexdigest()
    return header


def _load(url, headers):
    """
    Returns json/dictionary of data in "message" from API response
    """
    req = urllib2.Request(api_url + url)
    req.add_header("Date", headers["Date"])
    req.add_header("Auth", headers["Auth"])
    response = urllib2.urlopen(req)
    content = response.read()
    data = json.loads(content)
    try:
        if data["code"] != 200:
            raise invalidCode
        else:
            return data["message"]
    except:
        raise urlParseError


class invalidID(Exception):
    pass


class invalidCode(Exception):
    pass


class urlParseError(Exception):
    pass


class Citizen(object):

    """Contains all citizen variables
        requires valid citizen ID as initial parameter
    """
    def __init__(self, citizenID):
        super(Citizen, self).__init__()
        self.id = str(citizenID)
        self.resource = "citizen"
        self.action = "profile"
        self.params = "citizenId=" + self.id
        self.profile_url = "http://www.erepublik.com/en/citizen/profile/" + self.id

        if not self.id.isdigit():
            raise invalidID
        else:
            self.url = _construct_url(self.resource, self.action, self.params)
            self.headers = _construct_headers(self.url)
        self.data = _load(self.url, self.headers)

        # General attributes
        self.name = self.data["general"]["name"]
        if self.name is None:
            raise invalidID
        self.is_alive = self.data["general"]["is_alive"] == "1"
        self.has_avatar = self.data["general"]["has_avatar"]
        self.avatar = self.data["general"]["avatar"]
        self.experience_points = int(self.data["general"]["experience_points"])
        self.level = int(self.data["general"]["level"])
        self.birthday = self.data["general"]["birthDay"]
        self.national_rank = self.data["general"]["nationalRank"]

        # Military attributes
        self.strength = float(self.data["militaryAttributes"]["strength"])
        self.rank_points = int(self.data["militaryAttributes"]["rank_points"])
        self.rank_name = self.data["militaryAttributes"]["rank_name"]
        self.rank_stars = self.data["militaryAttributes"]["rank_stars"]
        self.rank_icon = self.data["militaryAttributes"]["rank_icon"]
        self.rank_value = self.__return_rank_value()

        # Achievements - dict
        if self.data["achievements"]:
            self.achievements = self.__parse_achievements()
        else:
            self.achievements = {}

        # Location
        self.citizenship_country_id =\
            int(self.data["location"]["citizenship_country_id"])
        self.citizenship_country_name =\
            self.data["location"]["citizenship_country_id"]
        self.citizenship_country_initials =\
            self.data["location"]["citizenship_country_initials"]
        self.citizenship_region_id =\
            int(self.data["location"]["citizenship_region_id"])
        self.citizenship_region_name =\
            self.data["location"]["citizenship_region_name"]
        self.residence_country_id =\
            int(self.data["location"]["residence_country_id"])
        self.residence_country_name =\
            self.data["location"]["residence_country_name"]
        self.residence_country_initials =\
            self.data["location"]["residence_country_initials"]
        self.residence_region_id =\
            int(self.data["location"]["residence_region_id"])
        self.residence_region_name =\
            self.data["location"]["residence_region_name"]

        # Party info
        if self.data["party"]:
            self.party_member = True
            self.party_id = int(self.data["party"]["id"])
            self.party_name = self.data["party"]["name"]
            self.is_president = self.data["party"]["is_president"] == "1"
        else:
            self.party_member = False

        # Military unit
        if self.data["militaryUnit"]:
            self.in_unit = True
            self.unit_id = int(self.data["militaryUnit"]["id"])
            self.unit_name = self.data["militaryUnit"]["name"]
            self.unit_leader = self.data["militaryUnit"]["is_leader"]
        else:
            self.in_unit = False

        # Newspappers

        if self.data["newspaper"]:
            self.owns_newspaper = True
            self.newspaper_id = int(self.data["newspaper"]["id"])
            self.newspaper_name = self.data["newspaper"]["name"]
        else:
            self.owns_newspaper = False

    def __parse_achievements(self):
        """
        Returns a dictionary with all medals/achievements and
        total number of them from selected citizen

        {
            "achievement_name":quantaty_integer,
        }
        """
        total_count = 0
        parsed = {}
        for item in self.data["achievements"]:
            ach_type = self.data["achievements"][item]["type"].capitalize()
            ach_count = int(self.data["achievements"][item]["total"])
            parsed[ach_type] = ach_count
            total_count += ach_count
        parsed["Total"] = total_count
        return parsed

    def __return_rank_value(self):
        full_rank_name = self.rank_name + "*" * self.rank_stars
        rank_list = {
            'Recruit': 1,
            'Private': 2,
            'Private*': 3,
            'Private**': 4,
            'Private***': 5,
            'Corporal': 6,
            'Corporal*': 7,
            'Corporal**': 8,
            'Corporal***': 9,
            'Sergeant': 10,
            'Sergeant*': 11,
            'Sergeant**': 12,
            'Sergeant***': 13,
            'Lieutenant': 14,
            'Lieutenant*': 15,
            'Lieutenant**': 16,
            'Lieutenant***': 17,
            'Captain': 18,
            'Captain*': 19,
            'Captain**': 20,
            'Captain***': 21,
            'Major': 22,
            'Major*': 23,
            'Major**': 24,
            'Major***': 25,
            'Commander': 26,
            'Commander *': 27,
            'Commander **': 28,
            'Commander ***': 29,
            'Lt Colonel': 30,
            'Lt Colonel*': 31,
            'Lt Colonel**': 32,
            'Lt Colonel***': 33,
            'Colonel': 34,
            'Colonel*': 35,
            'Colonel**': 36,
            'Colonel***': 37,
            'General': 38,
            'General*': 39,
            'General**': 40,
            'General***': 41,
            'Field Marshal': 42,
            'Field Marshal*': 43,
            'Field Marshal**': 44,
            'Field Marshal***': 45,
            'Supreme Marshal': 46,
            'Supreme Marshal*': 47,
            'Supreme Marshal**': 48,
            'Supreme Marshal***': 49,
            'National Force': 50,
            'National Force*': 51,
            'National Force**': 52,
            'National Force***': 53,
            'World Class': 54,
            'World Class': 55,
            'World Class': 56,
            'World Class': 57,
            'Legendary Force': 58,
            'Legendary Force*': 59,
            'Legendary Force**': 60,
            'Legendary Force***': 61,
            'God of War': 62,
            'God of War*': 63,
            'God of War**': 64,
            'God of War***': 65,
        }
        return rank_list.get(full_rank_name, None)


class Country_regions(object):

    """Contains regions of country as dictionary.
      Requires country ID as initial argument

    self.regions={ "region_name":{
                                    "id":integer
                                    "owner_id":integer
                                    "original_owner_id":integer
                                    "url":string
                                }

                }
    """
    def __init__(self, countryID):
        super(Country_regions, self).__init__()
        self.id = str(countryID)
        self.resource = "country"
        self.action = "regions"
        self.params = "countryId=" + self.id

        if not self.id.isdigit():
            raise invalidID
        else:
            self.url = _construct_url(self.resource, self.action, self.params)
            self.headers = _construct_headers(self.url)
        self.data = _load(self.url, self.headers)
        self.base_url = "http://www.erepublik.com/en/main/region/"
        self.regions = {}
        for item in self.data["regions"]["region"]:
            region = self.data["regions"]["region"][item]
            self.regions[region["name"]] = {
                "id": int(region["id"]),
                "owner_id": int(region["current_owner_country_id"]),
                "original_owner_id": int(region["original_owner_country_id"]),
                "url": self.base_url + region["permalink"]}


class Countries(object):

    """Contains list of countries
        Use `by_id(country_id)` to get basic info about country as dict
            {
               "id":string,
               "name":string,
               "initials":string,
               "color":string,
               "continent_id":string,
               "continent_name":null,
               "capital_region_id":null/string,
               "capital_region_name":null/string
            },
    """
    def __init__(self):
        super(Countries, self).__init__()
        self.resource = "countries"
        self.action = "index"
        self.url = _construct_url(self.resource, self.action)
        self.headers = _construct_headers(self.url)
        self.data = _load(self.url, self.headers)
        self.all_countries = self.data["countries"]["country"]

    def by_id(self, id):
        """
        Returns Country info as dict
        Requires valid country ID
        """
        country_data = None
        for item in self.all_countries:
            if item["id"] == str(id):
                country_data = item
                break
        return country_data

    def by_name(self, name):
        """
        Returns Country info as dict
        Requires valid country name
        """
        country_data = None

        for item in self.all_countries:
            if item["name"].lower() == name.lower():
                country_data = item
                break
        return country_data


class Region(object):

    """
    Contains list of citizen IDs living in that region in self.citizenIDs
    Requires valid region ID as input and optional page number
    otherwise 1 is used for page num
    """
    def __init__(self, regionID, page=1):
        super(Region, self).__init__()
        self.id = str(regionID)
        self.page = str(page)
        self.resource = "region"
        self.action = "citizens"
        self.params = ["regionId=" + self.id, "page=" + self.page]

        if not self.id.isdigit():
            raise invalidID
        else:
            self.url = _construct_url(self.resource, self.action, self.params)
            self.headers = _construct_headers(self.url)
        self.data = _load(self.url, self.headers)
        if self.data["citizens"] is False:
            self.citizenIDs = None
        else:
            self.citizenIDs = [int(cit_id["citizen_id"]) for cit_id in self.data["citizens"]]


class Battle(object):

    """docstring for Battle"""
    def __init__(self, battleID):
        super(Battle, self).__init__()
        self.id = str(battleID)
        self.resource = "battle"
        self.action = "index"
        self.params = "battleId=" + self.id
        if not self.id.isdigit():
            raise invalidID
        else:
            self.url = _construct_url(self.resource, self.action, self.params)
            self.headers = _construct_headers(self.url)
        self.data = _load(self.url, self.headers)

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
        self.defender_alies = {}
        for item in self.data["battle"]["progress"]["countries"]["victim_country"]["allies"]:
                country_name = item["country"]["name"]
                country_id = int(item["country"]["allied_country_id"])
                country_initials = item["country"]["initials"]
                self.defender_alies[country_name] = {"id": country_id,
                                                     "initials": country_initials
                                                     }

        # Invaders
        self.defender_id = int(self.data["battle"]["progress"]["countries"]["invader_country"]["id"])
        self.defender_initials = self.data["battle"]["progress"]["countries"]["invader_country"]["initials"]
        self.defender_alies = {}
        for item in self.data["battle"]["progress"]["countries"]["invader_country"]["allies"]:
                country_name = item["country"]["name"]
                country_id = int(item["country"]["allied_country_id"])
                country_initials = item["country"]["initials"]
                self.defender_alies[country_name] = {"id": country_id,
                                                     "initials": country_initials
                                                     }

    def _format_time(self, api_time):
        if api_time.isdigit() is False:
            return None
        else:
            return strftime('%Y-%m-%d %H:%M:%S', localtime(int(api_time)))
