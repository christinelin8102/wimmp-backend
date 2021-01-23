import jwt
from flask import session
from flask import request
from utils.ApiResponse import *

SK_CRM_USER_INFO = "user_info"
E_CODE_USER_NOT_LOGIN = 0


def checkToken(func):
    def dec_func(*args, **kwargs):
        if not request.headers.get('Authorization') or request.headers.get('Authorization') is None :
            # user not login, return error msg directly. http code put to 403(forbidden)
            return ApiResponse.emitErrorOutput('401', u'Missed Authorization token', str(func), 401)
        else:
            encoded_jwt = request.headers.get('Authorization')
            decoded = jwt.decode(encoded_jwt, verify=False)
            name = decoded.get('unique_name')
            args += (name,)

            return func(*args, **kwargs)

    return dec_func


def checkSession(func):
    def dec_func(*args, **kwargs):
        # check if user has logined, otherwise send error information.
        print("We enter into here")

        if request.headers.get('Authorization') == "":
            # user not login, return error msg directly. http code put to 403(forbidden)
            return ApiResponse.emitErrorOutput(E_CODE_USER_NOT_LOGIN, u'用戶未登入，請登入後再執行操作', str(func))
        else:
            return func(*args, **kwargs)

    return dec_func


def getSessionInfo():
    encoded_jwt = request.headers.get('Authorization')
    decoded = jwt.decode(encoded_jwt, verify=False)
    return decoded.get('preferred_username')


def getSessionVal(key, defaultValue):
    # encoded_jwt = request.headers.get('Authorization')
    # decoded = jwt.decode(encoded_jwt, verify=False)

    #val = defaultValue
    # so = getSessionInfo()
    # if so != None and so != "":
    #     val = so.get(key)
    # return decoded.get('preferred_username')
    return 104


def setSessionInfo(name, loginid, roleid, rolename, logintime, token, customerId):
    data = {
        "name": name,
        "userLoginId": loginid,
        "roleId": roleid,
        "roleName": rolename,
        "loginTime": logintime,
        "token": token,
        "customerId": customerId
    }
    session[SK_CRM_USER_INFO] = data


def clearSession():
    session[SK_CRM_USER_INFO] = None
