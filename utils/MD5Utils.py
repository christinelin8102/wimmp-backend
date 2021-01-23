import hashlib


class MD5Utils:

    def encryptionMD5(encryptionCode):
        if encryptionCode:
            enCode = hashlib.md5(encryptionCode.encode(encoding='UTF-8')).hexdigest()
        return enCode
