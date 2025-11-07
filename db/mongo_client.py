from pymongo import MongoClient

def get_db():
    # ✅ Make sure this is ONE SINGLE LINE (no line breaks)
    CONNECTION_STRING = "mongodb+srv://poojasuresh1905_db_user:LFcNK2PZ1m16gUrN@cloud.ka3phqf.mongodb.net/library_db?retryWrites=true&w=majority"
    
    client = MongoClient(CONNECTION_STRING)
    return client['library_db']
