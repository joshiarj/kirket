# -*- coding: utf-8 -*-
"""

@author: mpr

TODO: 
    Joe Root :
        http://stats.espncricinfo.com/ci/engine/player/303669.html?class=2;template=results;type=batting;view=innings
    This is the list to pull from, from here pull the match numbers, and then the data dump.g
    
"""

# Currently trying it out with Joe Root's debut match. Can extend it to the
# full list once we have the wrapper up and running.

import requests
from bs4 import BeautifulSoup
import re

# Virat Kohli - 253802
# Joe Root = 303669
# ABDV = 44936
# Kane Williamson= 277906
# Steven Smith = 267192
# playerid = "303669"
# First let us find all the games a player has played.


def find_player_matches(playerid):
    """
    Finds the list of ODI innings the batsman has played, 
    and finds the match numbers and returns it as a list.
    """
    page = requests.get("http://stats.espncricinfo.com/ci/engine/player/{}.html"
                        "?class=2;template=results;type=batting;view=innings".format(playerid))
    # soup = BeautifulSoup(page.text)
    soup = BeautifulSoup(page.text, 'html.parser')
    # soup = BeautifulSoup(page.text, 'html.parser', markup_type='lxml')
    
    player_match_list = soup.find_all(name='a', attrs={"title":"view the scorecard for this row"})
    
    # From the above list we need to parse out the match numbers which are part of
    # the link. part after the /match/ and before the .html
    
    match_list = []
    for each in player_match_list:
        a = str(each)
        b = re.sub('<a href="/ci/engine/match/', "", a)
        b = b.split(".")       
        match_list.append(b[0])
    return match_list
