from flask import request, Blueprint
from models import ModelServer
from utils import make_success, make_faild
import requests
from services import service_lan


server = Blueprint('BlueprintServer', __name__, url_prefix='/server')


@server.route('/add', methods=['POST'])
def server_add():
    name = request.values.get('name')
    host = request.values['host'].replace(' ', '')

    if name is None or len(name) == 0:
        name = host

    find = ModelServer.get_or_none(ModelServer.host == host)
    if find is not None:
        return make_faild(msg='This server already exists', data=find)

    find = ModelServer.create(host=host, name=name)
    return make_success(msg='Added server successfully', data=find)


@server.route('/remove', methods=['POST'])
def server_remove():
    target_id = request.values['id']
    find: ModelServer = ModelServer.get_or_none(id=target_id)
    if find is None:
        return make_faild(msg='Operation Failed')
    if find.host == service_lan.lan_address:
        return make_faild(msg='Failed to delete, server is connected')
    find.delete_instance()
    return make_success()


@server.route('/list')
def server_list():
    find_all = ModelServer.select().execute()

    result = list(map(lambda v: v.dict(), find_all))
    return make_success(data=result)


@server.route('/refresh')
def server_refresh():
    find_all = ModelServer.select().order_by(-ModelServer.id)
    for item in find_all:
        try:
            uri = format(item.host)
            if uri.startswith('http') == False:
                uri = 'http://' + uri
            response = requests.get(
                '{0}/info'.format(uri),
                timeout=(0.5, 2),
            )
            if response.status_code != 200:
                item.version = 'Error: {0}'.format(response.status_code)
                item.save()
                continue

            data = response.json()
            item.online = data['online']
            item.version = data['version']
            item.ping = int(response.elapsed.total_seconds() * 1000)

        except requests.exceptions.ReadTimeout as e:
            item.version = 'Server response timed out'
            item.ping = -1
        except requests.exceptions.ConnectTimeout as e:
            item.version = 'Connection to server timed out'
            item.ping = -1
        except requests.exceptions.ConnectionError:
            item.version = 'Address access failed'
            item.ping = -1
        except:
            item.version = 'Server access failed'
            item.ping = -1

        item.save()

    result = list(map(lambda v: v.dict(), find_all))
    return make_success(data=result)
