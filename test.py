from utils import Utils
from data import Data
from features import Features
from depth_charts import DepthCharts


# Data.get_pfr_fantasy_totals_df(aggregate=True, save=True)
# Utils.check_good_data_pfr()
# Features = Features()
# Features._get_position_stats()
# print(Features.add_value_over_position())
# Features.add_value_over_position()
# print(Features.get_features_df_by_pos("RB"))
# print(DepthCharts.get_depth_charts())
# DepthCharts.get_depth_charts().to_csv("meta_data/depthchart_example.csv")
# print(Features.team_name_dict)


Features = Features()
Features.add_value_over_position()
Features.add_depth()
Features.save_df()
print(Features.df)
