from features import Features

"""saves all necessary dataframes for draft"""

Features = Features()
Features.add_value_over_position()
Features.add_depth()
Features.add_fantasy_pros()

Features.df.to_csv("draftkit/rankings.csv")
Features.get_features_df_by_pos("QB").to_csv("draftkit/QBrankings.csv")
Features.get_features_df_by_pos("RB").to_csv("draftkit/RBrankings.csv")
Features.get_features_df_by_pos("WR").to_csv("draftkit/WRrankings.csv")
Features.get_features_df_by_pos("TE").to_csv("draftkit/TErankings.csv")
