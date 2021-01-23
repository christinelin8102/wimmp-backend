
# app = Flask(__name__)
# # 设置配置
# app.config['CACHE_TYPE'] = 'simple'  # 使用本地python字典进行存储, 一级缓存
# app.config['CACHE_DEFAULT_TIMEOUT'] = 5 * 60  # 默认过期时间 5分钟
#
# # 创建缓存对象
# cache = Cache(app)

# cache = SimpleCache()
#
#

class CacheInfo:

    def dictSet(self,sessionDict,key,value):
        if key and sessionDict:
            sessionDict = {key:value}
            return sessionDict

    def dicGet(self,dicName,key):
        if dicName and key:
            return dicName[key]

    def dicDelete(self,sessionDict,key):
        # del dict['Name'] # 删除键 'Name'
        if sessionDict and key:
            del sessionDict[key]


    #  @cache.memoize(60)
    # def add(self,a, b):
    #     return "11111"
    #
    # @cache.memoize(60)
    # def sub(a, b):
    #     return a - b - random.randrange(0, 1000)


#     pass
    # 从缓存中通过Key取到数据
    # def infoKeyGet(self,infoKey):
    #     rv = cache.get(infoKey)
    #     if rv is None:
    #         return rv
    #     else:
    #         return None
    #
    # # 将数据 set进缓存 key value 过期时间
    # def infoKeySet(self,infoKey, infoValue):
    #     if infoKey is None:
    #         cache.set(infoKey, infoValue)
    #         print("--------------------------------------------")

    # if x > 0:
    #         return x
    #     else:
    #         return 0
    # flag = False
    # name = 'luren'
    # if name == 'python':  # 判断变量是否为 python
    #     flag = True  # 条件成立时设置标志为真
    #     print
    #     'welcome boss'  # 并输出欢迎信息
    # else:
    #     print
    #     name



    # 对无参数的路由响应进行缓存
    # @app.route('/')
    # @cache.cached(timeout=60)
    # def index(self):
    #     num = random.randint(0, 9)
    #     print(num)
    #     return str(num)
    #
    # # demo1/11   demo1/12 的缓存结果会做区分
    # @app.route('/demo1/<user_id>')
    #
    # @cache.memoize(timeout=30)
    # def demo1(user_id):
    #     num = random.randint(0, 9)
    #     print(num)
    #     return str(num)
    #
    # # 对自定义函数设置缓存
    # @cache.cached(timeout=20)
    # def func1(self):
    #     num = random.randint(0, 9)
    #     print(num)
    #     return str(num)
    #
    # # 可以对指定的数据进行缓存
    # @app.route('/demo2')
    # def loginCacheInfo(self,infoKey,infoValue,timeout):
    #     print('demo2')
    #     cache.set(infoKey, infoValue, timeout=30)
    #
    #     return 'demo2'
    #
    # # 取出缓存
    # @app.route('/demo3')
    # def getForCache(self,infoKey):
    #     infoKey = cache.get(infoKey)
    #     if infoKey != None and ''
    #     print(name)
    #     return 'demo3'
