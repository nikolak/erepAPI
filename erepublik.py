# Copyright (c) 2013 Nikola Kovacevic   <nikolak@outlook.com>,
#                                        <nikola.kovacevic91@gmail.com>

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

import urllib2
import json
from hashlib import sha256
from datetime import datetime
import hmac
import binascii

api_url = "http://api.erepublik.com/"
public_key = "public_key"
private_key = "private_key"


def _date_header(utc):
    """Return a string representation of a date according to RFC 1123
    (HTTP/1.1).

    The supplied date must be in UTC.

    """
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][utc.weekday()]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
             "Oct", "Nov", "Dec"][utc.month - 1]
    return "%s, %02d %s %04d %02d:%02d:%02d" % (weekday, utc.day, month,
                                                utc.year, utc.hour, utc.minute,
                                                utc.second)


def _construct_url(resource, action, params=None):
    """
    Constructs rest of API url based on resource, action and parameters.

    Multiple parameters must be a list.

    Single parameters must be a single string
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


def _digest(string):
    """
    Generate hash value using HMAC method and sha256

    Requires private access key
    """
    hashed = hmac.new(private_key, string, sha256)
    return hashed.hexdigest()


def _construct_headers(url):
    header = {"Auth": public_key + '/'}
    date = _date_header(datetime.utcnow())
    header["Date"] = date
    to_digest = url.replace('/', ':').replace('?', ':') + ':'
    to_digest = to_digest.lower()
    to_digest += date
    header["Auth"] += _digest(to_digest)
    return header


def _load(url, headers):
    # print url
    req = urllib2.Request(api_url + url)
    req.add_header("Date", headers["Date"])
    req.add_header("Auth", headers["Auth"])
    response = urllib2.urlopen(req)
    content = response.read()
    # print content
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

    """docstring for Citizen"""
    def __init__(self, citizenID):
        super(Citizen, self).__init__()
        self.id = citizenID
        self.resource = "citizen"
        self.action = "profile"
        self.params = "citizenId=" + self.id
        self.base_citizen_url = "http://www.erepublik.com/en/citizen/profile/"

        if not self.id.isdigit():
            raise invalidID
        else:
            self.url = _construct_url(self.resource, self.action, self.params)
            self.headers = _construct_headers(self.url)
        self.data = _load(self.url, self.headers)
        # print self.data

        # General attributes
        self.name = self.data["general"]["name"]
        self.is_alive = self.data["general"]["is_alive"]
        self.has_avatar = self.data["general"]["has_avatar"]
        self.avatar = self.data["general"]["avatar"]
        self.experience_points = self.data["general"]["experience_points"]
        self.level = self.data["general"]["level"]
        self.birthDay = self.data["general"]["birthDay"]
        self.national_rank = self.data["general"]["nationalRank"]
        self.profile_url = self.base_citizen_url + self.id

        # Military attributes
        self.strength = self.data["militaryAttributes"]["strength"]
        self.rank_points = self.data["militaryAttributes"]["rank_points"]
        self.rank_name = self.data["militaryAttributes"]["rank_name"]
        self.rank_stars = self.data["militaryAttributes"]["rank_stars"]
        self.rank_icon = self.data["militaryAttributes"]["rank_icon"]

        # Achievements - dict
        if self.data["achievements"]:
            self.achievements = self.__parse_achievements()
        else:
            self.achievements = None

        # Location
        self.citizenship_country_id =\
            self.data["location"]["citizenship_country_id"]
        self.citizenship_country_name =\
            self.data["location"]["citizenship_country_id"]
        self.citizenship_country_initials =\
            self.data["location"]["citizenship_country_initials"]
        self.citizenship_region_id =\
            self.data["location"]["citizenship_region_id"]
        self.citizenship_region_name =\
            self.data["location"]["citizenship_region_name"]
        self.residence_country_id =\
            self.data["location"]["residence_country_id"]
        self.residence_country_name =\
            self.data["location"]["residence_country_name"]
        self.residence_country_initials =\
            self.data["location"]["residence_country_initials"]
        self.residence_region_id =\
            self.data["location"]["residence_region_id"]
        self.residence_region_name =\
            self.data["location"]["residence_region_name"]

        # Party info
        if self.data["party"]:
            self.party_member = True
            self.party_id = self.data["party"]["id"]
            self.party_name = self.data["party"]["name"]
            if self.data["party"]["is_president"] == "1":
                self.is_president = True
            else:
                self.is_president = False
        else:
            self.party_member = False

        # Military unit
        if self.data["militaryUnit"]:
            self.in_unit = True
            self.unit_id = self.data["militaryUnit"]["id"]
            self.unit_name = self.data["militaryUnit"]["name"]
            self.unit_leader = self.data["militaryUnit"]["is_leader"]
        else:
            self.in_unit = False

        # Newspappers

        if self.data["newspaper"]:
            self.owns_newspaper = True
            self.newspaper_id = self.data["newspaper"]["id"]
            self.newspaper_name = self.data["newspaper"]["name"]
        else:
            self.owns_newspaper = False

    def __parse_achievements(self):
        """
        Returns a single string with list of all medals/achievements and
        total number of them from selected citizen
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


class Country_regions(object):

    """Contains regions of country as dictionary.
      Requires country ID as initial argument

    self.regions={ "region_name":{
                                    "id":
                                    "owner_id":
                                    "original_owner_id":
                                    "url":
                                }

                }
    """
    def __init__(self, countryID):
        super(Country, self).__init__()
        self.id = countryID
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
                "id": region["id"],
                "owner_id": region["current_owner_country_id"],
                "original_owner_id": region["original_owner_country_id"],
                "url": self.base_url + region["permalink"]}


class Countries(object):

    """Contains list of countries
        Use `by_id(country_id)` to get basic info about country as dict
            {
               "id":"",
               "name":"",
               "initials":"",
               "color":"",
               "continent_id":"",
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
            if item["id"] == id:
                country_data = item
                break
        return country_data

    def by_name(self, name):
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
    def __init__(self, regionID, page="1"):
        super(Region, self).__init__()
        self.id = regionID
        self.page = page
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
            self.citizenIDs = self.data["citizens"]
