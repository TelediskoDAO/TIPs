import sys
from pprint import pprint
import xmlrpc.client

try:
    env = {
        k: v for k, v in map(lambda l: l.strip().split("="), open(".env").readlines())
    }
except FileNotFoundError:
    print("Cannot find .env file with credentials")


url = "https://odoo.teledisko.com"
db = "teledisko"
username = env.get("ODOO_USERNAME")
password = env.get("ODOO_PASSWORD")
p = pprint

if not username or not password:
    print("Cannot find username or password")
    sys.exit(1)

common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))
uid = common.authenticate(db, username, password, {})


def version():
    return common.version()


def list_projects():
    return models.execute_kw(db, uid, password, "project.project", "search", [[]])


def list_tasks():
    return models.execute_kw(db, uid, password, "project.task", "search", [[]])


def read_projects():
    return models.execute_kw(db, uid, password, "project.project", "read", [2])


def read_tasks():
    return models.execute_kw(db, uid, password, "project.task", "read", [1115])


def read_duration():
    return models.execute_kw(db, uid, password, "project.task.duration", "read", [1318])


def read_tasks_by_user_id(user_id):
    return models.execute_kw(
        db, uid, password, "project.task", "search_read", [[["user_id", "=", user_id]]]
    )


def c(model, **kwargs):
    models.execute_kw(db, uid, password, model, "create", [kwargs])


def r(model, *args, **kwargs):
    query = []
    for k, v in kwargs.items():
        query.append([k, "=", v])
    return models.execute_kw(
        db, uid, password, model, "search_read", [query], {"fields": args}
    )


def u(model, id, **kwargs):
    models.execute_kw(db, uid, password, model, "write", [[id], kwargs])


import json


def dump_stuff():
    projects = []
    projects.extend(r("project.project", id=67))
    projects.extend(r("project.project", id=84))

    tasks = []
    tasks.extend(r("project.task", user_id=uid))

    durations = []
    durations.extend(r("project.task.duration", create_uid=uid))

    json.dump(projects, open("projects.json", "w"))
    json.dump(tasks, open("tasks.json", "w"))
    json.dump(durations, open("durations.json", "w"))


# pprint(r("project.task", user_id=uid))

# pprint(version())
# pprint(list_projects())
# pprint(read_projects())
# pprint(read_tasks())
# pprint(read_duration())

# https://stackoverflow.com/a/56498901/597097
# pickings = models.execute_kw(db, uid, pwd, 'stock.picking', 'search_read',
#                           [[['state', '=', 'done'], ['date_done', '>', '2019-01-01']]],
#                           {'fields':['name'], 'offset': 0, 'limit': 5, 'order': 'date_done desc'})
