import pandas as pd
import numpy as np
import os
from environment.enemy import *


class Task_Generator:
    def __init__(self):
        self.jammer_df = pd.read_excel('../../data/Jammer.xlsx')
        self.missilevehicle_df = pd.read_excel('../../data/MissileVehicle.xlsx')
        self.radar_df = pd.read_excel('../../data/Radar.xlsx')
        self.antiAirturrent_df = pd.read_excel('../../data/AntiAircraftTurrent.xlsx')
        self.commandpost_df = pd.read_excel('../../data/Commandpost.xlsx')

    def generate_task(self, args):
        assert args.difficulty in [0, 1, 2], "difficulty is invalid"
        if args.difficulty == 0:
            self.jammer_df = self.jammer_df[self.jammer_df['difficulty'] == 0].sample(args.n_jammer)
            self.missilevehicle_df = self.missilevehicle_df[self.missilevehicle_df['difficulty'] == 0].sample(
                args.n_missilevehicle)
            self.radar_df = self.radar_df[self.radar_df['difficulty'] == 0].sample(args.n_radar)
            self.antiAirturrent_df = self.antiAirturrent_df[self.antiAirturrent_df['difficulty'] == 0].sample(
                args.n_antiAirturrent)

        elif args.difficulty == 1:
            self.jammer_df = self.jammer_df[self.jammer_df['difficulty'] == 1].sample(args.n_jammer)
            self.missilevehicle_df = self.missilevehicle_df[self.missilevehicle_df['difficulty'] == 1].sample(
                args.n_missilevehicle)
            self.radar_df = self.radar_df[self.radar_df['difficulty'] == 1].sample(args.n_radar)
            self.antiAirturrent_df = self.antiAirturrent_df[self.antiAirturrent_df['difficulty'] == 1].sample(
                args.n_antiAirturrent)
            args.mv_strike_ability = 2
            args.detect_radius = 4
            args.defend_radius = 6
            args.defend_coef = 0.4

        elif args.difficulty == 2:
            self.jammer_df = self.jammer_df[self.jammer_df['difficulty'] == 2].sample(args.n_jammer)
            self.missilevehicle_df = self.missilevehicle_df[self.missilevehicle_df['difficulty'] == 2].sample(
                args.n_missilevehicle)
            self.radar_df = self.radar_df[self.radar_df['difficulty'] == 2].sample(args.n_radar)
            self.antiAirturrent_df = self.antiAirturrent_df[self.antiAirturrent_df['difficulty'] == 2].sample(
                args.n_antiAirturrent)
            args.mv_strike_ability = 3
            args.detect_radius = 5
            args.defend_radius = 8
            args.defend_coef = 0.6

        # 坐标四舍五入处理 fixme:坐标值其实最好不要出现小数点 那么直接设置为int类型即可
        self.jammer_df['pos_x'] = np.round(self.jammer_df['pos_x'], 0).astype(int)
        self.jammer_df['pos_y'] = np.round(self.jammer_df['pos_y'], 0).astype(int)
        self.missilevehicle_df['pos_x'] = np.round(self.missilevehicle_df['pos_x'], 0).astype(int)
        self.missilevehicle_df['pos_y'] = np.round(self.missilevehicle_df['pos_y'], 0).astype(int)
        self.radar_df['pos_x'] = np.round(self.radar_df['pos_x'], 0).astype(int)
        self.radar_df['pos_y'] = np.round(self.radar_df['pos_y'], 0).astype(int)
        self.antiAirturrent_df['pos_x'] = np.round(self.antiAirturrent_df['pos_x'], 0).astype(int)
        self.antiAirturrent_df['pos_y'] = np.round(self.antiAirturrent_df['pos_y'], 0).astype(int)

        jammers = []
        missile_vehicles = []
        radars = []
        antiAirturrents = []

        idx = 1
        for _, row in self.jammer_df.iterrows():
            jammers.append(
                Jammer(row['id'], row['pos_x'], row['pos_y'], idx, args)
            )
            idx += 1
        for _, row in self.missilevehicle_df.iterrows():
            missile_vehicles.append(
                MissileVehicle(row['id'], row['pos_x'], row['pos_y'], idx, args)
            )
            idx += 1
        for _, row in self.radar_df.iterrows():
            radars.append(
                Radar(row['id'], row['pos_x'], row['pos_y'], idx, args)
            )
            idx += 1
        for _, row in self.antiAirturrent_df.iterrows():
            antiAirturrents.append(
                AntiAircraftTurret(row['id'], row['pos_x'], row['pos_y'], idx, args)
            )
            idx += 1
        commandpost = CommandPost("CommandPost", args.mapX - 2, args.mapY - 2, idx, args)
        # SECTION:返回四种目标的集合 和一个指挥所
        return jammers, missile_vehicles, radars, antiAirturrents, commandpost
