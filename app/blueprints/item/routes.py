from app.blueprints.item import bp
from app.blueprints.item.schemas import ItemRequestSchema, ItemResponseSchema, ItemListSchema
#from app.blueprints.item.service import ItemService
from apiflask.fields import String, Integer
from apiflask import HTTPError

@bp.route('/')
def index():
    return 'This is The Food Blueprint'

@bp.get('/list/')
@bp.output(ItemListSchema(many = True))
def item_list_all():
    success, response = ItemService.food_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/list/<int:rid>')
@bp.input({'cid': Integer()}, location='query')
@bp.output(ItemListSchema(many = True))
def item_list_category(query_data, rid):
    success, response = ItemService.item_list_category(rid, query_data.get("cid"))
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.post('/add')
@bp.input(ItemRequestSchema, location="json")
@bp.output(ItemResponseSchema)
def item_add_new(json_data):
    success, response = ItemService.item_add(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put('/update/<int:fid>')
@bp.input(ItemRequestSchema, location="json")
@bp.output(ItemResponseSchema)
def item_update(fid, json_data):
    success, response = ItemService.item_update(fid, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:fid>')
def item_delete(fid):
    success, response = ItemService.item_delete(fid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)