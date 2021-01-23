from service.dataSerializer.IDataSerializer import IDataSerializer
from utils.ApiResponse import *
from model.Plant import ObjPlant
from model.Site import ObjSite
from model.BG import ObjBG
from model.database import db
from view.Header import HeaderSchema
import logging

logger = logging.getLogger(__name__)
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError


plant = ObjPlant()
bg = ObjBG()
site = ObjSite()
headerSchema = HeaderSchema()


class DatabaseGetHeaderService(IDataSerializer):
    def __init__(self):
        pass

    def serialize(self):
        """取得 plant site BG"""
        """ return 
            [{
              "site":"WIH",
              "bg":"CBG",
              "plant":"F601"
            }]
        """
        try:

            results = db.session.query(ObjPlant.name.label('plant'),
                                       ObjSite.name.label('site'),
                                       ObjBG.name.label('bg')) \
                .join(ObjSite, ObjPlant.site_id == ObjSite.id) \
                .join(ObjBG, ObjSite.bg_id == ObjBG.id)

            data = headerSchema.dumps(results, many=True)
            logger.debug(data)

            return ApiResponse.emitSuccessOutput({"result": data})
        except ValidationError as err:
            result = ApiResponse.emitErrorOutput(E_VALIDATION_ERROR, err.messages, "DatabaseGetHeaderService")
        except SQLAlchemyError as e:
            db.session.rollback()
            result = ApiResponse.emitErrorOutput(E_SQLALCHEMY_ERROR, str(e), "DatabaseGetHeaderService")
        return result
