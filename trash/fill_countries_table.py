import json
from pathlib import Path

import mariadb

if __name__ == '__main__':
    with open('../resources/countries-codes.json') as f:
        countries = json.load(f)
    print(countries)
    with open(Path.home() / 'database_connection.json') as f:
        connection_parameters = json.load(f)
    with mariadb.connect(**connection_parameters) as conn:
        with conn.cursor() as cursor:
            for country in countries:
                cursor.execute('insert into countries(iso2, iso3, denomination) values(%s, %s, %s)', (country['iso2_code'], country['iso3_code'], country['label_en']))
            conn.commit()
