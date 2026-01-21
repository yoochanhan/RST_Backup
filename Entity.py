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
class Entity():
    """Character's initial status setter"""
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
        """Change character's HP by character's healing skill"""
        self.hp += int(get_hp)
    # def change_stats_hp(
    #     self, get_hp
    #     ):
        # self.hp = get_hp
    def change_stats_mp(
        self, get_mp
        ):
        """Change character's MP by character's usage mp"""
        self.mp -= int(get_mp)
        if self.mp < 0:
            self.mp = 0
        if self.max_mp < self.mp:
            self.mp = self.max_mp

    def status_now(self):
        """Change character's HP by taken damage / character's df"""
        stats = ""
        stats = (
            str(self.name) + "," + str(self.role) + " has " 
            + str(self.hp) + "/" + str(self.max_hp)
            + "hp, " + str(self.mp) + "/" + str(self.max_mp) + "mp, " 
            + str(self.df) + "df.")
        return str(stats)

    def use_skill(self, enemy_stats, battle_log):
        """generate Skill by AI based on charcter'current situation"""
        opp_stats = enemy_stats
        stats = str(self.status_now())
        response = client.responses.create(
            model="gpt-5-mini",
            input=("you are" + str(stats) + "and Your in situation:" + battle_log
            + "and enemy stat is " + opp_stats + "you can make and use a skill "
            + "and it might use mp or not, your choice. The answer format is"
            + "Name of Skill, damage(-200, 400), self_healing(-150, 100),"
            + "usage_mp(0, 100), effect&description(very shortly and it can't )"
            + "change enemy's stats like df and mp"
            + "and current situation. Skill don't have to contain every effects, "
            + "It could be only attack or heal what ever you want in boundary"
            + "also it could be very dumb like you can heal enemy to make "
            + "damage as negative number and self hurt to make self_healing"
            + "as negative number. If MP <= 0, skill should"
            + "recharge MP with damage(0), self_healing(0), usage_mp(-1, -100)"
            + ", effect&description(very shortly and it can't )"
            + "your response should contain only values(in number exept name)"\
            + " and each sections should divided by ','"
            )
        )
        return response.output_text.strip()
    def effect_skill(self, eft_dmg):
        """Change character's HP by taken damage / character's df"""
        self.hp -= (int(eft_dmg)/self.df)
    
    
    def print_status(self):
        """print Character's present status"""
        print(
        f"{self.name}, {self.role} \nHP: {int(self.hp)}/{self.max_hp}"
        f"MP: {self.mp}/{self.max_mp}"
        )
    def get_df(self):
        """Return character's current df status"""
        return self.df

    def is_hp_zero(self):
        """Checking Character dead"""
        if self.hp <= 0:
            """print defeat line"""
            stats = str(self.status_now())
            response = client.responses.create(
                model="gpt-5-mini",
                input=("you are" + str(stats) + "and you are just defeate by enemy"
                + ", so leave your final mesage to enemy")
                )
            response.output_text.strip()
            return 1 #  yes
        else:
            return 0 # No
