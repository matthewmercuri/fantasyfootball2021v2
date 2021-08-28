from data import Data


class DraftSim:
    def __init__(self, teams: int = 12, years_data: int = 2020):
        self.df = Data.get_pfr_fantasy_totals_df(years_data)
        self.number_of_teams = teams

    def run_sim():
        pass
