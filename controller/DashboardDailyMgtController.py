#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/1/14
# @Author : Christine Lin
# @Site :
# @File : DashboardDailyMgtController.py
# @Software: Pycharm
from dateutil.relativedelta import relativedelta
from flask_restplus import Namespace, Resource, fields

from service.DashboardDailyMgtService import *
from utils.ControllerUtils import *
from flask import abort

api = Namespace('dashboardDailyMgt', description='dashboard Daily Management Data')

dailyMgtDashboardService = DashboardDailyMgtService()

period = api.model('period', {
    'startdate': fields.Integer(required=True, description="startdate TimeStamp", help="startdate cannot be blank."),
    'enddate': fields.Integer(required=True, description="enddate TimeStamp", help="enddate cannot be blank.")
})

request_fields = api.model('request_model', {
    'vendor': fields.Boolean(required=True, description="vendor", help="vendor cannot be blank."),
    'reimburse': fields.Boolean(required=True, description="reimburse", help="reimburse cannot be blank."),
    'nonreimburse': fields.Boolean(required=True, description="nonreimburse", help="nonreimburse cannot be blank."),
    'bg': fields.String(required=True, description="bg", help="bg cannot be blank."),
    'site': fields.String(required=True, description="site", help="site cannot be blank."),
    'plant': fields.String(required=True, description="plant", help="plant cannot be blank."),
    'period': fields.Nested(period, description="period", help="period cannot be blank.")
})

sort_fields = api.model('sort', {
    'field': fields.String(required=True, description="column name", help="field cannot be blank."),
    'value': fields.String(required=True, description="desc or asc", help="value cannot be blank.")
})

filter1_fields = api.model('filter1', {
    'field': fields.String(required=True, description="column name", help="field cannot be blank."),
    'value': fields.String(required=True, description="desc or asc", help="value cannot be blank.")
})

filter2_fields = api.model('filter2', {
    'field': fields.String(required=True, description="column name", help="field cannot be blank."),
    'value': fields.Integer(required=True, description="integer", help="value cannot be blank."),
    'operator': fields.String(required=True, description="lt or le or eq or ne or ge or gt",
                              help="operator cannot be blank.")
})

request_DailyMgt_page_main = api.model('request_DailyMgt_page_main_page_model', {
    'vendor': fields.Boolean(required=True, description="vendor", help="vendor cannot be blank."),
    'reimburse': fields.Boolean(required=True, description="reimburse", help="reimburse cannot be blank."),
    'nonreimburse': fields.Boolean(required=True, description="nonreimburse", help="nonreimburse cannot be blank."),
    'bg': fields.String(required=True, description="bg", help="bg cannot be blank."),
    'site': fields.String(required=True, description="site", help="site cannot be blank."),
    'plant': fields.String(required=True, description="plant", help="plant cannot be blank."),
    'period': fields.Nested(period, description="period", help="period cannot be blank."),
    'pageSize': fields.Integer(required=True, description="pageSize", help="pageSize cannot be blank."),
    'pageNo': fields.Integer(required=True, description="pageNo", help="pageNo cannot be blank."),
    'sort': fields.List(fields.Nested(sort_fields), description="sort", help="sort cannot be blank."),
    'filter': fields.List(fields.Nested(filter1_fields), description="filter", help="filter cannot be blank.")
})

request_withname_fields = api.model('request_model', {
    'vendor': fields.Boolean(required=True, description="vendor", help="vendor cannot be blank."),
    'reimburse': fields.Boolean(required=True, description="reimburse", help="reimburse cannot be blank."),
    'nonreimburse': fields.Boolean(required=True, description="nonreimburse", help="nonreimburse cannot be blank."),
    'bg': fields.String(required=True, description="bg", help="bg cannot be blank."),
    'site': fields.String(required=True, description="site", help="site cannot be blank."),
    'plant': fields.String(required=True, description="plant", help="plant cannot be blank."),
    'vendorname': fields.String(required=True, description="vendorname", help="vendorname cannot be blank."),
    'period': fields.Nested(period, description="period", help="period cannot be blank.")
})
request_DailyMgt_page_subVendor = api.model('request_DailyMgt_page_subVendor_model', {
    'vendor': fields.Boolean(required=True, description="vendor", help="vendor cannot be blank."),
    'reimburse': fields.Boolean(required=True, description="reimburse", help="reimburse cannot be blank."),
    'nonreimburse': fields.Boolean(required=True, description="nonreimburse", help="nonreimburse cannot be blank."),
    'bg': fields.String(required=True, description="bg", help="bg cannot be blank."),
    'site': fields.String(required=True, description="site", help="site cannot be blank."),
    'plant': fields.String(required=True, description="plant", help="plant cannot be blank."),
    'period': fields.Nested(period, description="period", help="period cannot be blank."),
    'pageSize': fields.Integer(required=True, description="pageSize", help="pageSize cannot be blank."),
    'pageNo': fields.Integer(required=True, description="pageNo", help="pageNo cannot be blank."),
    'sort': fields.List(fields.Nested(sort_fields), description="sort", help="sort cannot be blank."),
    'filter': fields.List(fields.Nested(filter1_fields), description="filter", help="filter cannot be blank."),
    'vendorName': fields.String(required=True, description="vendorName", help="vendorName cannot be blank.")
})
request_page_fields = api.model('request_page_model', {
    'paymentterm': fields.String(required=True, description="paymentterm", help="paymentterm cannot be blank."),
    'process': fields.Boolean(required=True, description="process", help="process cannot be blank."),
    'notprocess': fields.Boolean(required=True, description="notprocess", help="notprocess cannot be blank."),
    'bg': fields.String(required=True, description="bg", help="bg cannot be blank."),
    'site': fields.String(required=True, description="site", help="site cannot be blank."),
    'plant': fields.String(required=True, description="plant", help="plant cannot be blank."),
    'period': fields.Nested(period, description="period", help="period cannot be blank."),
    'pageSize': fields.Integer(required=True, description="pageSize", help="pageSize cannot be blank."),
    'pageNo': fields.Integer(required=True, description="pageNo", help="pageNo cannot be blank."),
    'sort': fields.List(fields.Nested(sort_fields), description="sort", help="sort cannot be blank."),
    'filter': fields.List(fields.Nested(filter1_fields), description="filter", help="filter cannot be blank.")
})

request_DailyMgt_page_subPo = api.model('request_DailyMgt_page_subPo_model', {
    'vendor': fields.Boolean(required=True, description="vendor", help="vendor cannot be blank."),
    'reimburse': fields.Boolean(required=True, description="reimburse", help="reimburse cannot be blank."),
    'nonreimburse': fields.Boolean(required=True, description="nonreimburse", help="nonreimburse cannot be blank."),
    'bg': fields.String(required=True, description="bg", help="bg cannot be blank."),
    'site': fields.String(required=True, description="site", help="site cannot be blank."),
    'plant': fields.String(required=True, description="plant", help="plant cannot be blank."),
    'period': fields.Nested(period, description="period", help="period cannot be blank."),
    'pageSize': fields.Integer(required=True, description="pageSize", help="pageSize cannot be blank."),
    'pageNo': fields.Integer(required=True, description="pageNo", help="pageNo cannot be blank."),
    'sort': fields.List(fields.Nested(sort_fields), description="sort", help="sort cannot be blank."),
    'filter': fields.List(fields.Nested(filter1_fields), description="filter", help="filter cannot be blank."),
    'pCode': fields.String(required=True, description="pCode", help="pCode cannot be blank.")
})

request_DailyMgt_page_poLine = api.model('request_DailyMgt_page_poLine_model', {
    'vendor': fields.Boolean(required=True, description="vendor", help="vendor cannot be blank."),
    'reimburse': fields.Boolean(required=True, description="reimburse", help="reimburse cannot be blank."),
    'nonreimburse': fields.Boolean(required=True, description="nonreimburse", help="nonreimburse cannot be blank."),
    'bg': fields.String(required=True, description="bg", help="bg cannot be blank."),
    'site': fields.String(required=True, description="site", help="site cannot be blank."),
    'plant': fields.String(required=True, description="plant", help="plant cannot be blank."),
    'period': fields.Nested(period, description="period", help="period cannot be blank."),
    'pageSize': fields.Integer(required=True, description="pageSize", help="pageSize cannot be blank."),
    'pageNo': fields.Integer(required=True, description="pageNo", help="pageNo cannot be blank."),
    'sort': fields.List(fields.Nested(sort_fields), description="sort", help="sort cannot be blank."),
    'filter': fields.List(fields.Nested(filter1_fields), description="filter", help="filter cannot be blank."),
    'po_no': fields.String(required=True, description="po_no", help="po_no cannot be blank.")
})


# request_DailyMgt_page_main = api.extend('request_DailyMgt_page_main_page_model', request_fields, {
#     'pageSize': fields.Integer(required=True, description="pageSize", help="pageSize cannot be blank."),
#     'pageNo': fields.Integer(required=True, description="pageNo", help="pageNo cannot be blank."),
#     'sort': fields.List(fields.Nested(sort_fields), description="sort", help="sort cannot be blank."),
#     'filter': fields.List(fields.Nested(filter1_fields), description="filter", help="filter cannot be blank.")
# })
#
# request_DailyMgt_page_subPo = api.extend('request_DailyMgt_page_subPo_model', request_DailyMgt_page_poMain, {
#     'pCode': fields.String(required=True, description="pCode", help="pCode cannot be blank.")
# })
#
# request_DailyMgt_page_poLine = api.extend('request_DailyMgt_page_poLine_model', request_DailyMgt_page_poMain, {
#     'pNo': fields.String(required=True, description="pNo", help="pNo cannot be blank.")
# })

@api.route('', methods=["GET", "POST", "DELETE", "PUT"])
class DashboardDailyMgtController(Resource):
    @api.route("/categories/amount")
    class categoriesAmountList(Resource):
        @api.expect(request_fields)
        def post(self):
            try:
                data = request.get_json()
                if data is None:
                    return "請求參數不能為空"
                req = ControllerUtils.handleRequestDailyMgtTableBody_purchaseOrPoOrPoline(data)
                return dailyMgtDashboardService.getTopTenList(req, DailyManagementPageTableCategoriesType.EIGHTCATEGORIES)
            except Exception as e:
                abort(500, e)

    @api.route("/pCode/pCodeChart")
    class getTopTenPCodeChart(Resource):
        @api.expect(request_fields)
        def post(self):
            try:
                data = request.get_json()
                if data is None:
                    return "請求參數不能為空"
                req = ControllerUtils.handleRequestBody(data)
                return dailyMgtDashboardService.getTopTenPCode(req)
            except Exception as e:
                abort(500, e)

    @api.route("/pCode/pCodeList")
    class getTopTenPCodeList(Resource):
        @api.expect(request_DailyMgt_page_main)
        def post(self):
            """取得Top ten project code List"""
            try:
                data = request.get_json()
                if data is None:
                    return "請求參數不能為空"
                req = ControllerUtils.handleRequestDailyMgtTableBody_purchaseOrPoOrPoline(data)

                return dailyMgtDashboardService.getTopTenList(req, DailyManagementPageTableCategoriesType.PCODE_TOP10)
            except Exception as e:
                abort(500, e)

    @api.route("/pCode/pCodePurchaseAmtPerSite")
    class getPCodePurchaseAmtPerSite(Resource):
        @api.expect(request_DailyMgt_page_subPo)
        def post(self):
            """取得Project code purchase Amount List"""
            try:
                data = request.get_json()
                if data is None:
                    return "請求參數不能為空"
                req = ControllerUtils.handleRequestDailyMgtTableBody_purchaseOrPoOrPoline(data)

                return dailyMgtDashboardService.getSubTable(req,
                                                            DailyManagementPageTableCategoriesType.PCODETOP10_PUCHASE_PER_SITE)
            except Exception as e:
                abort(500, e)

    @api.route("/pCode/polist")
    class getPCodePO(Resource):
        @api.expect(request_DailyMgt_page_subPo)
        def post(self):
            try:
                data = request.get_json()
                if data is None:
                    return "請求參數不能為空"
                req = ControllerUtils.handleRequestDailyMgtTableBody_purchaseOrPoOrPoline(data)

                return dailyMgtDashboardService.getSubTable(req,
                                                            DailyManagementPageTableCategoriesType.PCODE_PO_LIST)
            except Exception as e:
                abort(500, e)

    @api.route("/pCode/polinelist")
    class getPOLine(Resource):
        @api.expect(request_DailyMgt_page_poLine)
        def post(self):
            try:
                data = request.get_json()
                if data is None:
                    return "請求參數不能為空"
                req = ControllerUtils.handleRequestDailyMgtTableBody_purchaseOrPoOrPoline(data)

                return dailyMgtDashboardService.getSubTable(req,
                                                            DailyManagementPageTableCategoriesType.PO_LINE_LIST)
            except Exception as e:
                abort(500, e)

    @api.route("/pCode/buttonExport")
    class exportDataBycode(Resource):
        @api.expect(request_fields)
        def post(self):
            try:
                data = request.get_json()
                if data is None:
                    return "請求參數不能為空"
                req = ControllerUtils.handleRequestBody(data)
                p_code = data.get('pCode', None)
                if p_code is None or p_code == '':
                    return "P code 不能為空"
                return dailyMgtDashboardService.exportDataBycode(req, p_code)
            except Exception as e:
                abort(500, e)

    @api.route("/vendor/vendorChart")
    class getTopTenVendorChart(Resource):
        @api.expect(request_fields)
        def post(self):
            """取得vendor Top 10 Chart"""
            data = request.get_json()
            if data is None:
                return "請求參數不能為空"
            req = ControllerUtils.handleRequestBody(data)
            return dailyMgtDashboardService.getTopTenVendorChart(req)

    @api.route("/vendor/vendorList")
    class getTopTenVendorList(Resource):
        @api.expect(request_DailyMgt_page_main)
        def post(self):
            """取得vendor Top 10 List"""
            data = request.get_json()
            if data is None:
                return "請求參數不能為空"
            req = ControllerUtils.handleRequestDailyMgtTableBody_purchaseOrPoOrPoline(data)
            return dailyMgtDashboardService.getTopTenList(req, DailyManagementPageTableCategoriesType.VENDOR_TOP10)

    @api.route("/vendor/vendorPurchaseAmountPerSite")
    class getVendorPurchaseAmountPerSite(Resource):
        @api.expect(request_DailyMgt_page_subVendor)
        def post(self):
            """取得vendor Top 10 List"""
            data = request.get_json()
            if data is None:
                return "請求參數不能為空"
            req = ControllerUtils.handleRequestDailyMgtTableBody_purchaseOrPoOrPoline(data)
            return dailyMgtDashboardService.getSubTable(req,
                                                        DailyManagementPageTableCategoriesType.VENDORTOP10_PUCHASE_PER_SITE)
