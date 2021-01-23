import json
import traceback
import random
import logging
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from flask import make_response

from utils.ApiResponse import *
from view.PaymentTerm import PaymentTermSchema
from view.Vendor import VendorSchema
from model.PaymentTerm import ObjPaymentTerm
from model.ExchangeRate import ObjExchangeRate
from model.Vendor import ObjVendor
from io import StringIO
import csv
import pandas as pd

# from model.

paymentTermSchema = PaymentTermSchema()
vendorSchema = VendorSchema()

logger = logging.getLogger(__name__)


class UploadFileService:

    def uploadPaymentTerm(self, data):
        '''data to db Code, Payment_Term, Description'''

        print(data)
        try:
            s = str(data, 'utf-8')
        except:
            s = str(data, 'Big5')
        data = StringIO(s)
        rows = pd.read_csv(data)
        total_row = len(rows)
        successcount = 0
        updatecount = 0

        for i in range(0, total_row):
            print(i)
            rowdata = rows.iloc[i]
            payment_term = rowdata.get('Payment_Term', None)
            payment_code = rowdata.get('Code', None)
            description = rowdata.get('Description', None)

            # print(pa.get('Payment_Term'))
            objPaymentTerm = ObjPaymentTerm.query.filter(
                ObjPaymentTerm.payment_term == payment_term).first()
            if objPaymentTerm is None:
                paymentterm = ObjPaymentTerm(payment_term=payment_term,
                                             payment_code=payment_code,
                                             description=description)
                paymentterm.create(paymentterm)
                successcount += 1
            else:
                objPaymentTerm.description = description
                objPaymentTerm.update()
                updatecount += 1

        returnStr = 'success data count:' + str(successcount) + ' updata data count:' + str(updatecount)
        return ApiResponse.emitSuccessOutput(returnStr)

    def uploadVendorList(self, data):
        '''data to db code, Brief_Name, Full_Name, Chinese_Full_Name, Loacation'''

        print(data)
        try:
            s = str(data, 'utf-8')
        except:
            s = str(data, 'Big5')
        data = StringIO(s)
        rows = pd.read_csv(data)
        total_row = len(rows)
        successcount = 0
        updatecount = 0

        for i in range(0, total_row):
            rowdata = rows.iloc[i]
            vendor_code = rowdata.get('Code', None)
            vendor_code = str(vendor_code)
            brief_name = rowdata.get('Brief_Name', None)
            full_name = rowdata.get('Full_Name', None)
            chinese_full_name = rowdata.get('Chinese_Full_Name', None)
            location = rowdata.get('Location', None)
            objVendor = ObjVendor.query.filter(ObjVendor.vendor_code == vendor_code).first()
            if objVendor is None:
                vendor = ObjVendor(vendor_code=vendor_code,
                                   brief_name=brief_name,
                                   full_name=full_name,
                                   chinese_full_name=chinese_full_name,
                                   location=location
                                   )
                vendor.create(vendor)
                successcount += 1

            else:
                objVendor.brief_name = brief_name
                objVendor.full_name = full_name
                objVendor.chinese_full_name = chinese_full_name
                objVendor.location = location
                objVendor.update()
                updatecount += 1

        returnStr = 'success data count:' + str(successcount) + ' updata data count:' + str(updatecount)
        return ApiResponse.emitSuccessOutput(returnStr)

    def upExRate(self, data):
        '''for rate insert db'''
        '''data to db Code, Payment_Term, Description'''

        print(data)
        try:
            s = str(data, 'utf-8')
        except:
            s = str(data, 'Big5')
        data = StringIO(s)
        rows = pd.read_csv(data)
        total_row = len(rows)
        successcount = 0
        updatecount = 0

        for i in range(0, total_row):
            rowdata = rows.iloc[i]
            kurst = rowdata.get('ExRt')
            valid_from = rowdata.get('Valid from')
            ratio_from = rowdata.get('Ratio(from)')
            currency_from = rowdata.get('From currency')
            rate = rowdata.get('Exchange Rate')
            ratio_to = rowdata.get('Ratio(to)'),
            currency_to = rowdata.get('To-currency')
            exchangerate = ObjExchangeRate(kurst=kurst,
                                           valid_from=valid_from,
                                           ratio_from=ratio_from,
                                           currency_from=currency_from,
                                           rate=rate,
                                           ratio_to=ratio_to,
                                           currency_to=currency_to
                                           )
            successcount += 1
            print(exchangerate)
            exchangerate.create(exchangerate)

        returnStr = 'success data count:' + str(successcount) + ' updata data count:' + str(updatecount)
        return ApiResponse.emitSuccessOutput(returnStr)

    def downloadPaymentToCSV(self):

        objVendor = ObjPaymentTerm.query
        result = paymentTermSchema.dump(objVendor, many=True)
        df = pd.DataFrame(result)
        execel_file = StringIO()
        df.to_csv(execel_file, encoding='utf-8')
        csv_output = execel_file.getvalue()
        execel_file.close()
        response = make_response(csv_output)
        response.headers["Content-Disposition"] = "attachment; filename=latestPaymentTerm.csv"
        response.headers["Content-Type"] = "text/csv"
        return response

    def downloadVendorToCSV(self):

        objVendor = ObjVendor.query
        result = vendorSchema.dump(objVendor, many=True)
        df = pd.DataFrame(result)
        execel_file = StringIO()
        df.to_csv(execel_file, encoding='utf-8')
        csv_output = execel_file.getvalue()
        execel_file.close()
        response = make_response(csv_output)
        response.headers["Content-Disposition"] = "attachment; filename=latestVendorList.csv"
        response.headers["Content-Type"] = "text/csv"
        return response
