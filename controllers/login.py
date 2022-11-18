from connection import conn
import ibm_db
from flask import session

def signInUser(data):
    response = -1
    sql = "SELECT id FROM user WHERE email = ? AND password = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, data['email'])
    ibm_db.bind_param(stmt, 2, data['password'])
    ibm_db.execute(stmt)
    tuple = ibm_db.fetch_tuple(stmt)
    if tuple != False:
        response = tuple[0]
        session['userId'] = response
    return response   