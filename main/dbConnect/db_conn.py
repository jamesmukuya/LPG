"""
db connection class
"""
import os, glob, json
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
            #local db
            user_name = os.environ.get('lpg_user')
            user_pass = os.environ.get('lpg_pass')
            db = 'lpg_mysql'
            host = 'localhost'
            conn = sql.connect(
                host=host, db=db, user=user_name, password=user_pass,
                use_unicode=True, charset="utf8")
            return conn
        except (sql.Error, sql.Warning):
            try:
                #web db
                for files in glob.iglob('**/*.json', recursive=True):
                    #print(files)
                    with open(files) as f:
                        data = json.load(f)
                        #print()
                        db = data.get('web_db')
                        user_name = data.get('web_admin')
                        user_pass = data.get('web_p')
                        conn = sql.connect(
                            host=host, db=db, user=user_name, password=user_pass,
                            use_unicode=True, charset="utf8")
                        return conn
            except Exception:
                return None
            #conn.close()
        except Exception as ex:
            print('UNKNOWN ERROR OCCURED', ex)
            return None

    def check_conn(self):
        #print('success')
        conn = self.connect_db()
        myCur = conn.cursor()
        query = """
        select * from basic_user_details
        """
        myCur.execute(query)
        data = myCur.fetchall()
        conn.close()
        print('this is the returned',data)

#conn1 = Connect()
#conn1.check_conn()
#print(os.environ.get('lpg_user'))
