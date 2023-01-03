from requests_html import HTMLSession
from bs4 import BeautifulSoup
import psycopg2
import json

def esc_q(text: str) -> str:
    return text.replace('\'', '\'\'').replace('\n', '').replace('[1]', '').strip()

sess = psycopg2.connect(
    host='127.0.0.1',
    port=5432,
    dbname='air_booking',
    user='kotprokhor',
    password='Pk23072002'
)

aircrafts = {}
session = HTMLSession()
URL = 'https://en.wikipedia.org/wiki/List_of_aircraft_type_designators'
last_key = ''

response = session.get(URL)
soup = BeautifulSoup(response.content).find('tbody')

for i, s in enumerate(soup.find_all('tr')):
    if i == 0: continue
    ref = s.find('td').next_sibling.next_sibling
    if len(ref.text) != 3: continue

    iata = esc_q(ref.text)
    ref = ref.next_sibling.next_sibling
    name = esc_q(ref.text)
    
    if iata not in aircrafts:
        aircrafts[iata] = name
        last_key = iata

query = """INSERT INTO aircraft(
    iata_type_code,
    model_name
    )
    VALUES"""

for ac in aircrafts:
    query += (
        f"""('{ac}',""" + 
        f"""'{aircrafts[ac]}')"""
    )
    if ac != last_key: query += ',\n'

with open('aircrafts.json', 'w') as file:
    ac = [{iata: aircrafts[iata]} for iata in aircrafts]
    file.write(json.dumps(ac))


cur = sess.cursor()
cur.execute(query + ';')
sess.commit()
