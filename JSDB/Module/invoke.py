import json
import pretty_errors

def invoke_json_path(category, get):
    print("【JOINED】")
    path = f"./JSDB/Commands/{str(category)}/{str(get)}.json"
    return path
