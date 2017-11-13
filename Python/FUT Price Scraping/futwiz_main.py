import urllib2
import csv
from bs4 import BeautifulSoup
import random

user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]

position_index = 2
player_details = 1
price = 3
rating_card = 4

CardTypes = {

    'small-gold': {
        'rare': True,
        'type': 'Gold'
    },
    'totw_gold': {
        'rare': True,
        'type': 'TOTW'
    },
    'small_common_gold': {
        'rare': False,
        'type': 'Gold'
    },
    'small_otw': {
        'rare': True,
        'type': 'OTW'
    },
    'small-icon':{
        'rare': True,
        'type': 'Icon'
    },
    'small_halloween':{
        'rare': True,
        'type': 'Halloween'
    },
    'small_award_winner':{
        'rare': True,
        'type': 'Award Winner'
    },
    'small_sbc':{
        'rare': True,
        'type': 'SBC Reward'
    },
    'small_rare_silver':{
        'rare': True,
        'type': 'Silver'
    },
    'small_purple':{
        'rare': True,
        'type': 'Hero'
    },
    'small_common_silver':{
        'rare': False,
        'type': 'Silver'
    },
    'small_totw_silver':{
        'rare': True,
        'type': 'TOTW Silver'
    },
    'small_rare_bronze':{
        'rare': True,
        'type': 'Bronze'
    },
    'small_common_bronze':{
        'rare': False,
        'type': 'Bronze'
    },
}

def ProcessCardType(string):
    result = None
    for type in CardTypes:
        if type in string:
            result = type
            break
    if result is None:
        print('FIX ME')

    return CardTypes[result]['type'], CardTypes[result]['rare']

player_list = []
try:
    for x in range(450, 632):
        print('PROCESSING PAGE ' + str(x))
        testurl = "https://www.futwiz.com/en/fifa18/players?page="+str(x)
        headers={'User-Agent':random.choice(user_agent_list),}

        req = urllib2.Request(testurl, headers=headers)

        try:
            page = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()

        content = page.read()
        soup = BeautifulSoup(content,"html.parser")
        all_tables = soup.find_all('table')

        for row in all_tables[0].tbody.findAll('tr'):
            elements = row.find_all('td')
            country = int(elements[player_details].find_all('img')[1].attrs['src'].rsplit('/')[-1].split('.')[0])
            details = elements[player_details].find_all('a')
            id = int(details[0].attrs['href'].rsplit('/',1)[-1])
            name = details[0].string
            club = details[1].string
            league = details[2].string
            position = elements[position_index].string.rstrip().lstrip()
            cost = int(elements[price].string.rstrip().lstrip().replace(',',''))
            rating = elements[rating_card].div.div.string
            player_type, rare = ProcessCardType(elements[rating_card].a.contents[1].attrs['style'])
            if cost > 0:
                player_list.append({'id': id, 'name': name, 'country': country, 'club': club, 'league': league,
                                    'position': position, 'cost': cost, 'rating': rating, 'player_type': player_type,
                                    'rare': rare})
finally:
    with open('G:\\Fifa\\FUT_Scraping\\players_450_631.csv', 'w') as csvfile:
        fieldnames = ['id', 'name', 'country', 'club', 'league', 'position', 'cost', 'rating', 'player_type', 'rare']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
        writer.writeheader()
        for player in player_list:
            row = {k: unicode(v).encode("utf-8") for k, v in player.iteritems()}
            writer.writerow(row)

