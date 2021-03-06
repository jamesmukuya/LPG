from main import app
from main.dbConnect.db_conn import Connect
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User:
    """
    Connecting and returning user data from database as per email_id
    """
    user_data = {}
    staff_data = {}
    staff_id = {}

    def get_user(self, e):
        # create a new object from class
        conn = Connect()
        # establish the connection
        con = conn.connect_db()
        # create a cursor
        #myCur = con.cursor()
        myCur = con.cursor(buffered=True, dictionary=True)
        # make a query on the basic_user_details table
        query = """select basic_user_details.id, first_name, last_name, email,
        user_password, user_registration.id as reg_id,basic_user_details_id
        from basic_user_details inner join user_registration
        on basic_user_details_id = basic_user_details.id where email = %(email)s
        limit 1"""
        # execute the query
        myCur.execute(query, {'email': e})
        # get data from the returned query object
        data = myCur.fetchone()
        con.close()
        # return required data
        #return data
        self.user_data = data
        return self.user_data

    def get_user_using_id(self, e):
        # create a new object from class
        conn = Connect()
        # establish the connection
        con = conn.connect_db()
        # create a cursor
        #myCur = con.cursor()
        myCur = con.cursor(buffered=True, dictionary=True)
        # make a query on the basic_user_details table
        query = """select basic_user_details.id, first_name, last_name, email,
        user_password, user_registration.id as reg_id,basic_user_details_id
        from basic_user_details inner join user_registration
        on basic_user_details_id = basic_user_details.id 
        where basic_user_details.id = %(id)s
        limit 1"""
        # execute the query
        myCur.execute(query, {'id': e})
        # get data from the returned query object
        data = myCur.fetchone()
        con.close()
        # return required data
        #return data
        self.user_data = data
        return self.user_data

    def get_staff(self, e):
        # create a new object from class
        conn = Connect()
        # establish the connection
        con = conn.connect_db()
        # create a cursor
        #myCur = con.cursor()
        myCur = con.cursor(buffered=True, dictionary=True)
        # make a query on the basic_user_details table
        query = (
            "select * from employee "
            "LEFT JOIN basic_user_details on employee.basic_user_details_id =\
            basic_user_details.id "
            "WHERE employee.emp_no = %(emp_no)s"
            )
        # execute the query
        myCur.execute(query, {'emp_no': e})
        # get data from the returned query object
        data = myCur.fetchone()
        con.close()
        # return required data
        self.staff_data = data
        return self.staff_data

    def get_staff_id(self, e):
        # create a new object from class
        conn = Connect()
        # establish the connection
        con = conn.connect_db()
        # create a cursor
        #myCur = con.cursor()
        myCur = con.cursor(buffered=True, dictionary=True)
        # make a query on the basic_user_details table
        query = (
            "select id from employee "
            "WHERE employee.emp_no = %(emp_no)s"
        )
        # execute the query
        myCur.execute(query, {'emp_no': e})
        # get data from the returned query object
        data = myCur.fetchone()
        con.close()
        # return required data
        self.staff_id = data
        return self.staff_id

    def get_email(self):
        """
        This method must return a unicode that uniquely identifies this user,
        and can be used to load the user from the user_loader callback. 
        """
        user_id = self.user_data.get('email')
        print('user id from get_id', user_id)
        return user_id
