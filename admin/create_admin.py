import admin_login_db as db
import hashlib

conn = db.create_connection()
db.create_admin_table(conn)

def create_md5(passwd: str) -> str:
    m = hashlib.md5()
    m.update(passwd.encode("utf-8"))
    return m.hexdigest()

admin_user = "admin"
admin_pass_md5 = create_md5("make_your_password")
db.insert_admin(conn, (admin_user, admin_pass_md5))