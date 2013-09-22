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
# SOFTWARE
import api

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
        self.__resource = "countries"
        self.__action = "index"
        self.__url = api._construct_url(self.__resource, self.__action)
        self.__headers = api._construct_headers(self.__url)
        self.data = api._load(self.__url, self.__headers)
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
