import hashlib

def generate_doc_id(text:str)->str:
    return hashlib.md5(text.encode('utf-8')).hexdigest()