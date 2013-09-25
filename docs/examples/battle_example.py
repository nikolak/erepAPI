#Ask for battle/resistance ID from user then show battle info
#Python 2.7, change raw_input to input for 3.x version

from erepapi import api, Battle

api.public_key="your public key goes here"
api.private_key="your private key goes here"

while True:
    entered_id=raw_input("Enter battle id:\n>>>")

    battle_info=Battle(39841)

    try:
        print("{} (attacker) VS {} (defender)".format(battle_info.attacker_initials,
                                                      battle_info.defender_initials))
        print("Battle:{}; for {}\nResistance:{}\nStarted:{}\nEnded:{}".format(battle_info.id,
                                                                              battle_info.region_name,
                                                                              battle_info.is_resistance,
                                                                              battle_info.start,
                                                                              battle_info.end))
        print("Attacker allies (Name/ID):")
        for k,v in battle_info.attacker_allies.items():
            print "\t",k,v['id']

        print("Defender allies (Name/ID):")
        for k,v in battle_info.defender_allies.items():
            print "\t",k,v['id']

        print("-"*30)

    except ValueError:
        print("Invalid battle ID, try again...")


# Output

# Enter battle id:
# >>>39841
# TH (attacker) VS HR (defender)
# Battle:39841; for Andhra Pradesh
# Resistance:False
# Started:2013-03-29 08:55:12
# Ended:2013-03-30 02:53:05
# Attacker allies (Name/ID):
# 	Poland 35
# 	Indonesia 49
# 	Serbia 65
# 	Republic of Macedonia (FYROM) 79
# 	United Kingdom 29
# 	Slovenia 61
# 	Latvia 71
# 	Chile 64
# 	Hungary 13
# 	Japan 45
# 	Spain 15
# 	Bulgaria 42
# Defender allies (Name/ID):
# 	Canada 23
# 	Turkey 43
# 	Italy 10
# 	France 11
# 	Ireland 54
# 	Argentina 27
# 	Norway 37
# 	Israel 58
# 	Iran 56
# 	China 14
# 	Bosnia and Herzegovina 69
# 	Ukraine 40
# 	Netherlands 31
# 	Finland 39
# 	Sweden 38
# 	Republic of China (Taiwan) 81
# 	Russia 41
# 	Romania 1
# 	Albania 167
# 	Uruguay 74
# 	Colombia 78
# 	Greece 44
# ------------------------------
# Enter battle id:
# >>>