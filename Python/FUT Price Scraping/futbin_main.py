import urllib2
import csv
from bs4 import BeautifulSoup
import random
import sys

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

CardTypes = ['gold', 'silver', 'bronze']

def ProcessCardType(list):
    result = None
    for type in CardTypes:
        if type in list:
            result = type
            break
    if result is None:
        print('FIX ME')

    return result, 'rare' in list

def ProcessCost(string):
    unit = string[-1]
    if unit == 'M':
        return int(float(string.rstrip('M'))*1000000)
    if unit == 'K':
        return int(float(string.rstrip('K')) * 1000)
    return int(string)


player_list = []
ratings_list = range(int(sys.argv[1:][0]),int(sys.argv[1:][1]))
filename = 'G:\\Fifa\\FUT_Scraping\\' + sys.argv[1:][2] + '.csv'
print("Processing players to file: " + filename)

for rating in ratings_list[::-1]:
    print('Processing rating ' + str(rating))
    print('===========================')
    resultsFound = True
    for x in range(1, 99):
        url = 'https://www.futbin.com/18/players?page={0}&player_rating={1}-{1}'.format(x, rating)
        headers={'User-Agent':random.choice(user_agent_list),}

        while True and resultsFound:
            try:
                req = urllib2.Request(url, headers=headers)

                try:
                    page = urllib2.urlopen(req)
                except urllib2.HTTPError, e:
                    print e.fp.read()

                content = page.read()
                soup = BeautifulSoup(content,"html.parser")
                all_tables = soup.find_all('table')

                page.close()

                if all_tables[2].tbody.findAll('tr')[0].string == 'No Results':
                    resultsFound = False
                    break

                print('Page ' + str(x))

                for row in all_tables[2].tbody.findAll('tr'):
                    elements = row.find_all('td')
                    player_data = elements[0].contents[3].find_all('a')
                    country = player_data[1].attrs['data-original-title']
                    id = elements[0].find('img').attrs['src'].rsplit('/')[-1].split('.')[0]
                    name = elements[0].find('a', {'class': 'player_name_players_table'}).string
                    club = player_data[0].attrs['data-original-title']
                    league = player_data[2].attrs['data-original-title']
                    position = elements[2].string
                    pscost = ProcessCost(elements[4].find('span').string)
                    xboxcost = ProcessCost(elements[5].find('span').string)
                    rating = elements[1].string
                    player_type, rare = ProcessCardType(elements[1].next.attrs['class'])
                    if pscost > 0:
                        player_list.append({'id': id, 'name': name, 'country': country, 'club': club, 'league': league,
                                            'position': position, 'ps_cost': pscost, 'xbox_cost': xboxcost, 'rating': rating,
                                            'player_type': player_type, 'rare': rare})
                break
            except:
                pass
            print('Error found processing page: ' + url + '. Trying again')
        if not resultsFound:
            break


with open(filename, 'w') as csvfile:
    fieldnames = ['id', 'name', 'country', 'club', 'league', 'position', 'ps_cost', 'xbox_cost', 'rating', 'player_type', 'rare']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
    writer.writeheader()
    for player in player_list:
        row = {k: unicode(v).encode("utf-8") for k, v in player.iteritems()}
        writer.writerow(row)

