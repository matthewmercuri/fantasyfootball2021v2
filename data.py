from bs4 import BeautifulSoup
import requests
from typing import Union, Tuple


class Data:
    FANTASY_BASE_URL = "https://www.pro-football-reference.com/years/"
    VALID_POSITIONS = ["QB", "RB", "WR", "TE", "K"]

    @classmethod
    def get_pfr_fantasy_totals_df(cls, year: str = "2020"):
        pass

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
