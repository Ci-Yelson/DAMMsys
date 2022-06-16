import hashlib

from dammsys import settings

def md5(data):
    salt = settings.SECRET_KEY.encode('utf-8')
    en = hashlib.md5(salt)
    en.update(data.encode('utf-8'))
    return en.hexdigest()