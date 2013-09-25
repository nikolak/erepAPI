#Ask for country ID from user then show all regions that belong to that country
# then prompt region name and display more info about it.
#Python 2.7, change raw_input to input for 3.x version

from erepapi import api, CountryRegions

api.public_key="your public key goes here"
api.private_key="your private key goes here"


while True:
    entered_id=raw_input("Enter Country id:\n>>>")
    try:
        regions_object=CountryRegions(entered_id)

        print("All regions:")
        for region in regions_object.regions:
            print("\t",region.name)

        info_region_name=raw_input("Enter region name to find out more about it:\n>>>")
        region_object=regions_object.get(info_region_name,None)

        if region_object is None:
            print("That region is not part of this country... exiting")
        else:
            print("Name:{}\nID:{}\nOwner ID:{}\nOriginal owner ID:{}\nURL:{}".format(region_object.name,
                                                                                     region_object.id,
                                                                                     region_object.owner_id,
                                                                                     region_object.original_owner_id,
                                                                                     region_object.url))

    except ValueError:
        print("Invalid country id")

#Enter Country id:
#>>>65
#All regions:
#('\t', u'Kosovo')
#('\t', u'Vojvodina')
#('\t', u'Belgrade')
#('\t', u'Sumadija')
#('\t', u'Eastern Serbia')
#('\t', u'Western Serbia')
#('\t', u'Raska')
#('\t', u'Southern Serbia')
#Enter region name to find out more about it:
#>>>Belgrade
#Name:Belgrade
#ID:635
#Owner ID:65
#Original owner ID:65
#URL:http://www.erepublik.com/en/main/region/Belgrade