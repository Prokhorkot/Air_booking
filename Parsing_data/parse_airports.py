from requests_html import HTMLSession
from bs4 import BeautifulSoup
import psycopg2
import json

def esc_q(text: str) -> str:
    return text.replace('\'', '\'\'').replace('\n', '').replace('[1]', '')

sess = psycopg2.connect(
    host='127.0.0.1',
    port=5432,
    dbname='air_booking',
    user='kotprokhor',
    password='Pk23072002'
)

alphabet = list('abcdefghijklm'.upper())

session = HTMLSession()

text = ''
airports = []

for ch in alphabet:
    URL = f'https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:_{ch}'
    request = session.get(URL)

    soup = BeautifulSoup(request.content)

    soup = soup.find('tbody')
    for sortbottom in soup.find_all('tr', {'class':'sortbottom'}):
        sortbottom.decompose()
    for thead in soup.find_all('thead'):
        thead.decompose()

    for i, s in enumerate(soup.find_all('tr')):
        if i != 0 and 'UTC' in s.text:
            ref = s.find('td')
            iata = esc_q(ref.text)

            airports.append({})
            ap = airports[-1]

            ref = ref.next_sibling.next_sibling.next_sibling.next_sibling
            name = esc_q(ref.text.split('(')[0])
            ref = ref.next_sibling.next_sibling
            location = esc_q(ref.text)
            loc_list = location.split(', ')
            city = loc_list[0]
            country = loc_list[-1]
            ref = ref.next_sibling.next_sibling
            utc = ref.text.\
                replace('UTC', '').replace('−', '-').replace('±', '').\
                    split(':')
            hours = int(utc[0])
            minutes = int(utc[1])

            ap['IATA'] = iata
            ap['name'] = name
            ap['country'] = country
            ap['city'] = city
            ap['hours'] = hours
            ap['minutes'] = minutes


with open('test.json', 'w') as file:
    file.write(json.dumps(airports))

print('##########################')
print('Values parsed')
print('##########################')

cur = sess.cursor()

query = '''INSERT INTO airport(
        airport_code,
        airport_name,
        country, city,
        timezone_hours,
        timezone_minutes)
    VALUES'''

for ap in airports[:-1]:
    if len(ap['IATA']) > 3:
        print(ap)
        continue
    query += (
        f"""('{ap['IATA']}', """ +
        f"""'{ap['name']}', """ + 
        f"""'{ap['country']}', """ + 
        f"""'{ap['city']}', """ + 
        f"""{ap['hours']},""" + 
        f"""{ap['minutes']}),\n"""
        )

ap = airports[-1]
query += (
        f"""('{ap['IATA']}', """ +
        f"""'{ap['name']}', """ + 
        f"""'{ap['country']}', """ + 
        f"""'{ap['city']}', """ + 
        f"""{ap['hours']},""" + 
        f"""{ap['minutes']})\n"""
        )

cur.execute(query)
sess.commit()