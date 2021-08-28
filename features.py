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

    def add_value_over_position(self):
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

        position_stats["WRS"] = {
            "mean": wrs["FantPtPerGame"].mean(),
            "median": wrs["FantPtPerGame"].median(),
            "std": wrs["FantPtPerGame"].std(),
        }

        position_stats["TE"] = {
            "mean": tes["FantPtPerGame"].mean(),
            "median": tes["FantPtPerGame"].median(),
            "std": tes["FantPtPerGame"].std(),
        }

        print(position_stats)

        return self.df
