'''
SQLAlchemy engine
Used to reset fogot user password
'''
# imports
from main import app
import os,sqlalchemy, glob, json
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# get authentication data
user_name = os.environ.get('lpg_user')
user_pass = os.environ.get('lpg_pass')

# TODO when in production place this at the correct place
# get the credentials from secure file
def get_auth():
    for files in glob.iglob('**/*.json', recursive=True):
        with open(files) as f:
            data = json.load(f)
            web_db = data.get('web_db')

            user_name = data.get('local_db_user')
            user_name_web = data.get('web_admin')

            user_pass = data.get('local_db_pass')
            user_pass_web = data.get('web_p')

    return user_name, user_pass, web_db, user_name_web, user_pass_web
auth = get_auth()
# Define the MySQL engine using MySQL Connector/Python
try:
  engine = sqlalchemy.create_engine(
      f'mysql+mysqlconnector://{user_name}:{user_pass}@localhost:3306/lpg_mysql?auth_plugin=mysql_native_password',
    echo=False)
except:
  try:
    engine = sqlalchemy.create_engine(
        f'mysql+mysqlconnector://{auth[0]}:{auth[1]}@localhost:3306/lpg_mysql?auth_plugin=mysql_native_password',
        echo=False)
  except:
    engine = sqlalchemy.create_engine(
        f'mysql+mysqlconnector://{auth[3]}:{auth[4]}@localhost:3306/{auth[2]}?auth_plugin=mysql_native_password',
        echo=False)

# create session object
session = Session(engine)
# base object
Base = declarative_base()

# user class
 
class UserTable(Base):
  '''
  This class represents the database schema of the user
  args: id, first_name, last_name, email, user_password, birth_date
  '''
  __tablename__ = 'basic_user_details'

  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
  first_name = sqlalchemy.Column(sqlalchemy.String(length=45))
  last_name = sqlalchemy.Column(sqlalchemy.String(length=45))
  email = sqlalchemy.Column(sqlalchemy.String(length=105))
  user_password = sqlalchemy.Column(sqlalchemy.String(length=105))

  def __repr__(self):
      return "<User(first_name='{0}', last name='{1}', email='{2}')>".format(
                          self.first_name, self.last_name, self.email)
  @staticmethod
  def verify_email(email):
    user = session.query(UserTable).filter_by(email=email).first()
    if user:
      global id
      id = user.id
      return user
    return None

  # 21600sec=6hrs
  def get_reset_token(self, expires=21600):
    """
    pass token to reset a user password
    payload to match token is user_id
    token currenly expires after 6hrs
    """
    s = Serializer(app.config['SECRET_KEY'])
    #print('self.id is this', self.id)
    #token = s.dumps({'user_id': self.id}).decode('utf-8')
    token = s.dumps({'user_id': id}).decode('utf-8')
    return token

  @staticmethod
  def verify_reset_token(token):
    # make the serializer object
    s = Serializer(app.config['SECRET_KEY'])
    # instance of the user class
    try:
        # pass the user id to the token to verify['user_id']
        user_id = s.loads(token)['user_id']
    except:
        return None
    # if id is verified return the user object
    our_user = session.query(UserTable).filter_by(id=user_id).first()
    #return UserTable.query.get(user_id)
    return our_user
