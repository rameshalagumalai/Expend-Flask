from connection import conn
import ibm_db

def addNewUser(data):
    sql = "INSERT INTO user (name, email, password, limit) VALUES (?, ?, ?, ?)"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, data['name'])
    ibm_db.bind_param(stmt, 2, data['email'])
    ibm_db.bind_param(stmt, 3, data['password'])
    ibm_db.bind_param(stmt, 4, data['limit'])
    ibm_db.execute(stmt)

    sql = "INSERT INTO expense_category (name, color, user_id) VALUES('Regular', '#B2B2B2', (SELECT id FROM user WHERE email = ?))"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, data['email'])
    ibm_db.execute(stmt)