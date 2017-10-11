import re
import requests
from bs4 import BeautifulSoup
from models import PlayerStandard, PlayerPPR, PlayerHalfPPR
from instantiate_session import session
from argparse import ArgumentParser

def grab_adp_rows(scoring):
    """
    Use Beautiful Soup to retrieve the rows of a player's ADP
    :return: rows
    """
    if scoring == 'ppr':
        url = 'https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php'
    elif scoring == 'standard':
        url = 'https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php'
    elif scoring == 'half-ppr':
        url = 'https://www.fantasypros.com/nfl/rankings/half-point-ppr-cheatsheets.php'

    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    rows = soup.findAll('tr', attrs={'class': re.compile('mpb-player*')})
    return rows

def load_into_adp(rows, scoring):
    """
    Create a 'Player' object for each row and add it to the session
    Commit the entire session or rollback
    :param rows:
    """
    for row in rows:
        text = row.text
        data = text.split('\n')
        name_team = data[1]
        tmp_name_team_groups = name_team.split(' ')
        name = ' '.join(tmp_name_team_groups[:-2])
        team = ' '.join(tmp_name_team_groups[-2:]).rstrip()
        if data[3].startswith('K'):
            position = 'K'
            position_rank = data[3][1:]
        elif data[3].startswith('DST'):
            position = 'DST'
            position_rank = data[3][3:]
        else:
            position = data[3][:2]
            position_rank = data[3][2:]
        if data[9] == "":
            data[9] = 1000

        if scoring == 'standard':
            playermodel = PlayerStandard
        elif scoring == 'ppr':
            playermodel = PlayerPPR
        elif scoring == 'half-ppr':
            playermodel = PlayerHalfPPR

        p = playermodel(
            rank = data[0],
            name = name,
            team = team,
            posrank_str = data[3],
            bye = data[4],
            adp = data[9],
            best = data[5],
            worst = data[6],
            avg = data[7],
            stdev = data[8],
            position = position,
            position_rank = position_rank
            )
        session.add(p)

    try:
        session.commit()
        return len(rows)
    except e:
        session.rollback()
        return e

def main():
    scoring_methods = ['standard', 'ppr', 'half-ppr']
    rows_dict = {s: grab_adp_rows(s) for s in scoring_methods}
    for scoring, rows in rows_dict.iteritems():
        load_into_adp(rows, scoring)
    return

if __name__ == "__main__":
    main()