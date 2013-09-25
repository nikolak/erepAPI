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

class Country(object):

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
        super(Country, self).__init__()
        self.__resource = "countries"
        self.__action = "index"
        self.__url = api._construct_url(self.__resource, self.__action)
        self.__headers = api._construct_headers(self.__url)
        self.data = api._load(self.__url, self.__headers)
        self.__country_dict=self.data["countries"]["country"]
        self.all_countries = [item["name"] for item in self.__country_dict]

            #self.__construct_all_list(self.data["countries"]["country"])

        self.id=None
        self.name=None
        self.initials=None
        self.color=None
        self.continent_id=None
        self.continent_name=None
        self.capital_region_id=None
        self.capital_region_name=None

    def __construct(self, country_data):
        self.id=country_data["id"]
        self.name=country_data["name"]
        self.initials=country_data["initials"]
        self.color=country_data["color"]
        self.continent_id=country_data["continent_id"]
        self.continent_name=country_data["continent_name"]
        self.capital_region_id=country_data["capital_region_id"]
        self.capital_region_name=country_data["capital_region_name"]

    def by_id(self, id):
        """
        Returns Country info as dict
        Requires valid country ID
        """
        country_data = None
        for item in self.__country_dict:
            if item["id"] == str(id):
                country_data = item
                break
        self.__construct(country_data)


    def by_name(self, name):
        """
        Returns Country info as dict
        Requires valid country name
        """
        country_data = None

        for item in self.__country_dict:
            if item["name"].lower() == name.lower():
                country_data = item
                break

        self.__construct(country_data)
