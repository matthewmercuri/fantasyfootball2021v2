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
            name_overrides = {
                "ALLEN ROBINSON II": "ALLEN ROBINSON",
                "PATRICK MAHOMES II": "PATRICK MAHOMES",
                "WILL FULLER V": "WILL FULLER",
                "MARVIN JONES JR.": "MARVIN JONES",
                "D.J. CHARK JR.": "DJ CHARK",
                "MELVIN GORDON III": "MELVIN GORDON",
                "TONY JONES JR.": "TONY JONES",
            }
            df["Player"] = df["Player"].replace(name_overrides)

            df.rename(columns={"Rk": "Score_Rank"}, inplace=True)

        else:
            raise ValueError(f"{source} is not a valid source.")

        return df
