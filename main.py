import requests
import datetime
import os
import json
import logging

from bs4 import BeautifulSoup
from google.cloud import bigquery

PROJECT_ID = os.environ['GCP_PROJECT']
BQ_DATASET = os.environ['DATASET']
BQ_TABLE = os.environ['TABLE']
SITE_URL = os.environ['SITE_URL']
BQ = bigquery.Client()


def fm802_onair_info(request):
    html = requests.get(SITE_URL)

    soup = BeautifulSoup(html.content, "html.parser")

    noa_song_list = soup.find(class_="noa-song-list")
    song_list = noa_song_list.find_all(["dt", "dd"])
    insert_list = []
    song_dict = {}
    for song in song_list:
        if song.name == "dt":
            time = song.text + ":00"
            song_dict["time"] = time
        else:
            song_dict["artist"] = song.find("span", class_="artist-name").text
            song_dict["song"] = song.find("span", class_="song-name").text
        if len(song_dict) == 3:
            insert_list.append(song_dict.copy())
            song_dict.clear()

    logging.info('Total record: ' + str(len(insert_list)))

    table_id = PROJECT_ID + '.' + BQ_DATASET + '.' + BQ_TABLE
    table = BQ.get_table(table_id)
    errors = BQ.insert_rows(table, insert_list)
    if errors != []:
        raise BigQueryError(errors)


class BigQueryError(Exception):
    '''Exception raised whenever a BigQuery error happened'''

    def __init__(self, errors):
        super().__init__(self._format(errors))
        self.errors = errors

    def _format(self, errors):
        err = []
        for error in errors:
            err.extend(error['errors'])
        return json.dumps(err)
