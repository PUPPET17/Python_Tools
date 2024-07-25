from datamuse import Datamuse

api = Datamuse()

print(api.suggest(s='fu',max_results=20))