"""
user model for a flask authentication
"""
from main.dbConnect.db_conn import Connect

class User():
    """
    model for basic user details
    """
    user_data = {}

    def get_user(self,e):
        # create a new object from class
        conn = Connect()
        # establish the connection
        con = conn.connect_db()
        # create a cursor
        myCur = con.cursor(buffered=True, dictionary=True)
        # make a query on the basic_user_details table
        query = "select * from basic_user_details where email = %(email)s\
            limit 1"
        # execute the query
        myCur.execute(query, {'email': e})
        # get data from the returned query object
        data = myCur.fetchone()
        con.close()
        # return required data
        #return data['email']
        self.user_data = data
        return data

    def get_id(self):
        return self.user_data.get('email')
    
    def is_anonymous(self):
        return False

    def is_active(self):
        return True


