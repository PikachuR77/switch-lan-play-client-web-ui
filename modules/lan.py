from flask import request, Blueprint
from models import ModelServer
from utils import make_success, make_faild
from services import service_lan

lan = Blueprint('BlueprintLan', __name__, url_prefix='/lan')


@lan.route('/connect', methods=['POST'])
def lan_connect():
    target_id = request.values.get('id')
    find: ModelServer = ModelServer.get_or_none(id=target_id)
    if find is None:
        return make_faild(msg='Operation failed')

    service_lan.start_lan_play(ip=find.host)
    return make_success()


@lan.route('/disconnect', methods=['POST'])
def lan_disconnect():
    service_lan.stop_lan_play()
    return make_success(msg='Disconnected from server')


@lan.route('/info')
def lan_info():

    runing = service_lan.runing()
    address = service_lan.lan_address
    update_timestamp = service_lan.update_timestamp
    server_info = None

    if runing:
        find = ModelServer.get_or_none(
            ModelServer.host == service_lan.lan_address
        )
        if find is not None:
            server_info = find.dict()

    return make_success(data={
        'runing': runing,
        'address': address,
        'update_timestamp': update_timestamp,
        'server': server_info
    })
