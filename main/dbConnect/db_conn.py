"""
db connection class
"""
import os
import mysql.connector as sql

class Connect:
    """
    establish connection
    """
    def connect_db(self):
        """
        returns a connection
        """
        # pass in the user credentials for the db
        try:
            user_name = 'techpoint_dev'
            user_pass = 'K@zumi@1'
            db = 'lpg_mysql'
            host='localhost'
            conn = sql.connect(
                host=host, db=db, user=user_name, password=user_pass, use_unicode=True, charset="utf8")
            return conn
        except (Exception, sql.Error, sql.Warning) as e:
            print(e)
            conn.close()

    def check_conn(self):
        #print('success')
        conn = self.connect_db()
        myCur = conn.cursor()
        query = """
        select * from accounts
        """
        myCur.execute(query)
        data = myCur.fetchall()
        conn.close()
        print('this is the returned',data)

#conn1 = Connect()
#conn1.check_conn()
#print(os.environ.get('DB_LPG_USER'))