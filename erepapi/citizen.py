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


class Citizen(object):
    """Contains all citizen variables
        requires valid citizen ID as initial parameter
    """

    def __init__(self, citizenID):
        """
        :param citizenID: String or Integer of citizen ID
        """
        super(Citizen, self).__init__()
        self.id = str(citizenID)
        self.__resource = "citizen"
        self.__action = "profile"
        self.__params = "citizenId=" + self.id
        self.profile_url = "http://www.erepublik.com/en/citizen/profile/" + self.id

        if not self.id.isdigit():
            raise ValueError
        else:
            self.__url = api._construct_url(self.__resource,
                                            self.__action,
                                            self.__params)
            self.__headers = api._construct_headers(self.__url)
        self.data = api._load(self.__url, self.__headers)

        # General attributes
        self.name = self.data["general"]["name"]
        if self.name is None:
            raise ValueError
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
        self.citizenship_country_id = \
            int(self.data["location"]["citizenship_country_id"])
        self.citizenship_country_name = \
            self.data["location"]["citizenship_country_id"]
        self.citizenship_country_initials = \
            self.data["location"]["citizenship_country_initials"]
        self.citizenship_region_id = \
            int(self.data["location"]["citizenship_region_id"])
        self.citizenship_region_name = \
            self.data["location"]["citizenship_region_name"]
        self.residence_country_id = \
            int(self.data["location"]["residence_country_id"])
        self.residence_country_name = \
            self.data["location"]["residence_country_name"]
        self.residence_country_initials = \
            self.data["location"]["residence_country_initials"]
        self.residence_region_id = \
            int(self.data["location"]["residence_region_id"])
        self.residence_region_name = \
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
            'World Class*': 55,
            'World Class**': 56,
            'World Class***': 57,
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
