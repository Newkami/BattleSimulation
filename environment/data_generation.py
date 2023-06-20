import pandas as pd
import numpy as np
import os
from environment.enemy import *
from config import DATA_PATH

EASY_MV_ABILITY = 1
MEDIUM_MV_ABILITY = 2
HARD_MV_ABILITY = 3

EASY_MV_ATK_RANGE = 3
MEDIUM_MV_ATK_RANGE = 4
HARD_MV_ATK_RANGE = 5

EASY_RD_DTC_RADIUS = 3
MEDIUM_RD_DTC_RADIUS = 4
HARD_RD_DTC_RADIUS = 5

EASY_AT_DFD_RADIUS = 4
MEDIUM_AT_DFD_RADIUS = 6
HARD_AT_DFD_RADIUS = 8

EASY_JM_ATK_RANGE = 4
MEDIUM_JM_ATK_RANGE = 6
HARD_JM_ATK_RANGE = 8

EASY_AT_DFD_COEF = 0.3
MEDIUM_AT_DFD_COEF = 0.4
HARD_JM_AT_DFD_COEF = 0.6


class Task_Generator:
    def __init__(self):
        self.jammer_df = pd.read_excel(os.path.join(DATA_PATH, 'Jammer.xlsx'))
        self.missilevehicle_df = pd.read_excel(os.path.join(DATA_PATH, 'MissileVehicle.xlsx'))
        self.radar_df = pd.read_excel(os.path.join(DATA_PATH, 'Radar.xlsx'))
        self.antiAirturrent_df = pd.read_excel(os.path.join(DATA_PATH, 'AntiAircraftTurrent.xlsx'))
        self.commandpost_df = pd.read_excel(os.path.join(DATA_PATH, 'Commandpost.xlsx'))

    def generate_task(self, args):

        assert args.difficulty in [0, 1, 2, 3], \
            f"difficulty is invalid, invalid value = {args.difficulty}, the avail options are [0,1,2,3]"
        if args.difficulty == 0:
            self.jammer_df = self.jammer_df[self.jammer_df['difficulty'] == 0].sample(args.n_jammer)
            self.missilevehicle_df = self.missilevehicle_df[self.missilevehicle_df['difficulty'] == 0].sample(
                args.n_missilevehicle)
            self.radar_df = self.radar_df[self.radar_df['difficulty'] == 0].sample(args.n_radar)
            self.antiAirturrent_df = self.antiAirturrent_df[self.antiAirturrent_df['difficulty'] == 0].sample(
                args.n_antiAirturrent)
            args.mv_strike_ability = EASY_MV_ABILITY
            args.mv_attack_range = EASY_MV_ATK_RANGE
            args.detect_radius = EASY_RD_DTC_RADIUS
            args.defend_radius = EASY_AT_DFD_RADIUS
            args.jm_attack_range = EASY_JM_ATK_RANGE
            args.defend_coef = EASY_AT_DFD_COEF

        elif args.difficulty == 1:
            self.jammer_df = self.jammer_df[self.jammer_df['difficulty'] == 1].sample(args.n_jammer)
            self.missilevehicle_df = self.missilevehicle_df[self.missilevehicle_df['difficulty'] == 1].sample(
                args.n_missilevehicle)
            self.radar_df = self.radar_df[self.radar_df['difficulty'] == 1].sample(args.n_radar)
            self.antiAirturrent_df = self.antiAirturrent_df[self.antiAirturrent_df['difficulty'] == 1].sample(
                args.n_antiAirturrent)
            args.mv_strike_ability = MEDIUM_MV_ABILITY
            args.mv_attack_range = MEDIUM_MV_ATK_RANGE
            args.detect_radius = MEDIUM_RD_DTC_RADIUS
            args.defend_radius = MEDIUM_AT_DFD_RADIUS
            args.jm_attack_range = MEDIUM_JM_ATK_RANGE
            args.defend_coef = MEDIUM_AT_DFD_COEF

        elif args.difficulty == 2:
            self.jammer_df = self.jammer_df[self.jammer_df['difficulty'] == 2].sample(args.n_jammer)
            self.missilevehicle_df = self.missilevehicle_df[self.missilevehicle_df['difficulty'] == 2].sample(
                args.n_missilevehicle)
            self.radar_df = self.radar_df[self.radar_df['difficulty'] == 2].sample(args.n_radar)
            self.antiAirturrent_df = self.antiAirturrent_df[self.antiAirturrent_df['difficulty'] == 2].sample(
                args.n_antiAirturrent)
            args.mv_strike_ability = HARD_MV_ABILITY
            args.mv_attack_range = HARD_MV_ATK_RANGE
            args.detect_radius = HARD_RD_DTC_RADIUS
            args.defend_radius = HARD_AT_DFD_RADIUS
            args.jm_attack_range = HARD_JM_ATK_RANGE
            args.defend_coef = HARD_JM_AT_DFD_COEF

        else:
            """
             支持目标数量的自定义，难度自定义
             其中mv_strike_ability mv_attack_range detect_radius defend_radius defend_coef使用arguments的默认值
            """
            from config import TASK_CONFIG  # 读取配置信息
            commandpost = self.custom_task_aux2(TASK_CONFIG, args)

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
        if args.difficulty != 3:
            commandpost = CommandPost("CommandPost", args.mapX - 2, args.mapY - 2, idx, args)
        # SECTION:返回四种目标的集合 和一个指挥所
        return jammers, missile_vehicles, radars, antiAirturrents, commandpost

    # 新版不读取表格数据 目标位置 随机生成
    def custom_task_aux2(self, config, args):
        total_num = config['total_num']
        jm_num_e = config['jammers']['easy']
        jm_num_m = config['jammers']['medium']
        jm_num_h = config['jammers']['hard']
        jm_num = jm_num_e + jm_num_m + jm_num_h
        mv_num_e = config['missile_vehicles']['easy']
        mv_num_m = config['missile_vehicles']['medium']
        mv_num_h = config['missile_vehicles']['hard']
        mv_num = mv_num_e + mv_num_m + mv_num_h
        # 雷达
        rd_num_e = config['radars']['easy']
        rd_num_m = config['radars']['medium']
        rd_num_h = config['radars']['hard']
        rd_num = rd_num_e + rd_num_m + rd_num_h
        aat_num_e = config['antiairturrents']['easy']
        aat_num_m = config['antiairturrents']['medium']
        aat_num_h = config['antiairturrents']['hard']
        aat_num = aat_num_e + aat_num_m + aat_num_h
        assert total_num == rd_num + aat_num + mv_num + jm_num, "error total_num is different from other target"
        init_x = config['init_commandpost_x']
        init_y = config['init_commandpost_y']
        commandpost = CommandPost("CommandPost", init_x, init_y, total_num, args)
        # 获取5圈的可选范围
        options = utils.get_MatrixWithNoObjs(init_x, init_y, np.zeros((args.mapX, args.mapY), dtype=int), 5)
        # todo 完成只选择该点范围内 左边和下方的点 并不选择该目标点后方的点
        actual_positons = random.sample(options, total_num)
        return commandpost

    # 旧版custom_task 实验数据还是从表格中读取
    def custom_task_aux(self, config, args):
        total_num = config['total_num']
        jm_num_e = config['jammers']['easy']
        jm_num_m = config['jammers']['medium']
        jm_num_h = config['jammers']['hard']
        jm_num = jm_num_e + jm_num_m + jm_num_h
        mv_num_e = config['missile_vehicles']['easy']
        mv_num_m = config['missile_vehicles']['medium']
        mv_num_h = config['missile_vehicles']['hard']
        mv_num = mv_num_e + mv_num_m + mv_num_h
        # 雷达
        rd_num_e = config['radars']['easy']
        rd_num_m = config['radars']['medium']
        rd_num_h = config['radars']['hard']
        rd_num = rd_num_e + rd_num_m + rd_num_h
        aat_num_e = config['antiairturrents']['easy']
        aat_num_m = config['antiairturrents']['medium']
        aat_num_h = config['antiairturrents']['hard']
        aat_num = aat_num_e + aat_num_m + aat_num_h

        assert total_num == rd_num + aat_num + mv_num + jm_num, "error total_num is different from other target"

        assert jm_num_e >= 0 and jm_num_e <= 5, "easy jammer num must be in [0-5]"
        assert jm_num_m >= 0 and jm_num_m <= 3, "medium jammer num must be in [0-3]"
        assert jm_num_h >= 0 and jm_num_h <= 2, "hard jammer num must be in [0-2]"
        args.n_jammers = jm_num

        assert mv_num_e >= 0 and mv_num_e <= 10, "easy missilevehicle num must be in [0-10]"
        assert mv_num_m >= 0 and mv_num_m <= 6, "medium missilevehicle num must be in [0-6]"
        assert mv_num_h >= 0 and mv_num_h <= 4, "hard missilevehicle num must be in [0-4]"
        args.n_missilevehicle = mv_num

        assert rd_num_e >= 0 and rd_num_e <= 10, "easy radar num must be in [0-10]"
        assert rd_num_m >= 0 and rd_num_m <= 6, "medium radar num must be in [0-6]"
        assert rd_num_h >= 0 and rd_num_h <= 4, "hard radar num must be in [0-4]"
        args.n_radar = rd_num

        assert aat_num_e >= 0 and aat_num_e <= 10, "easy antiAirturrents num must be in [0-10]"
        assert aat_num_m >= 0 and aat_num_m <= 6, "medium antiAirturrents num must be in [0-6]"
        assert aat_num_h >= 0 and aat_num_h <= 4, "hard antiAirturrents num must be in [0-4]"
        args.n_antiAirturrent = aat_num

        # 生成df
        # id	HP	pos_x	pos_y	strike_ability	idx_value	difficulty
        jm_df = pd.DataFrame(columns=["id", "HP", "pos_x", "pos_y", "strike_ability", "idx_value", "difficulty"])
        if jm_num_e > 0:
            df_e = self.jammer_df[self.jammer_df['difficulty'] == 0].sample(jm_num_e)
            jm_df = pd.concat([jm_df, df_e])
        if jm_num_m > 0:
            df_m = self.jammer_df[self.jammer_df['difficulty'] == 1].sample(jm_num_m)
            jm_df = pd.concat([jm_df, df_m])
        if jm_num_h > 0:
            df_h = self.jammer_df[self.jammer_df['difficulty'] == 2].sample(jm_num_h)
            jm_df = pd.concat([jm_df, df_h])
        self.jammer_df = jm_df

        mv_df = pd.DataFrame(columns=["id", "HP", "pos_x", "pos_y", "strike_army", "idx_value", "difficulty"])
        if mv_num_e > 0:
            df_e = self.missilevehicle_df[self.missilevehicle_df['difficulty'] == 0].sample(mv_num_e)
            mv_df = pd.concat([mv_df, df_e])
        if mv_num_m > 0:
            df_m = self.missilevehicle_df[self.missilevehicle_df['difficulty'] == 1].sample(mv_num_m)
            mv_df = pd.concat([mv_df, df_m])
        if mv_num_h > 0:
            df_h = self.missilevehicle_df[self.missilevehicle_df['difficulty'] == 2].sample(mv_num_h)
            mv_df = pd.concat([mv_df, df_h])
        self.missilevehicle_df = mv_df

        rd_df = pd.DataFrame(columns=["id", "HP", "pos_x", "pos_y", "detection_radius", "idx_value", "difficulty"])
        if jm_num_e > 0:
            df_e = self.radar_df[self.radar_df['difficulty'] == 0].sample(rd_num_e)
            rd_df = pd.concat([rd_df, df_e])
        if jm_num_m > 0:
            df_m = self.radar_df[self.radar_df['difficulty'] == 1].sample(rd_num_m)
            rd_df = pd.concat([rd_df, df_m])
        if jm_num_h > 0:
            df_h = self.radar_df[self.radar_df['difficulty'] == 2].sample(rd_num_h)
            rd_df = pd.concat([rd_df, df_h])
        self.radar_df = rd_df

        aat_df = pd.DataFrame(columns=["id", "pos_x", "pos_y", "idx_value", "difficulty"])
        if aat_num_e > 0:
            df_e = self.antiAirturrent_df[self.antiAirturrent_df['difficulty'] == 0].sample(aat_num_e)
            aat_df = pd.concat([aat_df, df_e])
        if aat_num_m > 0:
            df_m = self.antiAirturrent_df[self.antiAirturrent_df['difficulty'] == 1].sample(aat_num_m)
            aat_df = pd.concat([aat_df, df_m])
        if aat_num_h > 0:
            df_h = self.antiAirturrent_df[self.antiAirturrent_df['difficulty'] == 2].sample(aat_num_h)
            aat_df = pd.concat([aat_df, df_h])
        self.antiAirturrent_df = aat_df

        return True
        # todo: commandpost 就固定为1吧 没必要产生多个
