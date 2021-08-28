import pandas as pd

from data import Data
from players import Players


class Features:
    """Assembling a dataframe of all relevant features to draft or feed into ML"""

    def __init__(self, draft_list_source: str = "SCORE"):
        self.base_df = Data.get_pfr_fantasy_totals_df()
        self.base_aggregate_df = Data.get_pfr_fantasy_totals_df(aggregate=True)
        self.draftees = Players.draft_eligible_players(draft_list_source)

        self.df = self.draftees

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

    def _get_positio_stats(self):
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

        return position_stats

    def add_value_over_position(self):
        position_stats = self._get_positio_stats()

        self.df["FantPtPerGame_2020"] = self.df.apply(
            self._get_player_fantptpergame, axis=1
        )
        self.df["ValueOverPosition_2020"] = self.df.apply(
            self._add_value_over_position_cols, axis=1, position_stats=position_stats
        )

        return self.df
