import pandas as pd
import requests
import time
import random
import logging
from typing import List
from termcolor import colored, cprint
from twitchAPI import Twitch
from bs4 import BeautifulSoup
from alive_progress import alive_bar
from collections import defaultdict

TWITCH_TRCK_URL = 'https://twitchtracker.com/'

HAEDER = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.8',
}


def turn_into_df(data: dict) -> pd.DataFrame:
    """ turn raw data into a pandas DataFrame

    Args:
        data (dict): dict collect from twitch api

    Returns:
        pd.DataFrame
    """
    data = data['data']
    data = pd.DataFrame(data)
    return data


def fetch_twitch_data(twitch: Twitch, fn_name: str, **kwargs) -> pd.DataFrame:
    """ fetch data from Twitch API

    Args:
        twitch (Twitch): twitchAPI object
        fn_name (str): function name of twitchAPI
        **kwargs: arguments for fn_name

    Returns:
        pd.DataFrame: fetched data
    """
    n = kwargs['first']
    fn = getattr(twitch, fn_name)

    kwargs['first'] = min(100, n)
    n -= kwargs['first']
    data_all = fn(**kwargs)
    data = turn_into_df(data_all)
    while (n > 0):
        kwargs['first'] = min(100, n)
        n -= kwargs['first']
        # check if there is more pages
        if not data_all['pagination']:
            break
        kwargs['after'] = data_all['pagination']['cursor']
        data_all = fn(**kwargs)
        data = pd.concat([data, turn_into_df(data_all)])

    return data


def fetch_top_games(twitch: Twitch, n: int = 100) -> pd.DataFrame:
    """ fetch top n games

    Args:
        twitch (Twitch): twich api class instance
        n (int, optional): how many data rows to collect. Defaults to 100.

    Returns:
        pd.DataFrame
    """
    top_games = fetch_twitch_data(twitch, 'get_top_games', first=n)

    return top_games


def fetch_game_streams(twitch: Twitch,
                       game_id: str,
                       n: int = 100) -> pd.DataFrame:
    """ fetch game streams data from Twitch API

    Args:
        twitch (Twitch): twitch api instance
        game_ids (str): list of game ids
        n (int): how many streams to fetch

    Returns:
        pd.DataFrame / None: dataframe of game streams
    """
    kwargs = {'first': n, 'game_id': [game_id]}
    game_streams = fetch_twitch_data(twitch, 'get_streams', **kwargs)
    # get user id to dig more data
    try:
        total_user_ids = game_streams['user_id'].tolist()
        user_ids_num = len(total_user_ids)
        ephoch = user_ids_num // 100
        if user_ids_num % 100 != 0:
            ephoch += 1
    except:
        print('game_streams')
        cprint('Error: ' + game_id + ' data broken. Jump over it.', 'red')
        return None
    else:
        total_users_data = pd.DataFrame(
            columns=['broadcaster_type', 'description', 'type'])
        for i in range(ephoch):
            user_ids = total_user_ids[i * 100:i * 100 + 100]
            users_data = twitch.get_users(user_ids=user_ids)
            users_data = turn_into_df(users_data)
            # select needed columns
            users_data = users_data[[
                'broadcaster_type', 'description', 'type'
            ]]
            total_users_data = total_users_data.append(users_data,
                                                       ignore_index=True)

        total_users_data.reset_index(drop=True, inplace=True)
        game_streams.reset_index(drop=True, inplace=True)
        game_streams = pd.concat([game_streams, total_users_data], axis=1)
        return game_streams


def fetch_url(url: str, hint: str = ""):
    """ fetch url content

    Args:
        url (str): URL
        hint (str, optional): Prompt hint. Defaults to "".

    Returns:
        BeautifulSoup object
    """
    print("Fetching " + hint + ":", url.split('/')[-1] + '...')

    while True:
        page = requests.get(url, headers=HAEDER)
        if page.status_code == 200:
            break
        logging.info(url.split('/')[-1] + ' busy. Try again...')
        time.sleep(random.uniform(1.6, 3.0))

    html = BeautifulSoup(page.text, 'html.parser')
    return html


def fetch_game_info(df: pd.DataFrame) -> pd.DataFrame:
    """ Fetch more specific info from `twitchtracker`

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
