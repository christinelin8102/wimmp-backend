import psycopg2
import random

def add_data():
    # Update connection string information
    host = "mmp-postgresql.postgres.database.azure.com"
    dbname = "wisdom_fask_database"
    user = "admin_mmp@mmp-postgresql"
    password = "Changeit!123"
    sslmode = "require"

    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = conn.cursor()
    print("igotin")

    Query = """SELECT * FROM public."IMPC_dummy";"""
    cursor.execute("SELECT * FROM public.\"IMPC_dummy\"")
    rows = cursor.fetchall()
    print(rows)

    count = 0

    # # Drop previous table of same name if one exists
    # cursor.execute("DROP TABLE IF EXISTS inventory;")
    # print("Finished dropping table (if existed)")

    # # Create a table
    # cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
    # print("Finished creating table")

    # BUYN = "張妮"
    # PONO = "2005JB51341"
    # POLN = "1"
    # REMARK = ""
    # RDAT = "2020/6/1 08:19"
    # VEND = "628770"
    # VDESC = "上海維諾網絡科技有限公司"
    # VEND2 = ""
    # SPEC = "CC001 M1 1F IDL招聘服務中心新增OA點"
    # RMAK = "五類非屏蔽雙絞線,長度約70-100米,兩端壓AMP 5類非屏蔽水晶頭"
    # PRQTY = 5
    # OQTY = 5
    # UNIT = "點"
    # OPRC = 225
    # PRIC = 225
    # TAXD = 9
    # DELI = "DAP CNKUS"
    # DDAT = "2020/6/15 00:00"
    # PAYM = "YKC0"
    # POCURR = "RMB"
    # PRCURR = "RMB"
    # PRNO = "P202005260501"
    # PRLN = "1"
    # LASTAPPROVEDATE = "2020/5/29 09:21"
    # APPN = "ANGEL SHA"
    # APPD = "MEL310"
    # CDEP = "MEH000"
    # PROJECTCODE = ""
    # AMNT = 1125
    # RTNO = "128335"
    # RTLN = "1"
    # RQTY = 5
    # PMNO = "FPA2007240172"
    # CRTDATE = "2020/8/7 00:03"
    # POTYPE = "N" #N/M
    # FORM_CODE = "N_PO" #N_PO/M_PO
    # POFLAG = "N" #D/C/N
    # REIMBURSE = "N" #N/Y
    # PARTNO = "KAF01.0062"
    # COMPANY = "L230"
    # PRTY = "生產用設備(生產用設備及架線工程)"
    # WCSNONAME = "架線工程類"
    # IMPN = ""
    # RECEIVEDATE = ""
    # SSTATUS = "Approve" #Approve/p/r/a
    # ADATE = ""
    # PLANTCODE = "F232"
    # ONAME = "記錄價"
    # HSFNAME = ""
    # PORG = ""
    # PDAT = ""

    while count < 5:

        BUYN = random.choice(['張妮','張三','李四','王五','陳六','王七'])
        PONO = str(random.randint(2000,2020)) + 'JB' + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) #'2005JB51341'
        POLN = str(random.randint(1,9))
        REMARK = ''
        RDAT = '2020/6/1 08:19'
        # VEND = '628770'
        # VDESC = '上海維諾網絡科技有限公司'
        VEND = ''
        VDESC = ''
        VD = [{'VEND': '628770', 'VDESC': '上海維諾網絡科技有限公司'},
              {'VEND': '960032', 'VDESC': '緯視晶光電(昆山)有限公司'},
              {'VEND': '960033', 'VDESC': '緯創資通(菲律賓)股份有限公司'},
              {'VEND': '960037', 'VDESC': 'Wistron K.K.'},
              {'VEND': '960075', 'VDESC': 'AIPG之海外控股公司'},
              {'VEND': '960088', 'VDESC': 'SMS Infocomm Corporation'},
              {'VEND': '960125', 'VDESC': '昆山緯隆供應鏈管理有限公司'}]

        Vc = random.choice(VD)
        VEND = Vc['VEND']

        VEND2 = ''
        SPEC = 'CC001 M1 1F IDL招聘服務中心新增OA點'
        RMAK = '五類非屏蔽雙絞線,長度約70-100米,兩端壓AMP 5類非屏蔽水晶頭'
        PRQTY = random.randint(1,100000)
        OQTY = random.randint(1,100000)
        UNIT = '點'
        OPRC = random.randint(1,100000)
        PRIC = random.randint(1,100000)
        TAXD = random.randint(1,50)
        DELI = 'DAP CNKUS'
        DDAT = '2020/6/15 00:00'
        PAYM = random.choice(['YKC0','YK30','YJ30','YHH0','YEH0','YD75','YC90','YA60','Y270','Y75F'])
        POCURR = random.choice(['RMB','NTD','USD'])
        PRCURR = random.choice(['RMB','NTD','USD'])
        PRNO = 'P' + str(random.randint(2000,2019))+ str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))+ str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
        PRLN = str(random.randint(1,9))
        LASTAPPROVEDATE = '2020/5/29 09:21'
        APPN = 'ANGEL SHA'
        APPD = 'MEL310'
        CDEP = 'MEH000'
        PROJECTCODE = ''
        AMNT = 1125
        RTNO = '128335'
        RTLN = str(random.randint(1,9))
        RQTY = random.randint(1,100000)
        PMNO = 'FPA2007240172'
        CRTDATE = '2020/8/7 00:03'
        POTYPE = random.choice(['N','M'])  # N/M
        FORM_CODE = POTYPE+'_PO'  # N_PO/M_PO
        POFLAG = random.choice(['N','D','C'])  # D/C/N
        REIMBURSE = random.choice(['N','Y'])  # N/Y
        PARTNO = 'KAF01.0062'
        COMPANY = 'L230'
        PRTY = '生產用設備(生產用設備及架線工程)'
        WCSNONAME = '架線工程類'
        IMPN = ''
        RECEIVEDATE = ''
        SSTATUS = random.choice(['a','p','r','Approve'])  # Approve/p/r/a
        ADATE = '2020/8/15 00:00'
        PLANTCODE = random.choice(['F232','F601','F236','F237','F7B1','F7B2','F555','F261','F741','F139','F337','F5A1','F5A2','F595','F2C1'])
        ONAME = '記錄價'
        HSFNAME = ''
        PORG = ''
        PDAT = ''
        count = count + 1

        cursor.execute("INSERT INTO public.\"IMPC_dummy\" "
                       "(\"BUYN\",\"PONO\",\"POLN\",\"REMARK\",\"RDAT\","
                       "\"VEND\",\"VDESC\",\"VEND2\",\"SPEC\",\"RMAK\","
                       "\"PRQTY\",\"OQTY\",\"UNIT\",\"OPRC\",\"PRIC\","
                       "\"TAXD\",\"DELI\",\"DDAT\",\"PAYM\",\"POCURR\","
                       "\"PRCURR\",\"PRNO\",\"PRLN\",\"LASTAPPROVEDATE\",\"APPN\","
                       "\"APPD\",\"CDEP\",\"PROJECTCODE\",\"AMNT\",\"RTNO\","
                       "\"RTLN\",\"RQTY\",\"PMNO\",\"CRTDATE\",\"POTYPE\","
                       "\"FORM_CODE\",\"POFLAG\",\"REIMBURSE\",\"PARTNO\",\"COMPANY\","
                       "\"PRTY\",\"WCSNONAME\",\"IMPN\",\"RECEIVEDATE\",\"SSTATUS\","
                       "\"ADATE\",\"PLANTCODE\",\"ONAME\",\"HSFNAME\",\"PORG\",\"PDAT\") "
                       "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                       (BUYN,PONO,POLN,REMARK,RDAT,
                        VEND,VDESC,VEND2,SPEC,RMAK,
                        PRQTY,OQTY,UNIT,OPRC,PRIC,
                        TAXD,DELI,DDAT,PAYM,POCURR,
                        PRCURR,PRNO,PRLN,LASTAPPROVEDATE,APPN,
                        APPD,CDEP,PROJECTCODE,AMNT,RTNO,
                        RTLN,RQTY,PMNO,CRTDATE,POTYPE,
                        FORM_CODE,POFLAG,REIMBURSE,PARTNO,COMPANY,
                        PRTY,WCSNONAME,IMPN,RECEIVEDATE,SSTATUS,
                        ADATE,PLANTCODE,ONAME,HSFNAME,PORG,PDAT))
        conn.commit()
        print(count)
        # cursor.close()
        # conn.close()


    # Insert some data into the table
    # cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", 150))
    # cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("orange", 154))
    # cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("apple", 100))
    # print("Inserted 3 rows of data")

    # Clean up
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    add_data()