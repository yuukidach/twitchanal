import os
import time
import pandas as pd
import logging
from typing import NoReturn
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from collections import defaultdict
from twitchanal.secret.secret import load_id_secret
from multiprocessing.dummy import Pool as ThreadPool
from alive_progress import alive_bar
from .fetch import fetch_top_n_games, fetch_game_streams, fetch_url

TWITCH_TRCK_URL = 'https://twitchtracker.com/'


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


def save_game_streams(twitch: Twitch, data_folder: str, game_id: str,
                      fname: str) -> NoReturn:
    """ save live streams

    Args:
        twitch (Twitch): twitch api class instance
        data_folder (str): folder to contains data
        game_id (str): game id
        fname (str): data file name
    
    Returns:
        NoReturn
    """
    game_streams = fetch_game_streams(twitch, game_id)
    if not game_streams is None:
        save_data_csv(data_folder, fname, game_streams)


def save_n_game_streams(twitch: Twitch,
                        data_folder: str,
                        data: pd.DataFrame,
                        file_suffix: str,
                        n: int = 100) -> NoReturn:
    """ save live streams of each games

    Args:
        twitch (Twitch): twitch api class instance
        data_folder (str): folder to contains data
        data (pd.DataFrame): game dataframe
        file_suffix (str): suffix for data file
        n (int, optional): number of live streams to collect. Defaults to 100.
    
    Returns:
        NoReturn
    """
    data_folder = os.path.join(data_folder, 'game_streams' + file_suffix)
    len = data.shape[0]
    game_names = data['name'].tolist()
    game_names = [name.replace(' ', '') \
                      .replace('/', '') \
                      .replace('\\', '') for name in game_names]
    fnames = ['game_' + x + file_suffix for x in game_names]
    twitchs = [twitch] * len
    data_folders = [data_folder] * len
    game_ids = data['id'].tolist()
    pool = ThreadPool(10)
    pool.starmap(save_game_streams, zip(twitchs, data_folders, game_ids,
                                        fnames))


def collect_game_info(df: pd.DataFrame) -> pd.DataFrame:
    """ Collect more specific info from `twitchtracker`

    Args:
        df (pd.DataFrame): dataframe of top_games

    Returns:
        pd.DataFrame: top_games with more info
    """
    data_dict = defaultdict(list)
    len = df.shape[0]

    with alive_bar(len) as bar:
        for _, row in df.iterrows():
            gid = row['id']

            html = fetch_url(TWITCH_TRCK_URL + 'games/' + gid, hint='game')
            divs = html.find_all('div', {'class': 'g-x-s-block'})
            for div in divs:
                # Give a initial value as None
                # so that the program won't raise exception for length
                val, label = (None, None)
                val = div.find('div', {'class': 'g-x-s-value'}).text.strip()
                label = div.find('div', {'class': 'g-x-s-label'}).text
                if ('@' in label):
                    (label, date) = label.split('@')
                    val += date
                data_dict[label].append(val)

            bar()

    df = df.assign(**data_dict)
    return df


def collect_data(data_folder: str = './dataset',
                 with_timestamp: bool = True,
                 num: int = 251,
                 extra: bool = True) -> NoReturn:
    """ collecet data from twitch api

    Args:
        data_folder (str, optional): folder to contains data files. Defaults to './data'.
        with_timestamp (bool, optional): whether using a timestamp as suffix or not. 
                                         Defaults to True.
        num (int, optional): Number of games to collect.
        extra (bool, optional): Whether to collect extra info like `peek viewers`, 
                                `peek channels` and so on for top games.
    
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

    top_games = fetch_top_n_games(twitch, num)
    save_n_game_streams(twitch, data_folder, top_games, timestamp)
    if extra:
        top_games = collect_game_info(top_games)
    save_data_csv(data_folder, 'top_games' + timestamp, top_games)
