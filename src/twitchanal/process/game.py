import os
import sys
import glob
import pandas as pd
from termcolor import colored, cprint
from typing import List

class Game(object):
    def __init__(self, dir='dataset', timestamp=None):
        self.dir = dir
        self.timestamp = timestamp
        self.tags = self._init_tags()
        self.data = self._init_data()
        self._append_label_data()
        self._clean_data()

    def get_data_pth(self) -> str:
        """ get data path

        Returns:
            str: file path
        """
        # get latest data file by default
        if self.timestamp is None:
            all_fpth = glob.glob(os.path.join(self.dir, '*.csv'))
            all_fpth = sorted(all_fpth, key=os.path.getmtime)
            fpth = all_fpth[-1]
        else:
            fname = 'top_games_' + self.timestamp + '.csv'
            fpth = os.path.join(self.dir, fname)

        if not os.path.exists(fpth):
            cprint(
                'Error: No dataset found. Check if the dataset directory is right.',
                'red')
            sys.exit()

        return fpth

    def _init_data(self) -> pd.DataFrame:
        """ initialize dataframe

        Returns:
            pd.DataFrame: data
        """
        fpth = self.get_data_pth()
        df = pd.read_csv(fpth)
        df = df.drop('box_art_url', axis=1).dropna()
        return df

    def _init_tags(self) -> dict:
        """ initialize tags list

        Returns:
            dict: {tag: [game_ids]}
        """
        tag_dir = os.path.join(self.dir, 'tags')
        tag_files = glob.glob(os.path.join(tag_dir, '*.csv'))

        tags = {}
        for tag_file in tag_files:
            try:
                df = pd.read_csv(tag_file)
            except:
                continue
            ids = df['id'].values
            tag = tag_file.split('/')[-1].split('.')[0]
            tags[tag] = ids
        return tags

    def _find_labels(self, game_id: int) -> List:
        """ find labels for certain game

        Args:
            game_id (int): game id

        Returns:
            List: [labels]
        """
        labels = []
        for key, val in self.tags.items():
            if game_id in val:
                labels.append(key)
        return labels

    def _append_label_data(self):
        """ append labels to dataframe
        """
        ids = self.data['id'].values
        labels = [self._find_labels(id) for id in ids]
        self.data['label'] = labels

    def _clean_data(self):
        """ data cleaning
        """
        idxes = []
        for idx, row in self.data.iterrows():
            label = row['label']
            if ('IRL' in label) or (not label):
                idxes.append(idx)
        self.data = self.data.drop(idxes)

    def get_data(self):
        return self.data
    
    def get_tags(self):
        return self.tags

    def get_labels(self) -> dict:
        cat = {}
        for _, row in self.data.iterrows():
            label = row['label']
            for tag in label:
                if tag in cat:
                    cat[tag].append(row['id'])
                else:
                    cat[tag] = [row['id']]
        return cat
