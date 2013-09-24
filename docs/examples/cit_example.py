#Ask for Citizen ID from user then show citizen info
#Python 2.7, change raw_input to input for 3.x version

from erepapi import api, Citizen

api.public_key="your public key goes here"
api.private_key="your private key goes here"

while True:
    entered_id=raw_input("Enter citizen id:\n>>>")
    try:
        citizen_info=Citizen(entered_id)
        print("Username:{}\nStrength:{}\nMilitary Rank:{}\n{}".format(citizen_info.name,
                                                        citizen_info.strength,
                                                        citizen_info.rank_value,
                                                        "*"*20))
        if citizen_info.in_unit:
            print("Unit name:{}\nPlayer is unit leader:{}\n".format(citizen_info.unit_name,
                                                                    citizen_info.unit_leader))

        print("Citizen has following achievements:")
        for achievement,ammount in citizen_info.achievements:
            print("{}:{}".format(achievement,ammount))
    except ValueError:
        print("The ID you supplied is not a valid one, try again.")


#Output

# Enter citizen id:
# >>>1649964
# Username:Unihorn
# Strength:37153.371
# Military Rank:64
# ********************
# Unit name:Tesla Troopers
# Player is unit leader:False
#
# Citizen has following achievements:
# Ambassador:1
# Hero:25
# Super trooper:148
# Hard worker:50
# Mercenary:1
# Congressman:6
# Media mogul:2
# True patriot:26
# Resistance hero:2
# Campaign hero:1
# President:1
# Total:264
# Society builder:1
# Enter citizen id:
# >>>