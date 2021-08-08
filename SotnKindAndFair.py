import json
import random
import math
import os
import shutil
import glob
from enum import Enum

below_25 = [
    "Skeleton",
    "Slogra",
    "Gaibon"
]
below_50 = [
    "Doppleganger 1"
]
chance_7 = [
    "Gremlin",
    "Large Slime",
    "Slime",
    "Wereskeleton",
    "Hellfire Beast",
    "Discus Lord",
    "Grave Keeper",
    "Bone Ark",
    "Lossoth",
    "Granfaloon",
    "Granfaloon Part"
]
chance_6 = [
    "Succubus",
    "Harpy",
    "Vandal Sword",
    "Flea Rider"
]
chance_5 = [
    "Flying Zombie Upper",
    "Flying Zombie Lower",
    "Lesser Demon",
    "Gorgon",
    "Black Panther",
    "White Dragon",
    "Fire Demon",
    "Dodo Bird",
    "Tombstone",
    "Jack O'Bones",
    "Yorick",
    "Nova Skeleton",
    "Spectral Sword 3",
    "Orobourous",
    "Dragon Rider",
    "Fire Warg",
    "Warg Rider",
    "Bomb Knight",
    "Bitterfly",
    "Sniper of Goth",
    "Ghost Dancer",
    "Azaghal",
    "Malachi",
    "Lion",
    "Tin Man",
    "Akmodan",
    "Cloaked Knight",
    "Darkwing Bat",
    "Karasuman",
    "Imp",
    "Balloon Pod",
    "Archer",
    "Scarecrow",
    "Shmoo",
    "Beezelbub",
    "Beezelbub Flies",
    "Fake Trevor",
    "Fake Grant",
    "Fake Sypha",
    "Medusa",
    "The Creature",
    "Minotaur 2",
    "Werewolf 2",
    "Guardian"
]
chance_4 = [
    "Dark Octopus",
    "Cave Troll",
    "Rock Knight",
    "Death 1",
    "Death 2",
    "Doppleganger 2",
    "Blue Venus Weed Unflowered",
    "Blue Venus Weed Flowered"
]
chance_3 = [
    "Frozen Half",
    "Salome",
    "Galamoth",
    "Galamoth Head"
]
skip = [
    "Zombie",
    "Warg",
    "Spike ball",
    "Intro Dracula 1",
    "Intro Dracula 2",
    "Shaft Orb",
    "Stone Skull"
]

below_25_range = []
below_50_range = []
chance_8_range = []
chance_7_range = []
chance_6_range = []
chance_5_range = []
chance_4_range = []
chance_3_range = []
chance_2_range = []

resist_pool = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4]

#Handitem: b1118 - b37e0
#Special: b382c - b429c
#Equip: b4308 - b5076
#???
#Enemies: b594c - b9f08

log = []

#Config

with open("Data\\Config.json", "r", encoding="utf-8") as file_reader:
    config = json.load(file_reader)

#Content

with open("Data\\Offsets\\Enemy.json", "r", encoding="utf-8") as file_reader:
    enemy_content = json.load(file_reader)

with open("Data\\Offsets\\Equipment.json", "r", encoding="utf-8") as file_reader:
    equipment_content = json.load(file_reader)

with open("Data\\Offsets\\HandItem.json", "r", encoding="utf-8") as file_reader:
    handitem_content = json.load(file_reader)

#Data

with open("Data\\Values\\Enemy.json", "r", encoding="utf-8") as file_reader:
    enemy_data = json.load(file_reader)

with open("Data\\Values\\Equipment.json", "r", encoding="utf-8") as file_reader:
    equipment_data = json.load(file_reader)

with open("Data\\Values\\HandItem.json", "r", encoding="utf-8") as file_reader:
    handitem_data = json.load(file_reader)

#Random

for i in range(24):
    below_25_range.append(i+1)

for i in range(49):
    below_50_range.append(i+1)

for i in range(98):
    if i <= 49:
        for e in range(7):
            chance_8_range.append(i+1)
    else:
        chance_8_range.append(i+1)

for i in range(98):
    if i <= 49:
        for e in range(6):
            chance_7_range.append(i+1)
    else:
        chance_7_range.append(i+1)

for i in range(98):
    if i <= 49:
        for e in range(5):
            chance_6_range.append(i+1)
    else:
        chance_6_range.append(i+1)

for i in range(98):
    if i <= 49:
        for e in range(4):
            chance_5_range.append(i+1)
    else:
        chance_5_range.append(i+1)

for i in range(98):
    if i <= 49:
        for e in range(3):
            chance_4_range.append(i+1)
    else:
        chance_4_range.append(i+1)

for i in range(98):
    if i <= 49:
        for e in range(2):
            chance_3_range.append(i+1)
    else:
        chance_3_range.append(i+1)

for i in range(98):
    chance_2_range.append(i+1)

class Attributes(Enum):
    HIT = 0x0020
    CUT = 0x0040
    POI = 0x0080
    CUR = 0x0100
    STO = 0x0200
    WAT = 0x0400
    DAR = 0x0800
    HOL = 0x1000
    ICE = 0x2000
    LIG = 0x4000
    FLA = 0x8000

def preset():
    if (config["Value"]["Option1"] == "Y" or config["Value"]["Option1"] == "N") and (config["Value"]["Option2"] == "Y" or config["Value"]["Option2"] == "N") and (config["Value"]["Option3"] == "Y" or config["Value"]["Option3"] == "N") and (config["Value"]["Option4"] == "Y" or config["Value"]["Option4"] == "N"):
        print("Randomize levels ? (Y/N):")
        print(config["Value"]["Option1"])
        print("Randomize resistances ? (Y/N):")
        print(config["Value"]["Option2"])
        print("Limit level ups ? (Y/N):")
        print(config["Value"]["Option3"])
        print("Apply item tweaks ? (Y/N):")
        print(config["Value"]["Option4"])
        while True:
            confirm = input("Is this okay ? (Y/N):\n").upper()
            if confirm == "Y" or confirm == "N":
                break
        print("")
        if confirm == "N":
            prompt()
    else:
        prompt()

def prompt():
    while True:
        while True:
            config["Value"]["Option1"] = input("Randomize levels ? (Y/N):\n").upper()
            if config["Value"]["Option1"] == "Y" or config["Value"]["Option1"] == "N":
                break
        while True:
            config["Value"]["Option2"] = input("Randomize resistances ? (Y/N):\n").upper()
            if config["Value"]["Option2"] == "Y" or config["Value"]["Option2"] == "N":
                break
        while True:
            config["Value"]["Option3"] = input("Limit level ups ? (Y/N):\n").upper()
            if config["Value"]["Option3"] == "Y" or config["Value"]["Option3"] == "N":
                break
        while True:
            config["Value"]["Option4"] = input("Apply item tweaks ? (Y/N):\n").upper()
            if config["Value"]["Option4"] == "Y" or config["Value"]["Option4"] == "N":
                break
        while True:
            confirm = input("Is this okay ? (Y/N):\n").upper()
            if confirm == "Y" or confirm == "N":
                break
        print("")
        if confirm == "Y":
            break

def random_enemy(level, resist):
    for i in range(len(enemy_data)):
        if enemy_data[i]["Key"] in skip:
            continue
        
        if level:
            if enemy_data[i]["Value"]["IsMainEntry"]:
                if "Dracula" in enemy_data[i]["Key"]:
                    enemy_data[i]["Value"]["Level"] = abs(shaft_level - 100)
                elif enemy_data[i]["Key"] in below_25:
                    enemy_data[i]["Value"]["Level"] = random.choice(below_25_range)
                elif enemy_data[i]["Key"] in below_50:
                    enemy_data[i]["Value"]["Level"] = random.choice(below_50_range)
                elif enemy_data[i]["Key"] in chance_7:
                    enemy_data[i]["Value"]["Level"] = random.choice(chance_7_range)
                elif enemy_data[i]["Key"] in chance_6:
                    enemy_data[i]["Value"]["Level"] = random.choice(chance_6_range)
                elif enemy_data[i]["Key"] in chance_5:
                    enemy_data[i]["Value"]["Level"] = random.choice(chance_5_range)
                elif enemy_data[i]["Key"] in chance_4:
                    enemy_data[i]["Value"]["Level"] = random.choice(chance_4_range)
                elif enemy_data[i]["Key"] in chance_3:
                    enemy_data[i]["Value"]["Level"] = random.choice(chance_3_range)
                elif enemy_data[i]["Key"] == "Shaft":
                    enemy_data[i]["Value"]["Level"] = random.choice(chance_2_range)
                    shaft_level = enemy_data[i]["Value"]["Level"]
                else:
                    enemy_data[i]["Value"]["Level"] = random.choice(chance_8_range)
                
            else:
                enemy_data[i]["Value"]["Level"] = enemy_data[i-1]["Value"]["Level"]
        
        if enemy_data[i]["Key"] == "Dracula":
            continue
        
        if resist:
            for e in Attributes:
                if enemy_data[i]["Value"]["IsMainEntry"] or enemy_data[i]["Key"] == "Dracula Hands":
                    enemy_data[i]["Value"]["Resistances"][str(e)[11:]] = random.choice(resist_pool)
                else:
                    enemy_data[i]["Value"]["Resistances"][str(e)[11:]] = enemy_data[i-1]["Value"]["Resistances"][str(e)[11:]]

def limit_exp():
    for i in enemy_data:
        if i["Value"]["IsBoss"]:
            i["Value"]["ExperienceLevel1"] = math.ceil(i["Value"]["ExperienceLevel1"]/10)
            i["Value"]["ExperienceLevel99"] = math.ceil(i["Value"]["ExperienceLevel99"]/10)
        else:
            i["Value"]["ExperienceLevel1"] = 0
            i["Value"]["ExperienceLevel99"] = 0

def description():
    file.seek(0xF2400)
    file.write(str.encode("Shocking"))
    file.seek(0xF2538)
    file.write(str.encode(" flail         "))
    file.seek(0xF2864)
    file.write(str.encode("Moist"))
    file.seek(0xF287F)
    file.write(str.encode("fire"))
    file.seek(0xF3C6D)
    file.write(str.encode("CON"))
    file.seek(0xF3C75)
    file.write(str.encode("O"))
    file.seek(0xF3C9A)
    file.write(str.encode("T  "))
    file.seek(0xF3DB0)
    file.write(str.encode("CON"))
    file.seek(0xF4844)
    file.write(str.encode("Resistant to evil attacks "))
    file.seek(0xF43FC)
    file.write(str.encode("Immune to water "))
    file.seek(0xF4420)
    file.write(str.encode("Affection for cats          "))
    file.seek(0xF4450)
    file.write(str.encode("Immune to lightning         "))
    file.seek(0xF4480)
    file.write(str.encode("Immune to darkness          "))
    file.seek(0xF44B0)
    file.write(str.encode("Immune to ice            "))
    file.seek(0xF44DC)
    file.write(str.encode("Immune to fire            "))
    file.seek(0xF4508)
    file.write(str.encode("Immune to light           "))
    file.seek(0xF486C)
    file.write(str.encode("Immunity to all status effects"))

def write_enemy_to_rom():
    for i in range(len(enemy_content)):
        health = math.ceil(((enemy_data[i]["Value"]["HealthLevel99"] - enemy_data[i]["Value"]["HealthLevel1"])/98)*(enemy_data[i]["Value"]["Level"]-1) + enemy_data[i]["Value"]["HealthLevel1"])
        if health < 0:
            health = 0
        if health > 32768:
            health = 32768
        high, low = divmod(health, 0x100)
        file.seek(int(enemy_content[i]["Value"]["Health"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        strength = math.ceil(((enemy_data[i]["Value"]["ContactDamageLevel99"] - enemy_data[i]["Value"]["ContactDamageLevel1"])/98)*(enemy_data[i]["Value"]["Level"]-1) + enemy_data[i]["Value"]["ContactDamageLevel1"])
        if strength < 0:
            strength = 0
        if strength > 32768:
            strength = 32768
        if enemy_data[i]["Value"]["IsMainEntry"]:
            main_strength = strength
        high, low = divmod(strength, 0x100)
        file.seek(int(enemy_content[i]["Value"]["ContactDamage"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        high, low = divmod(int(enemy_data[i]["Value"]["ContactDamageType"], 16), 0x100)
        file.seek(int(enemy_content[i]["Value"]["ContactDamageType"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        defense = math.ceil(((enemy_data[i]["Value"]["DefenseLevel99"] - enemy_data[i]["Value"]["DefenseLevel1"])/98)*(enemy_data[i]["Value"]["Level"]-1) + enemy_data[i]["Value"]["DefenseLevel1"])
        if defense < 0:
            defense = 0
        if defense > 32768:
            defense = 32768
        high, low = divmod(defense, 0x100)
        file.seek(int(enemy_content[i]["Value"]["Defense"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        high, low = divmod(int(enemy_data[i]["Value"]["Surface"], 16), 0x100)
        file.seek(int(enemy_content[i]["Value"]["Surface"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        weak = 0
        strong = 0
        immune = 0
        absorb = 0
        for e in Attributes:
            if enemy_data[i]["Value"]["Resistances"][str(e)[11:]] == 0:
                weak += e.value
            elif enemy_data[i]["Value"]["Resistances"][str(e)[11:]] == 2:
                strong += e.value
            elif enemy_data[i]["Value"]["Resistances"][str(e)[11:]] == 3:
                immune += e.value
            elif enemy_data[i]["Value"]["Resistances"][str(e)[11:]] == 4:
                absorb += e.value
        
        high, low = divmod(weak, 0x100)
        file.seek(int(enemy_content[i]["Value"]["Resistances"]["Weak"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        high, low = divmod(strong, 0x100)
        file.seek(int(enemy_content[i]["Value"]["Resistances"]["Strong"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        high, low = divmod(immune, 0x100)
        file.seek(int(enemy_content[i]["Value"]["Resistances"]["Immune"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        high, low = divmod(absorb, 0x100)
        file.seek(int(enemy_content[i]["Value"]["Resistances"]["Absorb"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        level = enemy_data[i]["Value"]["Level"]
        high, low = divmod(level, 0x100)
        file.seek(int(enemy_content[i]["Value"]["Level"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        experience = math.ceil(((enemy_data[i]["Value"]["ExperienceLevel99"] - enemy_data[i]["Value"]["ExperienceLevel1"])/98)*(enemy_data[i]["Value"]["Level"]-1) + enemy_data[i]["Value"]["ExperienceLevel1"])
        if experience < 0:
            experience = 0
        if experience > 32768:
            experience = 32768
        high, low = divmod(experience, 0x100)
        file.seek(int(enemy_content[i]["Value"]["Experience"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        for e in range(len(enemy_content[i]["Value"]["AttackDamage"])):
            damage = math.ceil(enemy_data[i]["Value"]["AttackDamageMultiplier"][e]*main_strength)
            if damage < 0:
                damage = 0
            if damage > 32768:
                damage = 32768
            high, low = divmod(damage, 0x100)
            file.seek(int(enemy_content[i]["Value"]["AttackDamage"][e], 16))
            file.write(bytes([low]))
            file.write(bytes([high]))
            
        for e in range(len(enemy_content[i]["Value"]["AttackDamageType"])):
            high, low = divmod(int(enemy_data[i]["Value"]["AttackDamageType"][e], 16), 0x100)
            file.seek(int(enemy_content[i]["Value"]["AttackDamageType"][e], 16))
            file.write(bytes([low]))
            file.write(bytes([high]))

def write_item_to_rom():
    for i in range(len(equipment_content)):
        if equipment_data[i]["Value"]["Attack"] < -32767:
            equipment_data[i]["Value"]["Attack"] = -32767
        if equipment_data[i]["Value"]["Attack"] > 32768:
            equipment_data[i]["Value"]["Attack"] = 32768
        if equipment_data[i]["Value"]["Attack"] < 0:
            equipment_data[i]["Value"]["Attack"] += 65536
        high, low = divmod(int(equipment_data[i]["Value"]["Attack"]), 0x100)
        file.seek(int(equipment_content[i]["Value"]["Attack"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        if equipment_data[i]["Value"]["Defense"] < -32767:
            equipment_data[i]["Value"]["Defense"] = -32767
        if equipment_data[i]["Value"]["Defense"] > 32768:
            equipment_data[i]["Value"]["Defense"] = 32768
        if equipment_data[i]["Value"]["Defense"] < 0:
            equipment_data[i]["Value"]["Defense"] += 65536
        high, low = divmod(int(equipment_data[i]["Value"]["Defense"]), 0x100)
        file.seek(int(equipment_content[i]["Value"]["Defense"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        if equipment_data[i]["Value"]["Strength"] < -127:
            equipment_data[i]["Value"]["Strength"] = -127
        if equipment_data[i]["Value"]["Strength"] > 128:
            equipment_data[i]["Value"]["Strength"] = 128
        if equipment_data[i]["Value"]["Strength"] < 0:
            equipment_data[i]["Value"]["Strength"] += 256
        file.seek(int(equipment_content[i]["Value"]["Strength"], 16))
        file.write(bytes([int(equipment_data[i]["Value"]["Strength"])]))
        
        if equipment_data[i]["Value"]["Constitution"] < -127:
            equipment_data[i]["Value"]["Constitution"] = -127
        if equipment_data[i]["Value"]["Constitution"] > 128:
            equipment_data[i]["Value"]["Constitution"] = 128
        if equipment_data[i]["Value"]["Constitution"] < 0:
            equipment_data[i]["Value"]["Constitution"] += 256
        file.seek(int(equipment_content[i]["Value"]["Constitution"], 16))
        file.write(bytes([int(equipment_data[i]["Value"]["Constitution"])]))
        
        if equipment_data[i]["Value"]["Intelligence"] < -127:
            equipment_data[i]["Value"]["Intelligence"] = -127
        if equipment_data[i]["Value"]["Intelligence"] > 128:
            equipment_data[i]["Value"]["Intelligence"] = 128
        if equipment_data[i]["Value"]["Intelligence"] < 0:
            equipment_data[i]["Value"]["Intelligence"] += 256
        file.seek(int(equipment_content[i]["Value"]["Intelligence"], 16))
        file.write(bytes([int(equipment_data[i]["Value"]["Intelligence"])]))
        
        if equipment_data[i]["Value"]["Luck"] < -127:
            equipment_data[i]["Value"]["Luck"] = -127
        if equipment_data[i]["Value"]["Luck"] > 128:
            equipment_data[i]["Value"]["Luck"] = 128
        if equipment_data[i]["Value"]["Luck"] < 0:
            equipment_data[i]["Value"]["Luck"] += 256
        file.seek(int(equipment_content[i]["Value"]["Luck"], 16))
        file.write(bytes([int(equipment_data[i]["Value"]["Luck"])]))
        
        weak = 0
        strong = 0
        immune = 0
        absorb = 0
        for e in Attributes:
            if equipment_data[i]["Value"]["Resistances"][str(e)[11:]] == 0:
                weak += e.value
            elif equipment_data[i]["Value"]["Resistances"][str(e)[11:]] == 2:
                strong += e.value
            elif equipment_data[i]["Value"]["Resistances"][str(e)[11:]] == 3:
                immune += e.value
            elif equipment_data[i]["Value"]["Resistances"][str(e)[11:]] == 4:
                absorb += e.value
        
        high, low = divmod(weak, 0x100)
        file.seek(int(equipment_content[i]["Value"]["Resistances"]["Weak"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        high, low = divmod(strong, 0x100)
        file.seek(int(equipment_content[i]["Value"]["Resistances"]["Strong"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        high, low = divmod(immune, 0x100)
        file.seek(int(equipment_content[i]["Value"]["Resistances"]["Immune"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        high, low = divmod(absorb, 0x100)
        file.seek(int(equipment_content[i]["Value"]["Resistances"]["Absorb"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
    for i in range(len(handitem_content)):
        if handitem_data[i]["Value"]["Attack"] < -32767:
            handitem_data[i]["Value"]["Attack"] = -32767
        if handitem_data[i]["Value"]["Attack"] > 32768:
            handitem_data[i]["Value"]["Attack"] = 32768
        if handitem_data[i]["Value"]["Attack"] < 0:
            handitem_data[i]["Value"]["Attack"] += 65536
        high, low = divmod(int(handitem_data[i]["Value"]["Attack"]), 0x100)
        file.seek(int(handitem_content[i]["Value"]["Attack"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        if handitem_data[i]["Value"]["Defense"] < -32767:
            handitem_data[i]["Value"]["Defense"] = -32767
        if handitem_data[i]["Value"]["Defense"] > 32768:
            handitem_data[i]["Value"]["Defense"] = 32768
        if handitem_data[i]["Value"]["Defense"] < 0:
            handitem_data[i]["Value"]["Defense"] += 65536
        high, low = divmod(int(handitem_data[i]["Value"]["Defense"]), 0x100)
        file.seek(int(handitem_content[i]["Value"]["Defense"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        total = 0
        for e in Attributes:
            if handitem_data[i]["Value"]["Element"][str(e)[11:]]:
                total += e.value
        
        high, low = divmod(total, 0x100)
        file.seek(int(handitem_content[i]["Value"]["Element"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        file.seek(int(handitem_content[i]["Value"]["Sprite"], 16))
        file.write(bytes([int(handitem_data[i]["Value"]["Sprite"], 16)]))
        
        file.seek(int(handitem_content[i]["Value"]["Special"], 16))
        file.write(bytes([int(handitem_data[i]["Value"]["Special"], 16)]))
        
        high, low = divmod(int(handitem_data[i]["Value"]["Spell"], 16), 0x100)
        file.seek(int(handitem_content[i]["Value"]["Spell"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        if handitem_data[i]["Value"]["ManaCost"] < -32767:
            handitem_data[i]["Value"]["ManaCost"] = -32767
        if handitem_data[i]["Value"]["ManaCost"] > 32768:
            handitem_data[i]["Value"]["ManaCost"] = 32768
        if handitem_data[i]["Value"]["ManaCost"] < 0:
            handitem_data[i]["Value"]["ManaCost"] += 65536
        high, low = divmod(int(handitem_data[i]["Value"]["ManaCost"]), 0x100)
        file.seek(int(handitem_content[i]["Value"]["ManaCost"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        if handitem_data[i]["Value"]["StunFrames"] < -32767:
            handitem_data[i]["Value"]["StunFrames"] = -32767
        if handitem_data[i]["Value"]["StunFrames"] > 32768:
            handitem_data[i]["Value"]["StunFrames"] = 32768
        if handitem_data[i]["Value"]["StunFrames"] < 0:
            handitem_data[i]["Value"]["StunFrames"] += 65536
        high, low = divmod(int(handitem_data[i]["Value"]["StunFrames"]), 0x100)
        file.seek(int(handitem_content[i]["Value"]["StunFrames"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        if handitem_data[i]["Value"]["Range"] < -32767:
            handitem_data[i]["Value"]["Range"] = -32767
        if handitem_data[i]["Value"]["Range"] > 32768:
            handitem_data[i]["Value"]["Range"] = 32768
        if handitem_data[i]["Value"]["Range"] < 0:
            handitem_data[i]["Value"]["Range"] += 65536
        high, low = divmod(int(handitem_data[i]["Value"]["Range"]), 0x100)
        file.seek(int(handitem_content[i]["Value"]["Range"], 16))
        file.write(bytes([low]))
        file.write(bytes([high]))
        
        file.seek(int(handitem_content[i]["Value"]["Extra"], 16))
        file.write(bytes([int(handitem_data[i]["Value"]["Extra"], 16)]))

def read_from_rom():
    for i in enemy_content:
        entry = {}
        entry["Key"] = i["Key"]
        entry["Value"] = {}
        file.seek(int(i["Value"]["Health"], 16))
        entry["Value"]["Health"] = swap_bytes(file.read(2).hex())
        file.seek(int(i["Value"]["ContactDamage"], 16))
        entry["Value"]["ContactDamage"] = swap_bytes(file.read(2).hex())
        file.seek(int(i["Value"]["ContactDamageType"], 16))
        entry["Value"]["ContactDamageType"] = "0x{:04x}".format(swap_bytes(file.read(2).hex()))
        file.seek(int(i["Value"]["Defense"], 16))
        entry["Value"]["Defense"] = swap_bytes(file.read(2).hex())
        file.seek(int(i["Value"]["Surface"], 16))
        entry["Value"]["Surface"] = "0x{:04x}".format(swap_bytes(file.read(2).hex()))
        
        entry["Value"]["Resistances"] = {}
        for e in Attributes:
            entry["Value"]["Resistances"][str(e)[11:]] = 1
        
        file.seek(int(i["Value"]["Resistances"]["Weak"], 16))
        total = swap_bytes(file.read(2).hex())
        for e in Attributes:
            if (total & e.value) != 0:
                entry["Value"]["Resistances"][str(e)[11:]] = 0
        file.seek(int(i["Value"]["Resistances"]["Strong"], 16))
        total = swap_bytes(file.read(2).hex())
        for e in Attributes:
            if (total & e.value) != 0:
                entry["Value"]["Resistances"][str(e)[11:]] = 2
        file.seek(int(i["Value"]["Resistances"]["Immune"], 16))
        total = swap_bytes(file.read(2).hex())
        for e in Attributes:
            if (total & e.value) != 0:
                entry["Value"]["Resistances"][str(e)[11:]] = 3
        file.seek(int(i["Value"]["Resistances"]["Absorb"], 16))
        total = swap_bytes(file.read(2).hex())
        for e in Attributes:
            if (total & e.value) != 0:
                entry["Value"]["Resistances"][str(e)[11:]] = 4
        
        file.seek(int(i["Value"]["Level"], 16))
        entry["Value"]["Level"] = swap_bytes(file.read(2).hex())
        file.seek(int(i["Value"]["Experience"], 16))
        entry["Value"]["Experience"] = swap_bytes(file.read(2).hex())

        entry["Value"]["AttackDamage"] = []
        for e in i["Value"]["AttackDamage"]:
            file.seek(int(e, 16))
            entry["Value"]["AttackDamage"].append(swap_bytes(file.read(2).hex()))
        entry["Value"]["AttackDamageType"] = []
        for e in i["Value"]["AttackDamageType"]:
            file.seek(int(e, 16))
            entry["Value"]["AttackDamageType"].append("0x{:04x}".format(swap_bytes(file.read(2).hex())))
        log.append(entry)
    
    with open("SpoilerLog.json", "w") as file_writer:
        file_writer.write(json.dumps(log, indent=2))

def swap_bytes(bytes):
    high, low = divmod(int(bytes, 16), 0x100)
    string_high = format(high, '02x')
    string_low = format(low, '02x')
    string = string_low + string_high
    return int(string, 16)

#Main

preset()
print("Working...")

if glob.glob("Rom\\*.bin"):
    file_name = glob.glob("Rom\\*.bin")[0].split("\\")[1]
else:
    file_name = "NoBinFileFoundInFolder"

shutil.copyfile("Rom\\" + file_name, "ErrorRecalc\\" + file_name)

file = open("ErrorRecalc\\" + file_name, "r+b")

if config["Value"]["Option1"] == "Y" or config["Value"]["Option2"] == "Y":
    random_enemy(config["Value"]["Option1"] == "Y", config["Value"]["Option2"] == "Y")
if config["Value"]["Option3"] == "Y":
    limit_exp()
write_enemy_to_rom()
if config["Value"]["Option4"] == "Y":
    write_item_to_rom()
    description()
read_from_rom()

file.close()

root = os.getcwd()
os.chdir("ErrorRecalc")
os.system("cmd /c error_recalc.exe \"" + file_name + "\"")
os.chdir(root)

shutil.move("ErrorRecalc\\" + file_name, file_name)

with open("Data\\Config.json", "w") as file_writer:
    file_writer.write(json.dumps(config, indent=2))