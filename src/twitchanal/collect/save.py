import os
import time
import pandas as pd
import logging
from typing import NoReturn
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from twitchanal.secret.secret import load_id_secret
from multiprocessing.dummy import Pool as ThreadPool
from .fetch import fetch_top_games, fetch_game_streams, fetch_game_info, fetch_twitch_data

TAGS = [
    '4X', 'Action', 'Adventure Game', 'Arcade', 'Autobattler',
    'Card & Board Game', 'Creative', 'Driving/Racing Game', 'Educational Game',
    'Fighting', 'Flight Simulator', 'FPS', 'Gambling Game', 'Game Overlay',
    'Hidden Objects', 'Horror', 'Indie Game', 'IRL', 'Metroidvania', 'MMO',
    'MOBA', 'Mobile Game', 'Mystery', 'Open World', 'Party', 'Pinball',
    'Platformer', 'Point and Click', 'Puzzle', 'Rhythm & Music Game',
    'Roguelike', 'RPG', 'RTS', 'Shoot \'Em Up', 'Shooter', 'Simulation',
    'Sports Game', 'Stealth', 'Strategy', 'Survival', 'Visual Novel'
]


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


def save_game_streams(twitch: Twitch,
                      data_folder: str,
                      game_id: str,
                      fname: str,
                      n: int = 100) -> NoReturn:
    """ save live streams

    Args:
        twitch (Twitch): twitch api class instance
        data_folder (str): folder to contains data
        game_id (str): game id
        fname (str): data file name
        n (int): number of live streams to collect. Defaults to 100.

    Returns:
        NoReturn
    """
    game_streams = fetch_game_streams(twitch, game_id, n)
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
    n = [n] * len
    pool = ThreadPool(10)
    pool.starmap(save_game_streams,
                 zip(twitchs, data_folders, game_ids, fnames, n))


def save_tags(twitch: Twitch, data_folder: str) -> NoReturn:
    """ save tags for games. usually run only once

    Args:
        twitch (Twitch): twitchAPI object
        data_folder (str): folder to contains data

    Returns:
        NoReturn
    """
    data_folder = os.path.join(data_folder, 'tags')
    for tag in TAGS:
        fname = tag.replace(' ', '') \
                   .replace('&', '') \
                   .replace('/', '') \
                   .replace('\'', '')
        tag_data = fetch_twitch_data(twitch, 'search_categories', query=tag, first=1000)
        save_data_csv(data_folder, fname, tag_data)


def collect_data(data_folder: str = './dataset',
                 with_timestamp: bool = True,
                 num: int = 251,
                 stream: int = 100,
                 extra: bool = True) -> NoReturn:
    """ collecet data from twitch api

    Args:
        data_folder (str, optional): folder to contains data files. Defaults to './data'.
        with_timestamp (bool, optional): whether using a timestamp as suffix or not. 
                                         Defaults to True.
        num (int, optional): Number of games to collect.
        stream (int, optional): Number of streams to collect.
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

    # tags shouldn't be updated too frequently
    if not os.path.exists(os.path.join(data_folder, 'tags')):
        save_tags(twitch, data_folder)

    top_games = fetch_top_games(twitch, num)
    save_n_game_streams(twitch, data_folder, top_games, timestamp, stream)
    if extra:
        top_games = fetch_game_info(top_games)
    save_data_csv(data_folder, 'top_games' + timestamp, top_games)
