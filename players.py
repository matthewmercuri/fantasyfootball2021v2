from data import Data

import pandas as pd


class Players:
    @classmethod
    def _pfr_players(cls) -> pd.DataFrame:
        data_dict, errors = Data.get_pfr_players_meta_dict()
        df = pd.DataFrame.from_dict(data_dict, orient="index")
        return df

    @classmethod
    def get_players_meta_df(cls, source: str = "PFR") -> pd.DataFrame:
        source = source.strip().upper()

        if source == "PFR":
            return cls._pfr_players()
        else:
            raise ValueError(f"{source} is not a valid source.")

    @classmethod
    def draft_eligible_players(cls, source: str = "SCORE") -> pd.DataFrame:
        """returns a dataframe of draft eligibles sorted by the source's rank opinion"""
        source = source.strip().upper()

        if source == "SCORE":
            df = pd.read_csv("meta_data/2021draftees_thescore.csv")
            df["Player"] = df["Player"].apply(lambda x: x.strip().upper())
        else:
            raise ValueError(f"{source} is not a valid source.")

        return df
