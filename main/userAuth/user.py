"""
user model for a flask authentication
"""
from six import text_type
from flask_login import UserMixin
from main.dbConnect.db_conn import Connect

class User(UserMixin):
    """
    model for basic user details
    """
    user_data = {}
    """
    def __init__(self,id=None):
        self.user_data = self.get_user(id)
        print('user data from User',self.user_data)
    """
    
    def get_user(self,e):
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

    def get_id(self):
        """
        This method must return a unicode that uniquely identifies this user,
        and can be used to load the user from the user_loader callback. 
        """
        user_id = self.user_data.get('email')
        print('user id from get_id',user_id)
        return text_type(user_id)
    """
    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def is_authenticated(self):
        return True
    """
