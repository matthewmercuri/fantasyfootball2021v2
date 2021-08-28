from bs4 import BeautifulSoup
import pandas as pd
import requests
from typing import Union, Tuple

pd.options.mode.chained_assignment = None


class Data:
    FANTASY_BASE_URL = "https://www.pro-football-reference.com/years/"
    VALID_POSITIONS = ["QB", "RB", "WR", "TE", "K"]
    VALID_YEARS = ["2020", "2019", "2018", "2017", "2016"]

    @classmethod
    def _clean_pfr_fantasy_totals_df(cls, df: pd.DataFrame) -> pd.DataFrame:

        df.columns = df.columns.to_flat_index()
        df.columns = ["_".join(x) for x in df.columns]

        for col in df.columns:
            if col[:3] == "Unn":
                df.rename(columns={col: col.split("_")[-1]}, inplace=True)

        df = df[df["Tm"] != "Tm"]

        df[df.columns[4:]] = df[df.columns[4:]].fillna(value=0)

        df["FantPos"] = df["FantPos"].fillna("NA")
        df["FantPos"] = df["FantPos"].apply(lambda x: str(x).upper())

        df["Player"] = df["Player"].apply(lambda x: x.replace("*", " "))
        df["Player"] = df["Player"].apply(lambda x: x.replace("+", " "))
        df["Player"] = df["Player"].apply(lambda x: x.strip().upper())

        types_dict = {
            "Player": str,
            "Tm": str,
            "FantPos": str,
            "Age": int,
            "Games_G": int,
            "Games_GS": int,
            "Passing_Cmp": float,
            "Passing_Att": int,
            "Passing_Yds": float,
            "Passing_TD": int,
            "Passing_Int": int,
            "Rushing_Att": int,
            "Rushing_Yds": float,
            "Rushing_Y/A": float,
            "Rushing_TD": float,
            "Receiving_Tgt": int,
            "Receiving_Rec": int,
            "Receiving_Yds": float,
            "Receiving_Y/R": float,
            "Receiving_TD": int,
            "Fumbles_Fmb": int,
            "Fumbles_FL": int,
            "Scoring_TD": int,
            "Scoring_2PM": int,
            "Scoring_2PP": int,
            "Fantasy_FantPt": float,
            "Fantasy_PPR": float,
            "Fantasy_DKPt": float,
            "Fantasy_FDPt": float,
            "Fantasy_VBD": float,
            "Fantasy_PosRank": int,
            "Fantasy_OvRank": int,
        }

        df = df.astype(types_dict)

        return df

    @classmethod
    def _add_pfr_fantasy_totals_df(
        cls, df: pd.DataFrame, year: str = None
    ) -> pd.DataFrame:
        df["FantPtPerGame"] = df["Fantasy_FantPt"] / df["Games_G"]
        df["FantPtPerGame"] = df["FantPtPerGame"].apply(lambda x: 0 if x > 30 else x)
        df["FantPtPerGame"] = df["FantPtPerGame"].apply(lambda x: 0 if x < 0 else x)

        if year is not None:
            df["Stat_Year"] = year
        return df

    @classmethod
    def get_pfr_fantasy_totals_df(
        cls, year: str = "2020", aggregate: bool = False
    ) -> pd.DataFrame:

        if aggregate is False:
            _df = pd.read_html(
                cls.FANTASY_BASE_URL + f"{year}/fantasy.htm", index_col=0
            )[0]
            df = cls._clean_pfr_fantasy_totals_df(_df)
            df = cls._add_pfr_fantasy_totals_df(df)
            return df
        else:
            dfs = []
            for _year in cls.VALID_YEARS:
                _df = pd.read_html(
                    cls.FANTASY_BASE_URL + f"{year}/fantasy.htm", index_col=0
                )[0]
                df = cls._clean_pfr_fantasy_totals_df(_df)
                df = cls._add_pfr_fantasy_totals_df(df, _year)
                dfs.append(df)

            df = pd.concat(dfs)
            return df

    @classmethod
    def get_pfr_players_meta_dict(
        cls, year: str = "2020"
    ) -> Union[dict, Tuple[dict, list]]:

        r = requests.get(cls.FANTASY_BASE_URL + f"{year}/fantasy.htm")
        soup = BeautifulSoup(r.text, "lxml")
        fantasy_table = soup.find("table", {"id": "fantasy"}).find("tbody")
        player_rows_raw = fantasy_table.find_all("tr")

        errors = []
        player_meta = {}
        for raw_player_row in player_rows_raw:
            try:
                player_position = (
                    raw_player_row.find("td", {"data-stat": "fantasy_pos"})
                    .text.strip()
                    .upper()
                )

                if player_position not in cls.VALID_POSITIONS:
                    player_position = "NA"

                player_anchor = raw_player_row.find("a")

                player_profile_link = player_anchor["href"].strip()

                player = player_anchor.text.replace("*", "").replace("+", "")
                player = player.strip().upper()

                player_meta[player] = {
                    "pfrProfile": player_profile_link,
                    "fantasyPosition": player_position,
                }
            except Exception as e:
                errors.append(e)

        return player_meta, errors
