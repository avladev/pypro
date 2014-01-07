import web
import config

db = web.database(dbn='mysql', db=config.db_name, user=config.db_user, passwd=config.db_password)


def get_todos():
    return db.select(config.db_todo_table, order='id')


def new_todo(text):
    db.insert(config.db_todo_table, title=text)


def del_todo(id):
    db.delete(config.db_todo_table, where="id=$id", vars=locals())