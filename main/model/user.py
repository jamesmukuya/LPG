from six import text_type
from main.dbConnect.db_conn import Connect

class User:
    """
    Connecting and returning user data from database as per email_id
    """
    user_data = {}

    def get_user(self, e):
        # create a new object from class
        conn = Connect()
        # establish the connection
        con = conn.connect_db()
        # create a cursor
        #myCur = con.cursor()
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
        #return data
        self.user_data = data
        return self.user_data

    def get_email(self):
        """
        This method must return a unicode that uniquely identifies this user,
        and can be used to load the user from the user_loader callback. 
        """
        user_id = self.user_data.get('email')
        print('user id from get_id', user_id)
        return text_type(user_id)

