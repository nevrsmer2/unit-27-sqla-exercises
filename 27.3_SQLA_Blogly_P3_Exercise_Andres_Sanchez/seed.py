
from app import app
from models import Post, User, db

# Create all tables
db.drop_all()
db.create_all()

'''---------Create  Instances of User Model--------'''

u1 = User(first_name='Darth', last_name='Vader',
          image_url='https://www.goalcast.com/wp-content/uploads/2022/08/darth-vader.jpg')
u2 = User(first_name='Freddy', last_name='Kruger',
          image_url='https://dmdave.com/wp-content/uploads/2019/10/freddy-krueger.jpg')
u3 = User(first_name='Terminator', last_name='2',
          image_url='https://ultimateactionmovies.com/wp-content/uploads/2018/08/Terminator-2-Arnold.jpg')
u4 = User(first_name='Sigrouney', last_name='Weaver',
          image_url='https://bloody-disgusting.com/wp-content/uploads/2014/08/AII_1.jpg')


db.session.add_all([u1, u2, u3, u4])
db.session.commit()


'''---------Create Instances of Post Model--------'''

p1 = Post(title='January Days',
          content='The days in January are grey, cold, and windy.', user_id=2)
p2 = Post(title='Chili is Comfort Food',
          content='In the winter, chili keeps me warm and happy.', user_id=1)
p3 = Post(title='Sunfolower with Spots',
          content='I have a sunflower with spots who is a ray of sunshine.', user_id=3)
p4 = Post(title='Buttermilk Bisquits',
          content='I love buttermilk bisquits for breakfast.', user_id=2)

db.session.add_all([p1, p2, p3, p4])
db.session.commit()
