'''
Have to change po_price to mmp_charge_in_ntd when data is ready!!!!!!!!!!!
'''

import json
from datetime import datetime
import pandas as pd
import numpy as np
from service.dataSerializer.IDataSerializer import IDataSerializer
from service.dataSerializer.GetDataService import GetDataService
import logging

logger = logging.getLogger(__name__)


def change_operator(operator):
    if operator == 'lt':
        return '<'
    elif operator == 'le':
        return '<='
    elif operator == 'eq':
        return '=='
    elif operator == 'ne':
        return '!='
    elif operator == 'ge':
        return '>='
    else:  # 'gt'
        return '>'


class DBPcodeListSQL(IDataSerializer):

    def __init__(self, bg_list, site_list, plant_list, start_score, end_score, vendor_type, reimburse_type, pageSize,
                 pageNo, sort_lst, filter_list):
        self.bg = bg_list
        self.site = site_list
        self.plant = plant_list
        self.s_score = start_score
        self.e_score = end_score
        self.vendor_type = vendor_type
        self.reimburse_type = reimburse_type
        self.pageSize = pageSize
        self.pageNo = pageNo
        self.sort = sort_lst
        self.filter = filter_list

        logger.debug('''------DailyMngmPcode Param: \
            \n
            BG: {0},
            \n
            SITE: {1},
            \n
            PLANT: {2},
            \n
            score between: {3} and {4}, 
            \n
            isIgnoreVendor: {5}, Reimburse: {6}'''.format(self.bg, self.site, self.plant,
                                                          self.s_score, self.e_score,
                                                          self.vendor_type, self.reimburse_type))

    def serialize(self):
        # transfer date for SQL
        s_date = datetime.fromtimestamp(self.s_score).strftime("%Y-%m-%d 00:00:00")  # %H:%M:%S
        e_date = datetime.fromtimestamp(self.e_score).strftime("%Y-%m-%d 23:59:59")
        logger.debug("# ----- getPcodeSortList SQL time range: {0} and {1}".format(s_date, e_date))
        # check if excluding vendor or not
        if self.vendor_type == "Y":
            sq = 'select vendor_code from public."VENDORS";'
            vendor = GetDataService.getwistrondata(self, sqlquery=sq)
            vendor = [x[0] for x in vendor]
            vend_in_list = "AND table1.mmp_vendor_code NOT IN ('" + "', '".join(vendor) + "')"
        else:
            vend_in_list = ''
        # check reimburse type (0:all, 1:reimburse, 2:non-reimburse)
        if self.reimburse_type == 1:
            reimburse_in_list = 'AND table1.reimburse = true'
        elif self.reimburse_type == 2:
            reimburse_in_list = 'AND table1.reimburse = false'
        else:
            reimburse_in_list = ''
        # paging by (pageSize, pageNo)
        paging = 'LIMIT {0} OFFSET {1}'.format(self.pageSize, self.pageSize * (self.pageNo - 1))
        # bg、site、plant
        if self.bg is None:
            bg_cond = ""
        else:
            bg_cond = "AND table1.mmp_bg in ('" + "', '".join(self.bg) + "') "
        if self.site is None:
            site_cond = ""
        else:
            site_cond = "AND table1.mmp_site in ('" + "', '".join(self.site) + "') "
        if self.plant is None:
            plant_cond = ""
        else:
            plant_cond = "AND table1.charge_plant_code in ('" + "', '".join(self.plant) + "') "
        # sort condition
        if self.sort is None:
            # TODO:
            # sort_cond = 'order by SUM(table2.mmp_charge_in_ntd) desc '
            sort_cond = 'order by SUM(table3.po_price) desc '
        else:
            sort_cond = 'order by '
            for i in range(0, len(self.sort)):
                if self.sort[i]['field'] == 'po_no':
                    # sort_cond = sort_cond + 'COUNT(DISTINCT table1.po_no) ' + self.sort[i]['value'] +', '
                    sort_cond = sort_cond + 'po_no ' + self.sort[i]['value'] + ', '
                elif self.sort[i]['field'] == 'mmp_charge_in_ntd':
                    # sort_cond = sort_cond + 'SUM(table2.mmp_charge_in_ntd) ' + self.sort[i]['value'] +', '
                    sort_cond = sort_cond + 'SUM(table3.po_price) ' + self.sort[i]['value'] + ', '
                elif self.sort[i]['field'] == 'mmp_charge_code':
                    sort_cond = sort_cond + 'table2.mmp_charge_code ' + self.sort[i]['value'] + ', '
                else:
                    sort_cond = sort_cond + 'table1.mmp_bg ' + self.sort[i]['value'] + ', '
            sort_cond = sort_cond[:-2] + ' '
        # filter condition
        if self.filter is None:
            filter_cond = ''
            having_cond = ''
        else:
            filter_cond = ''
            having_cond = ''
            for i in range(0, len(self.filter)):
                if self.filter[i]['field'] == 'po_no':
                    if having_cond == '':
                        having_cond = having_cond + 'HAVING COUNT(DISTINCT table1.po_no) ' + change_operator(
                            self.filter[i]['operator']) + ' ' + str(self.filter[i]['value']) + ' '
                    else:
                        having_cond = having_cond + 'AND COUNT(DISTINCT table1.po_no) ' + change_operator(
                            self.filter[i]['operator']) + ' ' + str(self.filter[i]['value']) + ' '
                elif self.filter[i]['field'] == 'mmp_charge_in_ntd':
                    if having_cond == '':
                        # having_cond = having_cond + 'HAVING SUM(table2.mmp_charge_in_ntd) ' + change_operator(self.filter[i]['operator']) + ' ' + self.filter[i]['value'] +' '
                        having_cond = having_cond + 'HAVING SUM(table3.po_price) ' + change_operator(
                            self.filter[i]['operator']) + ' ' + str(self.filter[i]['value']) + ' '
                    else:
                        # having_cond = having_cond + 'AND SUM(table3.po_price) ' + change_operator(self.filter[i]['operator']) + ' ' + str(self.filter[i]['value']) +' '
                        having_cond = having_cond + 'AND SUM(table3.po_price) ' + change_operator(
                            self.filter[i]['operator']) + ' ' + str(self.filter[i]['value']) + ' '
                elif self.filter[i]['field'] == 'mmp_charge_code':
                    filter_cond = filter_cond + "AND table2.mmp_charge_code in ('" + self.filter[i]['value'] + "') "
                else:
                    filter_cond = filter_cond + "AND table1.mmp_bg in ('" + self.filter[i]['value'] + "') "
        # --- using po_price for amount --- #
        sqlquery1 = """SELECT table1.mmp_bg, table2.mmp_charge_code, SUM(table3.po_price) mmp_charge_in_ntd, COUNT(DISTINCT table1.po_no) po_no \
        FROM public."{8}" table1 \
        FULL OUTER JOIN public."{9}" table2 on ( table1.po_no = table2.po_no ) \
        FULL OUTER JOIN public."{10}" table3 on ( table1.po_no = table3.po_no ) \
        WHERE table1.po_date between '{0}'::timestamp and '{1}'::timestamp \
        {5} {6} {7} \
        {2} {3} \
        {12} \
        group by table1.mmp_bg, table2.mmp_charge_code \
        {13} \
        {11} \
        {4};""".format(s_date, e_date, vend_in_list, reimburse_in_list, paging,
                       bg_cond, site_cond, plant_cond,
                       "PURCHASE_ORDER", "PURCHASE_ORDER_CHARGE", "PURCHASE_ORDER_DETAIL",
                       sort_cond, filter_cond, having_cond)
        logger.debug("# ----- getPcodeSortList Data SQL: {}".format(sqlquery1))
        # sql for totalPage and totalCount
        sqlquery2 = """WITH report AS (SELECT table1.mmp_bg, table2.mmp_charge_code, SUM(table3.po_price) , COUNT(DISTINCT table1.po_no) \
        FROM public."{7}" table1 \
        FULL OUTER JOIN public."{8}" table2 on ( table1.po_no = table2.po_no ) \
        FULL OUTER JOIN public."{9}" table3 on ( table1.po_no = table3.po_no ) \
        WHERE table1.po_date between '{0}'::timestamp and '{1}'::timestamp \
        {4} {5} {6} \
        {2} {3} \
        {10} \
        group by table1.mmp_bg, table2.mmp_charge_code \
        {11} ) \
        SELECT count(*) count from  report;""".format(s_date, e_date, vend_in_list, reimburse_in_list,
                                                      bg_cond, site_cond, plant_cond,
                                                      "PURCHASE_ORDER", "PURCHASE_ORDER_CHARGE",
                                                      "PURCHASE_ORDER_DETAIL",
                                                      filter_cond, having_cond)
        logger.debug("# ----- getPcodeSortList Paging SQL: {}".format(sqlquery2))
        try:
            output = {}
            pag_result = GetDataService.getwistrondata(self, sqlquery=sqlquery2)
            pag_result = pd.DataFrame(pag_result)
            if pag_result[0][0] > 0:
                if pag_result[0][0] / self.pageSize > pag_result[0][0] // self.pageSize:
                    output['totalPage'] = pag_result[0][0] // self.pageSize + 1
                else:
                    output['totalPage'] = pag_result[0][0] // self.pageSize
                output['totalCount'] = pag_result[0][0]
            result = GetDataService.getwistrondata(self, sqlquery=sqlquery1)
            result = pd.DataFrame(result)
            if result.shape[0] > 0:
                result.columns = ['mmp_bg', 'mmp_charge_code', 'mmp_charge_in_ntd', 'po_no']
                result['mmp_charge_in_ntd'] = result['mmp_charge_in_ntd'].astype(float)
                result = result.dropna(subset=['mmp_charge_in_ntd']).reset_index(drop=True)
                logger.debug("# ----- getPcodeSortList Result: {}".format(result))
                result = result.to_dict('records')

                for index, d in enumerate(result):
                    d['rank'] = index + 1 + (self.pageSize * self.pageNo - 1)
                output['data'] = json.dumps(result)
                output['totalPage'] = int(output['totalPage'])
                output['totalCount'] = int(output['totalCount'])
                return output
            else:
                logger.debug("# ----- No Matching data in DataBase!!!")
                return None
        except Exception as ex:
            logger.debug("# ----- getPcodeSortList Fail! Reason: {}".format(ex))
            return None
