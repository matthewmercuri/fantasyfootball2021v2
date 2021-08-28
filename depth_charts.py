import pandas as pd
from bs4 import BeautifulSoup
import requests


class DepthCharts:

    URL = "https://fantasydata.com/nfl/depth-charts"

    @classmethod
    def get_depth_charts(cls):
        NEEDED_COLUMNS = ["QB", "LWR", "RWR", "SWR", "RB", "TE", "K"]

        r = requests.get(cls.URL)
        soup = BeautifulSoup(r.text, "lxml")
        depth_charts = soup.find_all("div", "depth-col")

        team_names_raw = [x.find("a", "team-link") for x in depth_charts]
        team_names = [x.text.strip().upper() for x in team_names_raw]

        team_data = {}
        for count, depth_chart in enumerate(depth_charts):
            positon_select = depth_chart.find_all("div", "depth-pos")

            position_data = {}
            for position in positon_select:
                players_raw = position.find_all("a")
                players = [x.text.strip().upper() for x in players_raw]

                position = position.find("div", "pos-name").text.strip().upper()
                position_data[position] = players

            team_data[team_names[count]] = position_data

        df = pd.DataFrame.from_dict(team_data, orient="index")
        df = df[NEEDED_COLUMNS]

        return df


DepthCharts.get_depth_charts()
