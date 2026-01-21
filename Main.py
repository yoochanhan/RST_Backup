#Copyright (c) 2025 St. Mother Teresa HS All rights reserved.

# Created by: Yoochan Han
# Created on: Jan 2026# This program displays, "AI fighting simulation"
import os
import openai
from Entity import Entity
from openai import OpenAI

client = OpenAI()
battle_log=["Battle just begun! fight!!"]
turn = 1

def generate_character():
    response = client.responses.create(
        model="gpt-5-mini",
        input="create a funny uselese character in a game and"\
        "write character's name, role, hp(100-2000), atk(30-280),"\
        "mp(20-400), df(1-3), short description."\
        "your response should contain only values and"\
        "each sections should"\
        "divided by ','"
        )
    # response2str = str(response)
    # print(type(response.output_text.strip()))
    print("AI response(character)")
    print(response.output_text.strip())
    return response.output_text.strip()



name1, role1, hp1, atk1, mp1, df1, dscpt1 = generate_character().split(",")
entity1 = Entity(name1, role1, int(hp1), int(atk1), int(mp1), int(df1), dscpt1)
# entity1.intro_dev()

name2, role2, hp2, atk2, mp2, df2, dscpt2 = generate_character().split(",")
entity2 = Entity(name2, role2, int(hp2), int(atk2), int(mp2), int(df2), dscpt2)
# entity2.intro_dev()

# Simulate start
while 1:
    # TODO hungry <-- doesn't have meaning, plz change b4 summit to teacher
    print(f"Turn# {turn}")

    entity1.print_status()
    skill_status1 = entity1.use_skill(entity2.status_now(), battle_log[-1])
    skill_name1, eft_dmg1, eft_heal1, eft_mp1, dscpt1 = skill_status1.split(",")
    #skill effects
    entity1.change_stats_hp(eft_heal1)  # heal
    entity1.change_stats_mp(eft_mp1)  # mp usage

    entity2.effect_skill(eft_dmg1)
    if entity2.is_hp_zero() == 1:
        break
    damage_taken = int(eft_dmg1)/int(entity2.get_df())
    battle_log.append(
        name1 + "used skill" + skill_name1 + ".\n"
        + name2 + " has been attacked!\n"
        + f" damage taken: {damage_taken} \nMeanwhile {name1} healed"
        + " hime/herself\nhp: " + eft_heal1 + " and used mp:" + eft_mp1 + '\n'
        )
    print(battle_log[-1])
    entity2.print_status()
    skill_status2 = entity2.use_skill(entity1.status_now(), battle_log[-1])
    # "Name of Skill, damage, self_healing, usage_mp, effect description
    skill_name2, eft_dmg2, eft_mp2, eft_heal2, dscpt2 = skill_status1.split(",")
    entity2.change_stats_hp(eft_heal2)  # heal
    entity2.change_stats_mp(eft_mp2)  # mp usage
    
    entity1.effect_skill(eft_dmg2)
    if entity1.is_hp_zero() == 1:
        break
    damage_taken = int(eft_dmg2)/int(entity1.get_df())
    battle_log.append(
        name2 + "used skill: " + skill_name2 + ".\n"
        + name1 + " has been attacked!\n"
        + f" damage taken: {damage_taken} \nMeanwhile " 
        + name2 + " healed"
        + " hime/herself\nhp: " + eft_heal2 + " and used mp:" + eft_mp2 + '\n'
        )
    print(battle_log[-1])
