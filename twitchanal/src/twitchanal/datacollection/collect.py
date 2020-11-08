import os
import yaml
import time
import pandas as pd
from typing import NoReturn
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from twitchanal.save_secret.save_secret import *


def get_dataframe(data: dict) -> pd.DataFrame:
    """ get dataframe from data

    Args:
        data (dict): dict collect from twitch api

    Returns:
        pd.DataFrame
    """
    data = data['data']
    data = pd.DataFrame(data)
    return data


def save_data_yaml(folder: str, fname: str, data: dict) -> NoReturn:
    """ Save data in a yaml file

    Args:
        folder (str): folder path to contains the file
        fname (str): name of the file
        data (dict): data collected

    Returns:
        NoReturn
    """
    fname += '.yaml'
    fpth = os.path.join(folder, fname)
    os.makedirs(folder, exist_ok=True)
    with open(fpth, 'w') as f:
        yaml.dump(data, f)
    print('Finish writing', fname)


def save_data_csv(folder: str, fname: str, data: pd.DataFrame) -> NoReturn:
    """ Save data in a csv file

    Args:
        folder (str): folder path to contains the file
        fname (str): name of the file
        data (pd.DataFrame): data collected

    Returns:
        NoReturn
    """
    fname += '.csv'
    fpth = os.path.join(folder, fname)
    os.makedirs(folder, exist_ok=True)
    data.to_csv(fpth, index=False)
    print('Finish writing', fname)


def collect_top_n_games(twitch: Twitch,
                        data_folder: str,
                        file_suffix: str,
                        n: int = 100) -> pd.DataFrame:
    """ collect top n games

    Args:
        twitch (Twitch): twich api class instance
        data_folder (str): data folder to contains data
        file_suffix (str): suffix for data file name
        n (int, optional): how many data rows to collect. Defaults to 100.

    Returns:
        pd.DataFrame
    """
    fname = 'top_games' + file_suffix

    cnt = min(100, n)
    n -= cnt
    top_games_data = twitch.get_top_games(first=cnt)
    top_games = get_dataframe(top_games_data)
    while (n > 0):
        cnt = min(100, n)
        n -= cnt
        top_games_data = twitch.get_top_games(
            first=cnt, after=top_games_data['pagination']['cursor'])
        top_games = pd.concat([top_games, get_dataframe(top_games_data)])

    save_data_csv(data_folder, fname, top_games)
    return top_games


def collect_game_streams(twitch: Twitch,
                         data_folder: str,
                         data: pd.DataFrame,
                         file_suffix: str,
                         n: int =100):
    """ collect live streams of each games

    Args:
        twitch (Twitch): twitch api class instance
        data_folder (str): folder to contains data
        data (pd.DataFrame): game dataframe
        file_suffix (str): suffix for data file
        n (int, optional): number of live streams to collect. Defaults to 100.
    """
    data_folder = os.path.join(data_folder, 'game_streams' + file_suffix)
    for _, row in data.iterrows():
        game_name = row['name'].replace(' ', '') \
                               .replace('/', '') \
                               .replace('\\', '')
        fname = 'game_' + game_name + file_suffix
        game_streams_data = twitch.get_streams(first=100, game_id=[row['id']])
        save_data_yaml(data_folder, fname, game_streams_data)
        game_streams = get_dataframe(game_streams_data)
        # get user id to dig more data
        users_id = list(game_streams['user_id'])
        users_data = twitch.get_users(user_ids=users_id)
        users_data = get_dataframe(users_data)
        # select needed columns
        users_data = users_data[['broadcaster_type', 'description', 'type']]
        game_streams = pd.concat([game_streams, users_data], axis=1)
        save_data_csv(data_folder, fname, game_streams)


def collect_data(data_folder: str = './dataset',
                 with_timestamp: bool = True,
                 num: int=251) -> NoReturn:
    """ collecet data from twitch api

    Args:
        data_folder (str, optional): folder to contains data files. Defaults to './data'.
        with_timestamp (bool, optional): whether using a timestamp as suffix or not. Defaults to True.
    
    Returns:
        NoReturn
    """
    (id, secret) = load_id_secret()
    if (id is None or secret is None):
        id = input('Enter id: ')
        secret = input('Enter secret: ')
    twitch = Twitch(id, secret)
    twitch.authenticate_app([])

    if (with_timestamp):
        timestamp = "_" + str(int(time.time()))
    else:
        timestamp = ""

    top_games = collect_top_n_games(twitch, data_folder, timestamp, num)
    collect_game_streams(twitch, data_folder, top_games, timestamp)


if __name__ == '__main__':
    collect_data()
