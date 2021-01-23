import traceback
from model.BG import ObjBG
from model.Plant import ObjPlant
from model.Site import ObjSite
from model.database import db
import logging
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

logger = logging.getLogger(__name__)
plant = ObjPlant()
bg = ObjBG()
site = ObjSite()


class Organization:

    def __init__(self, bg, site, plant):

        # the data sometimes is str the format as 'WSK,CBS' it should be split to array
        if type(bg) is str:
            self.bg = bg.split(',')
        else:
            self.bg = bg

        if type(site) is str:
            self.site = site.split(',')
        else:
            self.site = site

        if type(plant) is str:
            self.plant = plant.split(',')
        else:
            self.plant = plant


    def get_redis_format(self):
        try:
            ft = [ObjPlant.name.in_(self.plant), ObjBG.name.in_(self.bg), ObjSite.name.in_(self.site)]
            results = db.session.query(ObjPlant.name.label('plant'),
                                       ObjSite.name.label('site'),
                                       ObjBG.name.label('bg')) \
                .join(ObjSite, ObjPlant.site_id == ObjSite.id,  full=True) \
                .join(ObjBG, ObjSite.bg_id == ObjBG.id).filter(*ft).all()
            items = []
            for res in results:
                items.append('{}_{}_{}'.format(res.bg, res.site, res.plant))
            return items
        except ValidationError as err:
            logger.error(traceback.print_exc())
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(traceback.print_exc())
            return None
        except Exception as e:
            logger.error(traceback.print_exc())
            return None
