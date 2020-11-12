### This function calculate sum of viewer of each game
import numpy as np 
import pandas as pd
import os

# This function calculate sum of viewer for each game
def get_GameViwer(path):
    # @path: directory of top_game_csv file
    
    #read data and add sum Game viewer at the end
    games = pd.read_csv(path)
    games['Total_Viewer'] = np.nan
    
    #sort games according to names
    games_sorted = games.sort_values('name')
    nb_of_game = len(games)
    path_of_streamer = os.path.join(os.path.dirname(path),'game_streams')
    streams = sorted(find_csv_filenames(path_of_streamer, suffix=".csv"))
    
    # calculate sum using loop
    total = []

    for i in range( nb_of_game):
        game = pd.read_csv(os.path.join(path_of_streamer,streams[i]))
        total_view = game['viewer_count'].sum()
        total.append(total_view)
        
    games_sorted['Total_Viewer'] = total
    result = games_sorted.sort_values('Total_Viewer', ascending=False)
    result.to_csv(path)

    return
    

# return a list of sorted csv file name
def find_csv_filenames( path_to_dir, suffix=".csv" ):

    filenames = os.listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]
