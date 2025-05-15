from app.extensions import db
from app.blueprints.item.schemas import ItemResponseSchema

from app.models.item import Item

from sqlalchemy import select

class ItemService:

    @staticmethod
    def item_add(request):
        try:

            item = Item(**request)
            db.session.add(item)
            db.session.commit()

        except Exception as ex:
            return False, "item_add() error!"
        return True, ItemResponseSchema().dump(item)

    @staticmethod
    def item_list_all():
        items = db.session.execute(select(Item).filter(Item.deleted.is_(0))).scalars()
        return True, ItemResponseSchema().dump(items, many=True)

    @staticmethod
    def item_update(oid, request):
        try:
            item = db.session.get(Item, oid)
            if item:
                item.name = request["name"]
                item.description = request["description"]
                item.price = float(request["price"])
                db.session.commit()

        except Exception as ex:
            return False, "food_update() error!"
        return True, ItemResponseSchema().dump(item)

    @staticmethod
    def item_delete(iid):
        try:
            item = db.session.get(Item, iid)
            if item:
                item.deleted = 1
                db.session.commit()

        except Exception as ex:
            return False, "item_update() error!"
        return True, "OK"