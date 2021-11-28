from firebase_admin import credentials, initialize_app, db
from models import Laptop

# Initialize Realtime DB Firebase
cred = credentials.Certificate('findtechKey.json')
default_app = initialize_app(cred, {
    'databaseURL':'https://findtech-d396c-default-rtdb.asia-southeast1.firebasedatabase.app'
})
ref = db.reference('/Laptops')
snapshot = ref.get()

# Throw snapshot into list
laptopList = []
for items in snapshot:
    laptop = Laptop(items['Name'], items['Price'], items['Image'])
    laptopList.append(laptop)
jsonLaptopList = [e.serialize() for e in laptopList]