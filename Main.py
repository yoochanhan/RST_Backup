#Copyright (c) 2025 St. Mother Teresa HS All rights reserved.

# Created by: Mr. M
# Created on: Sep 2025
# This program displays, "Hello, World!"

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
    def status(self):
        status = (
            "you are" + self.name + "," + self.role + " has " + self.hp
            + "hp, " + self.mp + "mp, ")
    # introducing 
    def intro(self):
        pass
    def use_skill(self):
        response = client.responses.create(
        model="gpt-5-mini",
        input="intr"
    )
    def attack(self):
        pass


def generate_character():
    response = client.responses.create(
        model="gpt-5-nano",
        input="create a any character in a game and"\
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
