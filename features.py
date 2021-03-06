import pandas as pd

from data import Data
from depth_charts import DepthCharts
from players import Players


class Features:
    """Assembling a dataframe of all relevant features to draft or feed into ML"""

    VALID_POSITIONS = ["QB", "RB", "WR", "TE", "K", "DEF"]

    def __init__(self, draft_list_source: str = "SCORE"):
        self.base_df = Data.get_pfr_fantasy_totals_df()
        self.base_aggregate_df = Data.get_pfr_fantasy_totals_df(aggregate=True)
        self.draftees = Players.draft_eligible_players(draft_list_source)
        self.depth_df = DepthCharts.get_depth_charts()
        self.fp_df = self._get_fant_pros_df()
        self.team_name_dict = self._get_team_dict()

        self.df = self.draftees

    def _get_fant_pros_df(self):
        df = pd.read_csv("meta_data/FantasyPros_2021_Draft_ALL_Rankings.csv")
        df["PLAYER NAME"] = df["PLAYER NAME"].apply(lambda x: x.strip().upper())
        return df

    def _get_team_dict(self):
        _team_dict = pd.read_csv("meta_data/team_names.csv", index_col=0).to_dict(
            orient="index"
        )
        team_dict = {}
        for x in _team_dict:
            short = _team_dict[x]["SHORT"]
            team_dict[short] = x

        return team_dict

    def _get_player_fantptpergame(self, x):
        try:
            _value = self.base_df[self.base_df["Player"] == x["Player"]][
                "FantPtPerGame"
            ].iloc[0]
        except:
            _value = 0
        return _value

    def _add_value_over_position_cols(self, x, position_stats):
        position = x["Pos."].strip().upper()
        fppg = x["FantPtPerGame_2020"]

        if fppg != 0:
            return round(fppg - position_stats[position]["mean"], 2)
        else:
            return -1000

    def _add_position_factor_cols(self, x, position_stats):
        position = x["Pos."].strip().upper()
        vop = x["ValueOverPosition_2020"]
        factor = position_stats[position]["factor"]

        if vop != 0:
            return round(factor * vop, 2)
        else:
            return -1000

    def _add_depth_cols(self, x):
        position = x["Pos."].strip().upper()
        team = x["Team"].strip().upper()
        full_team = self.team_name_dict[team]

        if position != "WR":
            depth_row = self.depth_df[position].loc[full_team]
            for count, player in enumerate(depth_row):
                if player == x["Player"]:
                    return f"{position}{count+1}"

        else:
            lwr_depth_row = self.depth_df["LWR"].loc[full_team]
            for count, player in enumerate(lwr_depth_row):
                if player == x["Player"]:
                    return f"{'LWR'}{count+1}"
            rwr_depth_row = self.depth_df["RWR"].loc[full_team]
            for count, player in enumerate(rwr_depth_row):
                if player == x["Player"]:
                    return f"{'RWR'}{count+1}"
            swr_depth_row = self.depth_df["SWR"].loc[full_team]
            for count, player in enumerate(swr_depth_row):
                if player == x["Player"]:
                    return f"{'SWR'}{count+1}"

    def _add_fantasy_pros_rank_col(self, x):
        player = x["Player"]
        df = self.fp_df[self.fp_df["PLAYER NAME"] == player]
        values = list(df["RK"].values)

        if len(values) != 0:
            return values[0]
        else:
            return ""

    def _add_fantasy_pros_posrank_col(self, x):
        player = x["Player"]
        df = self.fp_df[self.fp_df["PLAYER NAME"] == player]
        values = list(df["POS"].values)

        if len(values) != 0:
            return values[0]
        else:
            return ""

    def _get_position_stats(self):
        position_stats = {}

        qbs = self.base_aggregate_df[self.base_aggregate_df["FantPos"] == "QB"]
        rbs = self.base_aggregate_df[self.base_aggregate_df["FantPos"] == "RB"]
        wrs = self.base_aggregate_df[self.base_aggregate_df["FantPos"] == "WR"]
        tes = self.base_aggregate_df[self.base_aggregate_df["FantPos"] == "TE"]

        position_stats["QB"] = {
            "mean": qbs["FantPtPerGame"].mean(),
            "median": qbs["FantPtPerGame"].median(),
            "std": qbs["FantPtPerGame"].std(),
        }

        position_stats["RB"] = {
            "mean": rbs["FantPtPerGame"].mean(),
            "median": rbs["FantPtPerGame"].median(),
            "std": rbs["FantPtPerGame"].std(),
        }

        position_stats["WR"] = {
            "mean": wrs["FantPtPerGame"].mean(),
            "median": wrs["FantPtPerGame"].median(),
            "std": wrs["FantPtPerGame"].std(),
        }

        position_stats["TE"] = {
            "mean": tes["FantPtPerGame"].mean(),
            "median": tes["FantPtPerGame"].median(),
            "std": tes["FantPtPerGame"].std(),
        }

        position_stats["QB"]["factor"] = (
            (position_stats["QB"]["std"] / position_stats["QB"]["mean"]) ** 2
        ) + 1

        position_stats["RB"]["factor"] = (
            (position_stats["RB"]["std"] / position_stats["RB"]["mean"]) ** 2
        ) + 1

        position_stats["TE"]["factor"] = (
            (position_stats["TE"]["std"] / position_stats["TE"]["mean"]) ** 2
        ) + 1
        position_stats["WR"]["factor"] = (
            (position_stats["WR"]["std"] / position_stats["WR"]["mean"]) ** 2
        ) + 1

        return position_stats

    def add_value_over_position(self):
        position_stats = self._get_position_stats()

        self.df["FantPtPerGame_2020"] = self.df.apply(
            self._get_player_fantptpergame, axis=1
        )
        self.df["ValueOverPosition_2020"] = self.df.apply(
            self._add_value_over_position_cols, axis=1, position_stats=position_stats
        )
        self.df["VOP_2020_WithFactor"] = self.df.apply(
            self._add_position_factor_cols, axis=1, position_stats=position_stats
        )

        return self.df

    def add_depth(self):
        self.df["Depth"] = self.df.apply(self._add_depth_cols, axis=1)
        return self.df

    def add_fantasy_pros(self):
        self.df["FP_Pos_Rank"] = self.df.apply(
            self._add_fantasy_pros_posrank_col, axis=1
        )

        self.df["FP_OVR_Rank"] = self.df.apply(self._add_fantasy_pros_rank_col, axis=1)
        return self.df

    def save_df(self):
        self.df.to_csv("data/features.csv")

    def get_features_df_by_pos(self, position: str) -> pd.DataFrame:
        position = position.strip().upper()
        if position not in self.VALID_POSITIONS:
            raise NameError(f"{position} is not a valid position")

        return self.df[self.df["Pos."] == position]
