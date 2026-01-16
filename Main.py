#Copyright (c) 2025 St. Mother Teresa HS All rights reserved.

# Created by: Yoochan Han
# Created on: Jan 2026
# This program displays, "AI fighting simulation"

import os
import openai

# Load environment variables from .env file
# Assumes OPENAI_API_KEY is set as an environment variable
from openai import OpenAI
client = OpenAI()
battle_log=["Battle just begun! fight!!"]
turn = 0
class entity():
    def __init__(
        self, get_name, get_role,get_hp, get_atk, get_mp, get_df, get_dscpt
        ):
        self.name = get_name
        self.role = get_role
        self.hp = get_hp
        self.max_hp = get_hp
        self.atk = get_atk
        self.mp = get_mp
        self.max_mp = get_mp
        self.df = get_df
        self.description = get_dscpt

    def change_stats_hp(
        self, get_hp
        ):
        self.hp = get_hp
    # def change_stats_hp(
    #     self, get_hp
    #     ):
        # self.hp = get_hp
    def change_stats_mp(
        self, get_mp
        ):
        self.mp = get_mp

    # introducing for developing
    def intro_dev(self):
        print(
            f"{self.name}, {self.role}, {self.hp}", 
            f"{self.atk}, {self.mp}, {self.df}, {self.description}"
            )
    def status_now(self):
        stats = ""
        stats = (
            str(self.name) + "," + str(self.role) + " has " 
            + str(self.hp) + "/" + str(self.max_hp)
            + "hp, " + str(self.mp) + "/" + str(self.max_mp) + "mp, " 
            + str(self.df) + "df.")
        return str(stats)
    # introducing
    def intro(self):
        pass
    def use_skill(self, enemy_stats):
        opp_stats = enemy_stats
        stats = str(self.status_now())
        # Not completed yet
        response = client.responses.create(
            model="gpt-5-mini",
            input=("you are" + str(stats) + "and Your in situation:" + battle_log[turn]
            + "and enemy stat is " + opp_stats + "you can make and use a skill "
            + "and it might use mp or not, your choice. The answer format is"
            + "Name of Skill, damage(-200, 200), self_healing(-150, 100),"
            + "usage_mp(0, 100), effect&description(very shortly and it can't )"
            + "change enemy's stats like df and mp"
            + "and current situation. Skill don't have to contain every effects, "
            + "It could be only attack or heal what ever you want in boundary"
            + "also it could be very dumb like you can heal enemy to make "
            + "damage as negative number and self hurt to make self_healing"
            + "as negative number")
        )
        print(response)
        battle_log.append(response.output_text.strip())
        return response.output_text.strip()
    def effect_skill(self, skill_name, eft_dmg, dscpt):
        


    def generate_character():
        response = client.responses.create(
            model="gpt-5-mini",
            input="create a any uselese character in a game and"\
                    "write character's name, role, hp(100-2000), atk(30-230),"\
                    "mp(10-400), df(5-100), short description."\
                    "your response should contain only values and"\
                    "each sections should"\
                    "divided by ','"
        )
        # response2str = str(response)
        print(type(response.output_text.strip()))
        print("AI response(character)")
        print(response.output_text.strip())
        return response.output_text.strip()


#game start

generate_character()
name1, role1, hp1, atk1, mp1, df1, dscpt1 = generate_character().split(",")
entity1 = entity(name1, role1, int(hp1), int(atk1), int(mp1), int(df1), dscpt1)
# entity1.intro_dev()

name2, role2, hp2, atk2, mp2, df2, dscpt2 = generate_character().split(",")
entity2 = entity(name2, role2, int(hp2), int(atk2), int(mp2), int(df2), dscpt2)
# entity2.intro_dev()

# Simulate start
while 1:
    # TODO hungry <-- doesn't have meaning, plz change b4 summit to teacher
    skill_status1 = entity1.use_skill(entity2.status_now())
    skill_name1, eft_dmg1, eft_mp1, dscpt1 = skill_status1.split(",")

    skill_status2 = entity2.use_skill(entity1.status_now())
    # "Name of Skill, damage, self_healing, usage_mp, effect description
    skill_name1, eft_dmg1, eft_mp1, dscpt1 = skill_status1.split(",")
    print("battle log")
    print(battle_log)
    break
