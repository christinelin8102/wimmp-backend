#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/17
# @Author : Alex Chen
# @Site :
# @File : DashboardController.py
# @Software: Pycharm
from dateutil.relativedelta import relativedelta
from flask_restplus import Namespace, Resource, fields

from service.dataSerializer.DatabaseGetMonthlyPurchaseAmountService import DatabaseGetMonthlyPurchaseAmountService
from utils.ControllerUtils import *
from service.DashboardService import *

dashboardService = DashboardService()


api = Namespace('dashboard', description='dashboard Data')



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
request_page_fields = api.model('request_page_model', {
    'paymentterm': fields.String(required=True, description="paymentterm", help="paymentterm cannot be blank."),
    'process': fields.Boolean(required=True, description="process", help="process cannot be blank."),
    'notprocess': fields.Boolean(required=True, description="notprocess", help="notprocess cannot be blank."),
    'bg': fields.String(required=True, description="bg", help="bg cannot be blank."),
    'site': fields.String(required=True, description="site", help="site cannot be blank."),
    'plant': fields.String(required=True, description="plant", help="plant cannot be blank."),
    'period': fields.Nested(period, description="period", help="period cannot be blank.")
})


@api.route('', methods=["GET", "POST", "DELETE", "PUT"])
class DashboardController(Resource):
    @api.route("/getHeader")
    class getHeader(Resource):
        def get(self):
            return dashboardService.getHeadr()

    @api.route("/monthlyPurchaseAmountBySite")
    class getMonthlyPurchaseAmountByDB(Resource):
        @api.expect(request_fields)
        def post(self):
            """
            取得 Monthly Purchase Amount 圖表
            """
            data = request.get_json()
            if data is None:
                return "請求參數不能為空"
            req = ControllerUtils.handleRequestBody(data)
            return dashboardService.postMonthlyPurchaseAmountPerSite(req)


    @api.route("/topTenVendor")
    class postVenderTopTen(Resource):
        @api.expect(request_fields)
        def post(self):
            data = request.get_json()
            if data is None:
                return "請求參數不能為空"
            req = ControllerUtils.handleRequestBody(data)
            return dashboardService.postVenderTopTen(req)

    @api.route("/topTenPO")
    class TopTenList(Resource):
        @api.expect(request_fields)
        def post(self):
            """
            取得 Top 10 PO 圖表
            """
            data = request.get_json()
            if data is None:
                return "請求參數不能為空"
            req = ControllerUtils.handleRequestBody(data)
            return dashboardService.postTopTenPO(req)

    @api.route("/dashboardHead")
    class DashboardHead(Resource):
        def get(self):
            return dashboardService.getDashBoardHead()

    @api.route("/bgSitePlant")
    class BgSitePlant(Resource):
        def get(self):
            return dashboardService.getBgSitePlant()

    @api.route("/paymentTermDistribution")
    class paymentTermDistributionByDB(Resource):
        @api.expect(request_fields)
        def post(self):
            """
            取得 Payment Term Distribution 圖表
            """
            data = request.get_json()
            if data is None:
                return "請求參數不能為空"
            req = ControllerUtils.handleRequestBody(data)
            return dashboardService.postPaymentTermDistribution(req)

        @api.route("/categoriesDistribution")
        class categoriesDistributionByDB(Resource):
            @api.expect(request_fields)
            def post(self):
                """
                取得 8-categorys Distribution 圖表
                """
                data = request.get_json()
                if data is None:
                    return "請求參數不能為空"
                req = ControllerUtils.handleRequestBody(data)
                return dashboardService.postDbGet8CategorysDistrbution(req)

