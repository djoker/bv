from bvapi import db, model
from bvapi.model import User, Client
from bvapi import AD_USER, AD_PASS

db.create_all()

ad = User()
ad.name = AD_USER
ad.userid = AD_USER
ad.hash_password(AD_PASS)

cli = Client()
cli.name = 'Mr. X'
cli.email = 'x@nowhere.com'
cli.address = 'nowhere place 404'



db.session.add(ad)
db.session.add(cli)
db.session.commit()

print('Tables created')
print('Admin user created')

