"""Query Wikidata for Belgian politicians"""

import argparse
from datetime import datetime as dt

from SPARQLWrapper import SPARQLWrapper, JSON

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filter', type=str, help='Filtering on name')
parser.add_argument('-n', '--number', type=int, help='Number of rows to display')

def get_rows():
    """Retrieve results from SPARQL"""
    endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
    sparql = SPARQLWrapper(endpoint)

    statement = """
#Musées Bruxelles
SELECT DISTINCT ?item ?itemLabel ?coordinates ?date_de_fondation_ou_de_cr_ation ?site_officiel WHERE {
  ?item (wdt:P31/(wdt:P279*)) wd:Q33506;
    wdt:P131 wd:Q239;
    wdt:P625 ?coordinates.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "fr, nl, en". }
  OPTIONAL { ?item wdt:P6375 ?adresse. }
  OPTIONAL { ?item wdt:P571 ?date_de_fondation_ou_de_cr_ation. }
  OPTIONAL { ?item wdt:P854 ?URL_de_la_r_f_rence. }
  OPTIONAL { ?item wdt:P856 ?site_officiel. }
}
    """

    sparql.setQuery(statement)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    rows = results['results']['bindings']
    print(f"\n{len(rows)} Brussels museums found\n")
    return rows

def show(rows, name_filter=None, n=10):
    """Display n politicians (default=10)"""
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    if name_filter:
        rows = [row for row in rows if name_filter in row['itemLabel']['value'].lower()]
    print(f"Displaying the first {n}:\n")
    for row in rows[:n]:
        name =  row['itemLabel']['value']
        try:
            site_officiel = row['site_officiel']['value']
        except KeyError:
            site_officiel = "????"       
        print(f"Nom: {name}. Site officiel: {site_officiel}")
                
        try:
            date_de_fondation_ou_de_cr_ation = dt.strptime(row['date_de_fondation_ou_de_cr_ation']['value'], date_format)
            date_de_fondation_ou_de_cr_ation_y = date_de_fondation_ou_de_cr_ation.year
            date_de_fondation_ou_de_cr_ation_m = date_de_fondation_ou_de_cr_ation.month
            date_de_fondation_ou_de_cr_ation_d = date_de_fondation_ou_de_cr_ation.day
        except (ValueError, KeyError):
            date_de_fondation_ou_de_cr_ation_y = '????'
            date_de_fondation_ou_de_cr_ation_m = '??'
            date_de_fondation_ou_de_cr_ation_d = '??'
        print(f"Date de fondation ou de création: {date_de_fondation_ou_de_cr_ation_d}/{date_de_fondation_ou_de_cr_ation_m}/{date_de_fondation_ou_de_cr_ation_y}")
            
if __name__ == "__main__":
    args = parser.parse_args()
    my_rows = get_rows()
    my_filter = args.filter if args.filter else None
    number = args.number if args.number else 10
    show(my_rows, my_filter, number)
