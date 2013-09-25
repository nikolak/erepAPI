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
        self.__resource = "region"
        self.__action = "citizens"
        self.__params = ["regionId=" + self.id, "page=" + self.page]

        if not self.id.isdigit() or not self.page.isdigit():
            raise ValueError
        else:
            self.__url = api._construct_url(self.__resource, self.__action, self.__params)
            self.__headers = api._construct_headers(self.__url)
        self.data = api._load(self.__url, self.__headers)
        if self.data["citizens"] is False:
            self.citizenIDs = None
        else:
            self.citizenIDs = [int(cit_id["citizen_id"]) for cit_id in self.data["citizens"]]
