from requests_html import HTMLSession
from bs4 import BeautifulSoup
import psycopg2
import json

def esc_q(text: str) -> str:
    text = text.replace('\'', '\'\'').replace('\n', '').replace('[1]', '').strip()
    return text.replace('IATA  – ', '')

sess = psycopg2.connect(
    host='127.0.0.1',
    port=5432,
    dbname='air_booking',
    user='kotprokhor',
    password='Pk23072002'
)

airlines = {}
session = HTMLSession()
URL = 'https://azcargo.cz/en/services/support/iata-airline-codes/'
last_key = ''

response = session.get(URL)
soup = BeautifulSoup(response.content).find('tbody')

for i, s in enumerate(soup.find_all('tr')):
    if i == 0: continue

    ref = s.find('td').next_sibling.next_sibling
    iata = esc_q(ref.text)
    ref = ref.next_sibling.next_sibling
    name = esc_q(ref.text)

    if name == '':
        continue

    if iata not in airlines:
        airlines[iata] = name
        last_key = iata


with open('airlines.json', 'w') as file:
    al = [{iata: airlines[iata]} for iata in airlines]
    file.write(json.dumps(al))

query = """INSERT INTO airline(airline_code, airline_name) VALUES\n"""

for al in airlines:
    query += (
        f"""('{al}',""" + 
        f"""'{airlines[al]}')"""
        )

    if al != last_key:
        query += ',\n'

print(query)

cur = sess.cursor()
cur.execute(query)
sess.commit()