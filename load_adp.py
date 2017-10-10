import re
import requests
from bs4 import BeautifulSoup
from models import Player
from instantiate_session import session

def grab_adp_rows():
    """
    Use Beautiful Soup to retrieve the rows of a player's ADP
    :return: rows
    """
    url = 'https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php'
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    rows = soup.findAll('tr', attrs={'class': re.compile('mpb-player*')})
    return rows

def load_into_adp(rows):
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
        p = Player(
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
    rows = grab_adp_rows()
    load_into_adp(rows)
    return

if __name__ == "__main__":
    main()
