import os
import yaml
import time
import pandas as pd
import requests
from typing import NoReturn
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from bs4 import BeautifulSoup
from collections import defaultdict
from termcolor import colored, cprint
from twitchanal.secret.secret import *

TWITCH_TRCK_URL = 'https://twitchtracker.com/'
HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
         AppleWebKit/537.36 (KHTML, like Gecko)    \
         Chrome/74.0.3729.169 Safari/537.36'
}


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


def collect_top_n_games(twitch: Twitch, n: int = 100) -> pd.DataFrame:
    """ collect top n games

    Args:
        twitch (Twitch): twich api class instance
        n (int, optional): how many data rows to collect. Defaults to 100.

    Returns:
        pd.DataFrame
    """
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

    return top_games


def save_game_streams(twitch: Twitch,
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
    for _, row in data.iterrows():
        game_name = row['name'].replace(' ', '') \
                               .replace('/', '') \
                               .replace('\\', '')
        fname = 'game_' + game_name + file_suffix
        game_streams_data = twitch.get_streams(first=100, game_id=[row['id']])
        game_streams = get_dataframe(game_streams_data)

        # get user id to dig more data
        try:
            users_id = game_streams['user_id'].tolist()
        except:
            print(game_streams)
            cprint('Error: ' + game_name + ' data broken. Jump over it.',
                   'red')
        else:
            users_data = twitch.get_users(user_ids=users_id)
            users_data = get_dataframe(users_data)
            # select needed columns
            users_data = users_data[[
                'broadcaster_type', 'description', 'type'
            ]]
            # print(users_data['description'])
            game_streams = pd.concat([game_streams, users_data], axis=1)
            save_data_csv(data_folder, fname, game_streams)


def fetch_url(url: str, hint: str = ""):
    print("Fetching " + hint + ":", url.split('/')[-1], '...')

    while True:
        page = requests.get(url, headers=HEADERS)
        if page.status_code == 200:
            break
        print('Busy. Try again...')
        time.sleep(1)

    html = BeautifulSoup(page.text, 'html.parser')
    return html


def collect_game_info(df: pd.DataFrame) -> pd.DataFrame:
    """ Collect more specific info from `twitchtracker`

    Args:
        df (pd.DataFrame): dataframe of top_games

    Returns:
        pd.DataFrame: top_games with more info
    """
    data_dict = defaultdict(list)

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

    df = df.assign(**data_dict)
    return df


def collect_data(data_folder: str = './dataset',
                 with_timestamp: bool = True,
                 num: int = 251) -> NoReturn:
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

    top_games = collect_top_n_games(twitch, num)
    save_game_streams(twitch, data_folder, top_games, timestamp)
    top_games = collect_game_info(top_games)
    save_data_csv(data_folder, 'top_games' + timestamp, top_games)


if __name__ == '__main__':
    collect_data()
