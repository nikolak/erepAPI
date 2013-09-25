========
Usage
========

To use erepapi in a project first set up api keys then you can use any of the classes described below:

Setting API keys
----------------

To use erepublik api you must obtain private and public api keys.

To set those keys import api from erepapi::

    from erepapi import api
    api.public_key=<your public key>
    api.private_key=<your private key>


Citizen Class
-------------

To use citizen class just import it from erepapi::

    from erepapi import Citizen

You can't instantiate empty ``Citizen`` object, Citizen class takes citizen ID
when initializing as only argument.


Example of getting citizen name and some other info:

.. literalinclude:: examples/cit_example.py

Citizen object variables
^^^^^^^^^^^^^^^^^^^^^^^^

+-----------------------------------+---------------------------------------------------------------+-----------+
| Variable name                     | Description                                                   | Type      |
+===================================+===============================================================+===========+
+-----------------------------------+---------------------------------------------------------------+-----------+
|``id``                             | supplied user ID                                              |string     |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``name``                           |Profile name                                                   |string     |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``is_alive``                       |Is user profile alive                                          |boolean    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``has_avatar``                     |Whether user has custom avatar or not                          |boolean    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``experience_points``              |Current number of experience points user has                   |integer    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``level``                          |Current level number                                           |integer    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``birthday``                       |Date of profile creation, string. MMM DD, YYYY                 |string     |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``national_rank``                  |Current national rank number                                   |integer    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``profile_url``                    |full URL to user profile based on ID                           |string     |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``strength``                       |current number of strength points                              |float      |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``rank_points``                    |number of rank points                                          |integer    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``rank_stars``                     |number of rank stars                                           |integer    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``rank_icon``                      |URL to rank icon file                                          |string     |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``achievements``                   |Dictionary of achievements k,v = name,quantity                 |dictionary |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``citizenship_country_id``         |self explanatory                                               |integer    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``citizenship_country_name``       |self explanatory                                               |string     |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``citizenship_country_initials``   |self explanatory                                               |string     |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``citizenship_region_id``          |self explanatory                                               |integer    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``citizenship_region_name``        |self explanatory                                               |string     |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``residence_country_id``           |self explanatory                                               |integer    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``residence_country_name``         |self explanatory                                               |string     |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``residence_country_initials``     |self explanatory                                               |string     |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``residence_region_id``            |self explanatory                                               |integer    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``residence_region_name``          |self explanatory                                               |string     |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``party_member``                   |true if player is part of political party otherwise false.     |boolean    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``party_id``                       |id of the party (if in one)                                    |integer    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``party_name``                     |name of the party                                              |string     |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``is_president``                   |True if selected player is party president, otherwise False    |boolean    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``in_unit``                        |true if player is part of political party otherwise false      |boolean    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``unit_id``                        |id of the military unit (if in unit)                           |integer    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``unit_name``                      |name of the unit                                               |string     |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``unit_leader``                    |true if player is leader of the military unit, otherwise False |boolean    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``owns_newspaper``                 |True if player owns newspapers otherwise False                 |boolean    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``newspaper_id``                   |id of the newspapers (if one exists)                           |integer    |
+-----------------------------------+---------------------------------------------------------------+-----------+
|``newspaper_name``                 |name of the newspapers                                         |string     |
+-----------------------------------+---------------------------------------------------------------+-----------+


Allies dictionary structure; country names are keys(strings)::

    {
        country_name:{"id":country_id,
                      "initials":country_initials},

        country_name:{"id":country_id,
                      "initials":country_initials},
        [...]
    }

Error types raised
^^^^^^^^^^^^^^^^^^

``ValueError`` if provided ID is not valid or doesn't exist.


Battle Class
------------

To use citizen class just import it from erepapi::

    from erepapi import Battle

You can't instantiate empty ``Battle`` object, Battle class takes battle ID
when initializing as only argument.

Example of getting battle info from ID:

.. literalinclude:: examples/battle_example.py


Battle object variables
^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------+-------------------------------------------------------------------------------+-----------+
| Variable name             | Description                                                                   | Type      |
+===========================+===============================================================================+===========+
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``region_id``              |id of the on which the battle is being fought on                               |integer    |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``region_name``            |name of the region                                                             |string     |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``start``                  |date and time of the battle start, `YYYY-MM-DD HH:MM:SS` format                |string     |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``end``                    |date and time of the battle end `YYYY-MM-DD HH:MM:SS` format, otherwise `None` |string     |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``finish_reason``          |reason for battle finish if the battle has ended                               |string     |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``defender_id``            |id of the country that's being attacked(defender)                              |integer    |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``attacker_id``            |id of the country that's attacking(attacker) defender                          |integer    |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``defender_initials``      |initials of the country that's being attacked(defender)                        |string     |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``attacker_initials``      |initials of the country that's attacking(attacker)                             |string     |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``defender_allies``        |allies of the country that's being attacked(defender)                          |dictionary |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``attacker_allies``        |allies of the country that's attacking(attacker)                               |dictionary |
+---------------------------+-------------------------------------------------------------------------------+-----------+


Error types raised
^^^^^^^^^^^^^^^^^^

``ValueError`` if provided ID is not valid or doesn't exist.


Country Regions Class
------------

To use country regions class just import it from erepapi::

    from erepapi import CountryRegions

You can't instantiate empty ``CountryRegions`` object, CountryRegions class takes country ID
when initializing as only argument.

Example usage:

.. literalinclude:: examples/c_regions_example.py

Battle object variables
^^^^^^^^^^^^^^^^^^^^^^^

``regions`` variable contains list of ``Region`` objects each with following variables:

+---------------------------+-------------------------------------------------------------------------------+-----------+
| Variable name             | Description                                                                   | Type      |
+===========================+===============================================================================+===========+
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``name``                   |Name of the region                                                             |string     |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``id``                     |ID of the region                                                               |intger     |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``owner_id``               |ID of the country that's current owner                                         |integer    |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``original_owner_id``      |ID of the original owner country                                               |integer    |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``url``                    |Full in game url for that region                                               |string     |
+---------------------------+-------------------------------------------------------------------------------+-----------+

Error types raised
^^^^^^^^^^^^^^^^^^

``ValueError``  if the supplied Country ID is invalid.

Region Class
------------

To use region class just import it from erepapi::

    from erepapi import Regions


This will return object with ``id`` and ``citizenIDs`` variables, the latter contains list of citizen IDs that live in
that region.

``Regions`` requries ``id`` parameter and accepts optional ``page`` param (as integer), the first one being the region ID
the second page of the ids. 100 ids are displayed max per page.

If region has no citizens or the page is empty ``citizenIDs`` will be equal to ``None``

Example usage::

    from erepapi import api, Region

    api.public_key="your public key"
    api.private_key="your private key"

    region=Region(635, page=2)

    for citizenID in region.citizenIDs:
        #do something with citizenID (integer)

Error types raised
^^^^^^^^^^^^^^^^^^

``ValueError`` if the supplied ID or page number is invalid type.


Country Class
------------
To use region class just import it from erepapi::

    from erepapi import Country

Base class has ``None`` values assigned to variables below and ``all_countries`` variable that contains list of
names for every country that's available in game, list is fetched from API not hard coded

After initialization 2 functions can be used to update country variables, ``by_name`` and ``by_id`` these functions require
country name or country ID, respectively, for information on which country data to fetch.

Variables stay equal to ``None`` if supplied id or name are invalid/ don't exist.


Example usage:

.. literalinclude:: examples/country_example.py


Country object variables
^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------+-------------------------------------------------------------------------------+-----------+
| Variable name             | Description                                                                   | Type      |
+===========================+===============================================================================+===========+
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``id``                     |Country ID                                                                     |integer    |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``name``                   |Country name                                                                   |string     |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``initials``               |Country initials                                                               |string     |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``color``                  |Country color code                                                             |string     |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``continent_id``           |Continent ID, this will always be equal to None but it exists...               |string     |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``continent_name``         |Continent name, always None                                                    |string     |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``capital_region_id``      |Capital region ID of that country                                              |integer    |
+---------------------------+-------------------------------------------------------------------------------+-----------+
|``capital_region_name``    |Capital region name of that country                                            |string     |
+---------------------------+-------------------------------------------------------------------------------+-----------+

Error types raised
^^^^^^^^^^^^^^^^^^

None