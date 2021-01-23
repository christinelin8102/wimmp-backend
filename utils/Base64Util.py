import base64


class Base64Util:
    def encryption(encryptionCode):
        bytesCode = encryptionCode.encode("utf-8")
        # 被编码的参数必须是二进制数据
        str_code = base64.b64encode(bytesCode)
        # print(str_code)
        return str_code

