from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

SECRET_KEY = "SECRET_KEY"


def generate_auth_token(data,expiration=3600 * 24 * 30):
    """
    生成token
    :param data: 用于加密在token中的数据
    :param expiration: 过期时间
    :return: 
    """
    s = Serializer(SECRET_KEY, expires_in=expiration)
    return s.dumps(data).decode("utf-8")

def verify_auth_token(token):
    """
    验证token
    :param token: 包含数据的token
    :return: 返回token中包含的数据
    """
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired as e:
        return None  # valid token, but expired
    except BadSignature as e:
        return None  # invalid token
    return data            