erepAPI
=======

erepublik.com API wrapper.

"Documentation" http://api.erepublik.com/doc/

"map","industries" and "war" are not currently supported due to issues with official API at the time of writing.

# Classes

## Citizen

Requires player ID (as string or integer) as initial argument. Raises `invalidID` exception if not supplied or invalid ID

### Example usage


    >>> from erepublik import Citizen
    >>> player=Citizen("1649964") # where "1649964" is player ID
    >>> player
    <erepublik.Citizen object at 0xb743f14c>
    >>> player.national_rank
    202
    >>> player.strength
    20822.371
    >>> player.achievements["Total"]
    182
    >>> player.achievements["President"]
    1
    >>> player.in_unit
    True
    >>> for key,value in player.achievements.items():
    ...     print key,value
    ...
    Ambassador 1
    Hero 21
    Super trooper 83
    Hard worker 44
    Mercenary 1
    Congressman 6
    Media mogul 2
    True patriot 19
    Resistance hero 2
    Campaign hero 1
    President 1
    Total 182
    Society builder 1
    >>>



### Full list of player variables available in Citizen class

| Variable        | Description           | Type  |
|----------------|:---------------------:|:-----:|
| `id`        | supplied user ID         | string |
| `name`        | Profile name              |   string |
|`is_alive` | Is user profile alive |boolean|
|`has_avatar` | Wheter user has custom avatar or not|boolean|
|`experience_points`|Current number of experience points user has|integer|
|`level`|Current level number|integer|
|`birthday`|Date of profile creation, string. `MMM DD, YYYY`|string|
|`national_rank`|Current national rank number|integer|
|`profile_url`|full url to user profile based on ID|string|
|`strength`|current number of strenght points|float|
|`rank_points`|number of rank points|integer|
|`rank_stars`|number of rank stars|integer|
|`rank_icon`|url to rank icon file|string|
|`achievements`|Dictionary of achievements with keys as achievement name and quantaty(`integer`) as value.|Dictionary|
|`citizenship_country_id`|self explanitory |integer|
|`citizenship_country_name`|self explanitory| string|
|`citizenship_country_initials`|self explanitory|string|
|`citizenship_region_id`|self explanitory|integer|
|`citizenship_region_name`|self explanitory|string|
|`residence_country_id`|self explanitory |integer|
|`residence_country_name`|self explanitory|string|
|`residence_country_initials`|self explanitory |string|
|`residence_region_id`|self explanitory|integer|
|`residence_region_name`|self explanitory|string|
|`party_member`| true if player is part of political party otherwise false.|boolean|
||if player is member of political party, the following attributes are also available:|||
|`party_id`| id of the party|integer|
|`party_name`| name of the party |string|
|`is_president`| `True` if selected player is party president, otherwise `False`|boolean|
|`in_unit`| ture if player is part of political party otherwise false| boolean|
||If player is memeber of military unit the following attributes are also available:||
|`unit_id`| id of the military unit|integer|
|`unit_name`|name of the unit|string|
|`unit_leader`|true if player is leader of the military unit, otherwise false|boolean|
|`owns_newspaper`|True if player owns newspapers otherwise false|boolean|
||If player owns newspapers the following attributes are also available||
|`newspaper_id`| id of the newspapers|integer|
|`newspaper_name`|name of the newspapers|string|


## Country_regions

Requires country ID (as `string` or `integer`) as initial argument.

### Example usage

    >>> from erepublik import Country_regions
    >>> regions=Country_regions(65).regions
    >>> for k,v in regions.items():
    ...     print k,v["id"]
    ...
    Eastern Serbia 637
    Belgrade 635
    Vojvodina 634
    Kosovo 743
    Southern Serbia 640
    Western Serbia 638
    Sumadija 636
    Raska 639

Each key in `regions` is `region name`(string) and each coresponding value is dict and contains following key, value pairs:

| Key        | Value Description           |  Value Type  |
|----------------|:---------------------:|:-----:|
|`id`|region id|integer|
|`owner_id`|ID of the country that is currently owner of the region|integer|
|`original_owner_id`|ID of the country that was/is original owner|integer|
|`url`|full url to ingame page with region info|string|


## Countries

No initial parameters required.

Used to list all countries or to find country by name or by an ID and list its information.

Each item in returned dictionary is `string` only `continet_name` is `None`

### Example usage

    >>> for country in Countries().all_countries:
    ...     print country["id"],country["initials"]
    ...
    167 AL
    27 AR
    50 AU
    33 AT
    83 BY
    32 BE
    76 BO
    [...]

    >>> print Countries().by_id(65)
    {
        u'name': u'Serbia',
        u'color': u'FFB47F',
        u'capital_region_name': u'Belgrade',
        u'capital_region_id': u'635',
        u'continent_id': u'1',
        u'continent_name': None,
        u'id': u'65',
        u'initials': u'CS'
    }
    >>> print Countries().by_name("serbia")["initials"]
    CS

`all_countries` - is a `list` of dictionaries each with following structure:

    {
        "id":"string",
        "name":"string",
        "initials":"string",
        "color":"string",
        "continent_id":"string",
        "continent_name":None,
        "capital_region_id":None/string,
        "capital_region_name":None/string
    },

## Regions

Requires valid region ID and, optionally, page number as either `string`s or `integer`s; larger regions contain multiple pages of data.

Contains list of citizen IDs as integers who are living in that region.


### Example usage

    >>> from erepublik import Region
    >>> Region(450,page=2).citizenIDs
    [1379069, 1379214, 1380608, 1380647, 1382406, 1382685,... ]

## Battle

Requires valid battle ID (string/integer) as initial argument.

### Example usage

    >>> from erepublik import Battle
    >>> b=Battle(39841)
    >>> b.is_resistance
    False
    >>> b.region_id
    450
    >>> b.start
    '2013-03-29 08:55:12'
    >>> print b.end
    None
    >>> b.defender_id
    59
    >>> b.defender_initials
    u'TH'
    >>> for k,v in b.defender_alies.items():
    ...     print k,v["id"]
    ...
    Poland 35
    Indonesia 49
    Serbia 65
    Republic of Macedonia (FYROM) 79
    [...]

### Full list of battle variables available in Battle class

| Variable        | Description           | Type  |
|----------------|:---------------------:|:-----:|
|`region_id`|id of the on which the battle is being fought on|integer|
|`region_name`|name of the region|string|
|`start`|date and time of the battle start, `YYYY-MM-DD HH:MM:SS` format|string|
|`end`|date and time of the battle end `YYYY-MM-DD HH:MM:SS` format, otherwise `None`|string|
|`finish_reason`|reason for battle finish if the battle has ended|string|
|`defender_id`|id of the country that's being attacked(defender)|integer|
|`attacker_id`|id of the country that's attacking(attacker) defender|integer|
|`defender_initials`|initials of the country that's being attacked(defender)|string|
|`attacker_initials`|initials of the country that's attacking(attacker)|string|
|`defender_alies`|alies of the country that's being attacked(defender)|dictionary|
|`attacker_alies`|alies of the country that's attacking(attacker)|dictionary|

Alies dictionary, country names are strings:

{
    country_name:dictionary,
    country_name:dictionary,
    [...]
}


Alies dictionary values structure:

| Key        | Value Description           | Type  |
|----------------|:---------------------:|:-----:|
|`"id"`|Country ID of the ally country|integer|
|`"initials"`|Country initials of the ally country|string|

___

# Licence

Copyright (c) 2013 Nikola Kovacevic nikolak@outlook.com,nikola.kovacevic91@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
