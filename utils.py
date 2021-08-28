import pandas as pd

from data import Data
from players import Players


class Utils:
    @staticmethod
    def check_good_data_pfr():
        data_df = Data.get_pfr_fantasy_totals_df()
        players_with_data = data_df["Player"].tolist()

        draft_df = Players.draft_eligible_players()
        draftees = draft_df["Player"].tolist()

        no_data = []
        for draftee in draftees:
            if draftee not in players_with_data:
                no_data.append(draftee)

        print(no_data)

        return no_data
