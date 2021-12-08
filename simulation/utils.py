import pandas as pd

def is_mislabelled(row: pd.Series, mean_limit: float = 0.6, sd_limit: float = 0.4):
    if float(row['mean']) < mean_limit and float(row['std']) < sd_limit:
        return 'identified'
    else:
        return 'not identified'

def get_sim_mean(row):
    mu = row['index'].split('_')[1]
    return float(mu[:3])


def get_sim_sd(row):
    sd = row['index'].split('_')[2]
    return float(sd[:3])


def get_sim_flip_percent(row):
    flip = row['index'].split('_')[0]
    if len(flip) > 8:
        return int(flip[0:2])
    else:
        return int(flip[0])