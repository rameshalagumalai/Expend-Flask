from connection import conn
from flask import session
import ibm_db

def getAllCategories():
    categories = []
    sql = "SELECT expense_category.id, expense_category.name, expense_category.color, (SELECT SUM(amount) FROM expense WHERE category_id = expense_category.id), (SELECT COUNT(*) FROM expense WHERE category_id = expense_category.id) FROM expense_category WHERE expense_category.user_id = ?" 
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, session['userId'])
    ibm_db.execute(stmt)
    tuple = ibm_db.fetch_tuple(stmt)
    while tuple != False:
        categories.append(tuple)
        tuple = ibm_db.fetch_tuple(stmt)
    return categories  


def addNewCategory(data):
    sql = "INSERT INTO expense_category (name, color, user_id) VALUES (?, ?, ?)"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, data['name'])
    ibm_db.bind_param(stmt, 2, data['color'])
    ibm_db.bind_param(stmt, 3, session['userId'])
    ibm_db.execute(stmt)      