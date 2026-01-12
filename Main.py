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
battle_log=[]
class equiment():
    pass
class entity():
    def __init__(
        self, get_name, get_role,get_hp, get_atk, get_mp, get_df, get_dscpt
        ):
        self.name = get_name
        self.role = get_role
        self.hp = get_hp
        self.atk = get_atk
        self.mp = get_mp
        self.df = get_df
        self.description = get_dscpt
    # introducing for developing
    def intro_dev(self):
        print(
            f"{self.name}, {self.role}, {self.hp}", 
            f"{self.atk}, {self.mp}, {self.df}, {self.description}"
            )
    def status_now(self):
        stats = ""
        stats = (
            "you are" + str(self.name) + "," + str(self.role) + " has " + str(self.hp)
            + "hp, " + str(self.mp) + "mp, " + str(self.df) + "df.")
        return str(stats)
    # introducing
    def intro(self):
        pass
    def use_skill(self):
        stats = status_now()
        response = client.responses.create(
        model="gpt-5-mini",
        input=(stats + "")
    )
    def attack(self):
        pass


def generate_character():
    response = client.responses.create(
        model="gpt-5-nano",
        input="create a any uselese character in a game and"\
                "write character's name, role, hp(100-2000), atk(30-230),"\
                "mp(10-400), df(5-100), short description."\
                "your response should contain only values and"\
                "each sections should"\
                "divided by ','"
    )
    print(type(response))
    # response2str = str(response)
    print(type(response.output_text.strip()))
    return response.output_text.strip()

generate_character()
name1, role1, hp1, atk1, mp1, df1, dscpt1 = generate_character().split(",")
entity1 = entity(name1, role1, int(hp1), int(atk1), int(mp1), int(df1), dscpt1)
# entity1.intro_dev()

name2, role2, hp2, atk2, mp2, df2, dscpt2 = generate_character().split(",")
entity2 = entity(name2, role2, int(hp2), int(atk2), int(mp2), int(df2), dscpt2)
# entity2.intro_dev()

# Simulate start
while 0:

    entity1.use_skill()
