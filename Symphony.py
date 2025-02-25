import Manager
import json
import random
import math
import os
import copy

def init():
    global damage_rate
    damage_rate = 1.0
    global attributes
    attributes = {
        "HIT": 0x0020,
        "CUT": 0x0040,
        "POI": 0x0080,
        "CUR": 0x0100,
        "STO": 0x0200,
        "WAT": 0x0400,
        "DAR": 0x0800,
        "HOL": 0x1000,
        "ICE": 0x2000,
        "LIG": 0x4000,
        "FLA": 0x8000
    }
    #Enemy Lists
    global level_skip
    level_skip = [
        "Zombie",
        "Warg"
    ]
    global resist_skip
    resist_skip = [
        "Intro Dracula 1",
        "Intro Dracula 2"
    ]
    global static_enemy
    static_enemy = [
        "Stone Skull",
        "Spike ball",
        "Evil Priest"
    ]
    level_skip.extend(static_enemy)
    resist_skip.extend(static_enemy)
    global final_bosses
    final_bosses = ("Shaft", "Dracula")
    global resist_pool
    resist_pool = []
    global special_id_to_enemy
    special_id_to_enemy = {}
    #FillResistPool
    for i in range(7):
        resist_pool.append(0)
    for i in range(35):
        resist_pool.append(1)
    for i in range(4):
        resist_pool.append(2)
    for i in range(2):
        resist_pool.append(3)
    for i in range(1):
        resist_pool.append(4)
    #Offsets
    global removal_offset
    removal_offset = [
        0x1195f8,
        0x119658,
        0x1196b8,
        0x1196f4,
        0x119730,
        0x119774,
        0x119634,
        0x119648,
        0x119694,
        0x1196a8,
        0x1196d0,
        0x1196e4,
        0x11970c,
        0x119720,
        0x119750,
        0x119764,
        0x1197b0,
        0x1197c4,
        0x4b6844c,
        0x4b6844e,
        0x4b68452,
        0x4b68450,
        0x4b68454,
        0x4b68456
    ]
    global forced_drops
    forced_drops = [
        0x4BC9324,
        0x4BC9328
    ]

def open_json():
    global offsets
    offsets = {}
    global values
    values = {}
    for i in os.listdir("Data\\Symphony\\Offsets"):
        name, extension = os.path.splitext(i)
        offsets[name] = {}
        with open("Data\\Symphony\\Offsets\\" + i, "r") as file_reader:
            offsets[name] = json.load(file_reader)
    for i in os.listdir("Data\\Symphony\\Values"):
        name, extension = os.path.splitext(i)
        with open("Data\\Symphony\\Values\\" + i, "r") as file_reader:
            values[name] = json.load(file_reader)
    global dictionary
    dictionary = {}
    for i in os.listdir("Data\\Symphony\\Dicts"):
        name, extension = os.path.splitext(i)
        with open("Data\\Symphony\\Dicts\\" + i, "r") as file_reader:
            dictionary[name] = json.load(file_reader)

def get_seed():
    #If the rom is randomized reuse its seed
    Manager.rom.seek(0x4389C6C)
    seed = int.from_bytes(Manager.rom.read(30), "big")
    if seed == 0x496E7075742081688168524943485445528168816820746F20706C617900:
        return random.random()
    else:
        start_with_spirit_orb()
        return seed

def apply_ppf_patch(patch):
    #Replicate PPF Studio's process of applying patches to not have to include it in the download
    with open("Data\\Symphony\\Patches\\" + patch + ".ppf", "r+b") as mod:
        progress = 0x3C
        while progress < os.path.getsize("Data\\Symphony\\Patches\\" + patch + ".ppf"):
            mod.seek(progress)
            offset = int.from_bytes(mod.read(8), "little")
            length = int.from_bytes(mod.read(1), "little")
            change = int.from_bytes(mod.read(length), "little")
            Manager.rom.seek(offset)
            Manager.rom.write(change.to_bytes(length, "little"))
            progress += 9 + length

def get_item_address():
    #candle
    zone_pos = 0x055724b8
    entity = 0x2494
    address = entity + 8
    print("0x{:04x}".format(zone_pos + address + address // 0x800 * 0x130))
    #item
    zone_pos = 0x04675f08
    zone_items = 0x0ec0
    index = 4
    address = zone_items + 0x02 * index
    print("0x{:04x}".format(zone_pos + address + address // 0x800 * 0x130))

def start_with_spirit_orb():
    #Start the player with spirit orb and fairy scroll
    Manager.rom.seek(0xFA97C)
    Manager.rom.write((0x0C04DB00).to_bytes(4, "little"))
    Manager.rom.seek(0x158C98)
    Manager.rom.write((0x34020003).to_bytes(4, "little"))
    Manager.rom.write((0x3C038009).to_bytes(4, "little"))
    Manager.rom.write((0xA062796F).to_bytes(4, "little"))
    Manager.rom.write((0xA0627973).to_bytes(4, "little"))
    Manager.rom.write((0x0803924F).to_bytes(4, "little"))
    Manager.rom.write((0x00000000).to_bytes(4, "little"))
    
def keep_equipment():
    #Prevent Death's cutscene from taking Alucard's equipment
    for i in removal_offset:
        Manager.rom.seek(i)
        Manager.rom.write((0).to_bytes(2, "little"))

def free_library():
    #Place a library card before Slogra and Gaibon in case they are near unbeatable
    drop = forced_drops[0]
    forced_drops.pop(0)
    Manager.rom.seek(drop)
    Manager.rom.write((0xA6).to_bytes(2, "little"))
    
def unused():
    #Invulnerability
    Manager.rom.seek(0x126626)
    Manager.rom.write((0).to_bytes(1, "little"))
    Manager.rom.seek(0x3A06F52)
    Manager.rom.write((0).to_bytes(1, "little"))
    Manager.rom.seek(0x59EB092)
    Manager.rom.write((0x1000).to_bytes(2, "little"))
    Manager.rom.seek(0x59EBC7A)
    Manager.rom.write((0x1000).to_bytes(2, "little"))
    #No experience
    Manager.rom.seek(0x117cf6)
    Manager.rom.write((0).to_bytes(1, "little"))
    Manager.rom.seek(0x117da0)
    Manager.rom.write((0).to_bytes(4, "little"))

def all_bigtoss():
    #Give every enemy attack the guaranteed bigtoss property
    for i in values["Enemy"]:
        if "Intro" in i or i == "Evil Priest":
            continue
        values["Enemy"][i]["DamageType"] = "0x{:04x}".format((int(values["Enemy"][i]["DamageType"], 16)//16)*16 + 5)
        for e in range(len(values["Enemy"][i]["AttackType"])):
            values["Enemy"][i]["AttackType"][e] = "0x{:04x}".format((int(values["Enemy"][i]["AttackType"][e], 16)//16)*16 + 5)

def reduce_bigtoss_damage(damage):
    #Reduce damage in such a way that the total bigtoss damage will on average be equal to regular damage
    return round(damage*Manager.lerp(1/1.5, 1, 240/(240 + damage)))

def infinite_wing_smash():
    #Give wing smash the same properties as in the saturn version but at a higher cost
    values["Spell"]["Wing Smash"]["ManaCost"] = round(values["Spell"]["Wing Smash"]["ManaCost"]*3.75)
    Manager.rom.seek(0x134990)
    Manager.rom.write((0).to_bytes(4, "little"))

def remove_enemy_drops():
    for i in offsets["Enemy"]:
        Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + int(dictionary["Properties"]["Enemy"]["Drop1"]["Offset"], 16)))
        Manager.rom.write((0).to_bytes(dictionary["Properties"]["Enemy"]["Drop1"]["Length"], "little"))
        Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + int(dictionary["Properties"]["Enemy"]["Drop2"]["Offset"], 16)))
        Manager.rom.write((0).to_bytes(dictionary["Properties"]["Enemy"]["Drop2"]["Length"], "little"))
    #Give a weapon at the start to compensate
    positive_weapons = []
    for i in dictionary["ItemId"]:
        if dictionary["ItemId"][i] in values["HandItem"]:
            if values["HandItem"][dictionary["ItemId"][i]]["Attack"] > 0 and not values["HandItem"][dictionary["ItemId"][i]]["Sprite"] in ["0x0f", "0x15"]:
                positive_weapons.append(i)
    drop = forced_drops[0]
    forced_drops.pop(0)
    Manager.rom.seek(drop)
    Manager.rom.write(int(random.choice(positive_weapons), 16).to_bytes(2, "little"))

def check_offset(offset):
    #Shift the input offset if it falls within one of the weird chunks of bytes
    start = 0x18
    position = int((offset - start)/0x930) + 1
    if offset >= start + 0x930*position - 0x130:
        offset += 0x130
    return offset

def write_simple_data():
    #Write data that doesn't need any specific process
    for i in offsets:
        if i == "Enemy":
            continue
        for e in offsets[i]:
            try:
                for o in values[i][e]:
                    try:
                        if dictionary["Properties"][i][o]["RawHex"]:
                            values[i][e][o] = int(values[i][e][o], 16)
                        else:
                            values[i][e][o] = values[i][e][o] & (0x100**dictionary["Properties"][i][o]["Length"]-1)
                        Manager.rom.seek(check_offset(int(offsets[i][e], 16) + int(dictionary["Properties"][i][o]["Offset"], 16)))
                        Manager.rom.write(int(values[i][e][o]).to_bytes(dictionary["Properties"][i][o]["Length"], "little"))
                    except (KeyError, TypeError):
                        continue
            except (KeyError, TypeError):
                continue

def write_complex_data():
    #ENEMY
    for i in offsets["Enemy"]:
        #Level
        level = values["Enemy"][i]["Level"]
        level = level & (0x100**dictionary["Properties"]["Enemy"]["Level"]["Length"]-1)
        Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + int(dictionary["Properties"]["Enemy"]["Level"]["Offset"], 16)))
        Manager.rom.write(level.to_bytes(dictionary["Properties"]["Enemy"]["Level"]["Length"], "little"))
        #Health
        max_health = values["Enemy"][i]["MaxHealth"]
        if max_health == 0x7FFF:
            min_health = max_health
        else:
            min_health = int(max_health/100)
        health = round(((max_health - min_health)/98)*(level-1) + min_health)
        health = Manager.check_meaningful_value(health)
        health = health & (0x100**dictionary["Properties"]["Enemy"]["Health"]["Length"]-1)
        Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + int(dictionary["Properties"]["Enemy"]["Health"]["Offset"], 16)))
        Manager.rom.write(health.to_bytes(dictionary["Properties"]["Enemy"]["Health"]["Length"], "little"))
        #Damage
        max_damage = values["Enemy"][i]["MaxDamage"]
        if i in static_enemy:
            min_damage = max_damage
        else:
            min_damage = int(max_damage/30)
        damage = round(((max_damage - min_damage)/98)*(level-1) + min_damage)
        damage = damage & (0x100**dictionary["Properties"]["Enemy"]["Damage"]["Length"]-1)
        Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + int(dictionary["Properties"]["Enemy"]["Damage"]["Offset"], 16)))
        if not values["Enemy"][i]["HasContact"]:
            Manager.rom.write((0).to_bytes(dictionary["Properties"]["Enemy"]["Damage"]["Length"], "little"))
        elif int(values["Enemy"][i]["DamageType"], 16) % 16 == 5:
            Manager.rom.write(reduce_bigtoss_damage(damage).to_bytes(dictionary["Properties"]["Enemy"]["Damage"]["Length"], "little"))
        else:
            Manager.rom.write(damage.to_bytes(dictionary["Properties"]["Enemy"]["Damage"]["Length"], "little"))
        #Defense
        max_defense = values["Enemy"][i]["MaxDefense"]
        min_defense = int(max_defense/10)
        defense = round(((max_defense - min_defense)/98)*(level-1) + min_defense)
        defense = defense & (0x100**dictionary["Properties"]["Enemy"]["Defense"]["Length"]-1)
        Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + int(dictionary["Properties"]["Enemy"]["Defense"]["Offset"], 16)))
        Manager.rom.write(defense.to_bytes(dictionary["Properties"]["Enemy"]["Defense"]["Length"], "little"))
        #Experience
        max_experience = values["Enemy"][i]["MaxExperience"]
        min_experience = int(max_experience/100)
        experience = round(((max_experience - min_experience)/98)*(level-1) + min_experience)
        experience = Manager.check_meaningful_value(experience)
        experience = experience & (0x100**dictionary["Properties"]["Enemy"]["Experience"]["Length"]-1)
        Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + int(dictionary["Properties"]["Enemy"]["Experience"]["Offset"], 16)))
        Manager.rom.write(experience.to_bytes(dictionary["Properties"]["Enemy"]["Experience"]["Length"], "little"))
        #Surface
        Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + int(dictionary["Properties"]["Enemy"]["Surface"]["Offset"], 16)))
        Manager.rom.write(int(values["Enemy"][i]["Surface"], 16).to_bytes(dictionary["Properties"]["Enemy"]["Surface"]["Length"], "little"))
        #Damage type
        Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + int(dictionary["Properties"]["Enemy"]["DamageType"]["Offset"], 16)))
        Manager.rom.write(int(values["Enemy"][i]["DamageType"], 16).to_bytes(dictionary["Properties"]["Enemy"]["DamageType"]["Length"], "little"))
        #Make stopwatch tolerance scale with level
        Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + 37))
        if values["Enemy"][i]["IsBoss"]:
            Manager.rom.write((0x30).to_bytes(1, "little"))
        elif values["Enemy"][i]["Level"] >= 40:
            Manager.rom.write((0x34).to_bytes(1, "little"))
        elif values["Enemy"][i]["Level"] >= 20:
            Manager.rom.write((0x16).to_bytes(1, "little"))
        else:
            Manager.rom.write((0x14).to_bytes(1, "little"))
        #Attack
        for e in range(len(offsets["Enemy"][i]["AttackAddress"])):
            #Attack correction
            attack = round(damage*values["Enemy"][i]["AttackCorrection"][e]**damage_rate)
            attack = attack & (0x100**dictionary["Properties"]["Enemy"]["Damage"]["Length"]-1)
            Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["AttackAddress"][e], 16) + int(dictionary["Properties"]["Enemy"]["Damage"]["Offset"], 16)))
            if int(values["Enemy"][i]["AttackType"][e], 16) % 16 == 5:
                Manager.rom.write(reduce_bigtoss_damage(attack).to_bytes(dictionary["Properties"]["Enemy"]["Damage"]["Length"], "little"))
            else:
                Manager.rom.write(attack.to_bytes(dictionary["Properties"]["Enemy"]["Damage"]["Length"], "little"))
            #Attack type
            Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["AttackAddress"][e], 16) + int(dictionary["Properties"]["Enemy"]["DamageType"]["Offset"], 16)))
            Manager.rom.write(int(values["Enemy"][i]["AttackType"][e], 16).to_bytes(dictionary["Properties"]["Enemy"]["DamageType"]["Length"], "little"))
            #Attack stopwatch tolerance
            Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["AttackAddress"][e], 16) + 37))
            if values["Enemy"][i]["Level"] >= 40 or values["Enemy"][i]["IsBoss"]:
                Manager.rom.write((0x20).to_bytes(1, "little"))
            elif values["Enemy"][i]["Level"] >= 20:
                Manager.rom.write((0x12).to_bytes(1, "little"))
            else:
                Manager.rom.write((0x00).to_bytes(1, "little"))
    #Display some damage and sound cues on enemies that lack them
    #Intro Dracula shown damage
    Manager.rom.seek(0xB7677)
    Manager.rom.write((0x08).to_bytes(1, "little"))
    Manager.rom.seek(0xB76EF)
    Manager.rom.write((0x08).to_bytes(1, "little"))
    #Zombie Trevor hit sound
    Manager.rom.seek(0xB94E4)
    Manager.rom.write((0x10).to_bytes(1, "little"))
    #Zombie Trevor shown damage
    Manager.rom.seek(0xB94E7)
    Manager.rom.write((0x08).to_bytes(1, "little"))
    #Beezelbub Flies shown damage
    Manager.rom.seek(0xB9267)
    Manager.rom.write((0x08).to_bytes(1, "little"))
    #Shaft Orb shown damage
    Manager.rom.seek(0xB92B7)
    Manager.rom.write((0x08).to_bytes(1, "little"))
    
    #EQUIPMENT
    for i in ["Enemy", "Equipment"]:
        for e in offsets[i]:
            if i == "Enemy":
                offset = int(offsets[i][e]["EnemyAddress"], 16)
            else:
                offset = int(offsets[i][e], 16)
            #Resistances
            weak = 0
            strong = 0
            immune = 0
            absorb = 0
            for o in attributes:
                if values[i][e]["Resistances"][o] == 0:
                    weak += attributes[o]
                elif values[i][e]["Resistances"][o] == 2:
                    strong += attributes[o]
                elif values[i][e]["Resistances"][o] == 3:
                    immune += attributes[o]
                elif values[i][e]["Resistances"][o] == 4:
                    absorb += attributes[o]
            Manager.rom.seek(check_offset(offset + int(dictionary["Properties"][i]["Weak"]["Offset"], 16)))
            Manager.rom.write(weak.to_bytes(dictionary["Properties"][i]["Weak"]["Length"], "little"))
            Manager.rom.seek(check_offset(offset + int(dictionary["Properties"][i]["Strong"]["Offset"], 16)))
            Manager.rom.write(strong.to_bytes(dictionary["Properties"][i]["Strong"]["Length"], "little"))
            Manager.rom.seek(check_offset(offset + int(dictionary["Properties"][i]["Immune"]["Offset"], 16)))
            Manager.rom.write(immune.to_bytes(dictionary["Properties"][i]["Immune"]["Length"], "little"))
            Manager.rom.seek(check_offset(offset + int(dictionary["Properties"][i]["Absorb"]["Offset"], 16)))
            Manager.rom.write(absorb.to_bytes(dictionary["Properties"][i]["Absorb"]["Length"], "little"))

def create_enemy_log():
    log = {}
    for i in values["Enemy"]:
        log[i] = {}
        #Stats
        for e in ["Level", "Health", "Damage", "Defense", "Experience"]:
            Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + int(dictionary["Properties"]["Enemy"][e]["Offset"], 16)))
            log[i][e] = int.from_bytes(Manager.rom.read(dictionary["Properties"]["Enemy"][e]["Length"]), "little")
            if log[i][e] > (0x100**dictionary["Properties"]["Enemy"][e]["Length"]/2) - 1:
                log[i][e] -= 0x100**dictionary["Properties"]["Enemy"][e]["Length"]
        #Resistances
        log[i]["Resistances"] = {}
        for e in attributes:
            log[i]["Resistances"][e] = 1
        Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + int(dictionary["Properties"]["Enemy"]["Weak"]["Offset"], 16)))
        total = int.from_bytes(Manager.rom.read(dictionary["Properties"]["Enemy"]["Weak"]["Length"]), "little")
        for e in attributes:
            if (total & attributes[e]) != 0:
                log[i]["Resistances"][e] = 0
        Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + int(dictionary["Properties"]["Enemy"]["Strong"]["Offset"], 16)))
        total = int.from_bytes(Manager.rom.read(dictionary["Properties"]["Enemy"]["Strong"]["Length"]), "little")
        for e in attributes:
            if (total & attributes[e]) != 0:
                log[i]["Resistances"][e] = 2
        Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + int(dictionary["Properties"]["Enemy"]["Immune"]["Offset"], 16)))
        total = int.from_bytes(Manager.rom.read(dictionary["Properties"]["Enemy"]["Immune"]["Length"]), "little")
        for e in attributes:
            if (total & attributes[e]) != 0:
                log[i]["Resistances"][e] = 3
        Manager.rom.seek(check_offset(int(offsets["Enemy"][i]["EnemyAddress"], 16) + int(dictionary["Properties"]["Enemy"]["Absorb"]["Offset"], 16)))
        total = int.from_bytes(Manager.rom.read(dictionary["Properties"]["Enemy"]["Absorb"]["Length"]), "little")
        for e in attributes:
            if (total & attributes[e]) != 0:
                log[i]["Resistances"][e] = 4
        #Attack damage
        log[i]["AttackDamage"] = []
        for e in offsets["Enemy"][i]["AttackAddress"]:
            Manager.rom.seek(check_offset(int(e, 16) + int(dictionary["Properties"]["Enemy"]["Damage"]["Offset"], 16)))
            damage = int.from_bytes(Manager.rom.read(2), "little")
            if damage > (0x100**dictionary["Properties"]["Enemy"]["Damage"]["Length"]/2) - 1:
                damage -= 0x100**dictionary["Properties"]["Enemy"]["Damage"]["Length"]
            log[i]["AttackDamage"].append(damage)
    
    with open("SpoilerLog\\Enemy.json", "w") as file_writer:
        file_writer.write(json.dumps(log, indent=2))
