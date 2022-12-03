import os
import pysolr
import requests
import json
import sys

CORE_NAME = sys.argv[1].strip()
DATA_PATH = sys.argv[2].strip()
assert DATA_PATH.endswith(".json")
HOST = "localhost"
PORT = 8001

def delete_core(core=CORE_NAME):
    print(os.system('sudo su - solr -c "/opt/solr/bin/solr delete -c {core}"'.format(core=core)))


def create_core(core=CORE_NAME):
    print(os.system(
        'sudo su - solr -c "/opt/solr/bin/solr create -c {core} -n data_driven_schema_configs"'.format(
            core=core)))


# collection
with open(DATA_PATH, 'r') as f:
    collection = json.load(f)
    # print(f'Collection size for {DATA_PATH} - {len(collection)}')
    # print(collection)

class Indexer:
    def __init__(self):
        self.solr_url = f'http://{HOST}:{PORT}/solr/'
        self.connection = pysolr.Solr(self.solr_url + CORE_NAME, always_commit=True, timeout=5000000)

    def do_initial_setup(self):
        delete_core()
        create_core()

    def create_documents(self, docs):
        print(self.connection.add(docs))


if __name__ == "__main__":
    i = Indexer()
    i.do_initial_setup()
    i.create_documents(collection)

