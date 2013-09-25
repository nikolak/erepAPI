#Ask for country ID, name or just print list of all countries
#Python 2.7, change raw_input to input for 3.x version

from erepapi import api, Country

api.public_key="your public key goes here"
api.private_key="your private key goes here"


country=Country()

while True:
    user_choice=int(raw_input("Enter option.\n1. List all countries\n"
                              "2. Print country info from name\n"
                              "3. Print country info from ID\n>>>"))

    if user_choice==1:
        for item in country.all_countries:
            print(item)

    elif user_choice==2:
        country_name=raw_input("Enter country name:\n>>>")
        country.by_name(country_name)
        if country.name is None:
            print("No country found by that name")
        else:
            print("Country:{}\nID:{}\nInitials:{}\nColor:{}\n"
                  "Continent ID:{}\nContinent Name:{}\n"
                  "Capital region ID:{}\nCapital region name:{}".format(
                country.name,country.id,country.initials,
                country.color,country.continent_id,
                country.continent_name,country.capital_region_id,
                country.capital_region_name
            ))

    elif user_choice==3:
        country_id=raw_input("Enter country ID:\n>>>")
        country.by_id(country_id)
        if country.name is None:
            print("No country found by that ID")
        else:
            print("Country:{}\nID:{}\nInitials:{}\nColor:{}\n"
                  "Continent ID:{}\nContinent Name:{}\n"
                  "Capital region ID:{}\nCapital region name:{}".format(
                country.name, country.id, country.initials,
                country.color, country.continent_id,
                country.continent_name, country.capital_region_id,
                country.capital_region_name
            ))

    else:
        print("Invalid input, try again")


# Output

#Enter option.
#1. List all countries
#2. Print country info from name
#3. Print country info from ID
#>>>1
#Albania
#Argentina
#Australia
#Austria
#[...]
#Enter option.
#1. List all countries
#2. Print country info from name
#3. Print country info from ID
#>>>2
#Enter country name:
#>>>Serbia
#Country:Serbia
#ID:65
#Initials:CS
#Color:FFB47F
#Continent ID:1
#Continent Name:None
#Capital region ID:743
#Capital region name:Kosovo
#Enter option.
#1. List all countries
#2. Print country info from name
#3. Print country info from ID
#>>>3
#Enter country ID:
#>>>65
#Country:Serbia
#ID:65
#Initials:CS
#Color:FFB47F
#Continent ID:1
#Continent Name:None
#Capital region ID:743
#Capital region name:Kosovo
#Enter option.
#1. List all countries
#2. Print country info from name
#3. Print country info from ID
#>>>