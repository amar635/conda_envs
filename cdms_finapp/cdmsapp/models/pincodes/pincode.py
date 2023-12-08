from extensions import db

class pincode(db.Model):
    __tablename__ = "pincodes"

    id = db.Column(db.Integer, primary_key=True)
    pincode=db.Column(db.Integer, unique=True, nullable=False)
    circle =  db.Column(db.String, unique=False, nullable=False)
    delivery =  db.Column(db.String, unique=False, nullable=False)
    district =  db.Column(db.String, unique=False, nullable=False)
    division =  db.Column(db.String, unique=False, nullable=False)
    latitude =  db.Column(db.String, unique=False, nullable=False)
    longitude =  db.Column(db.String, unique=False, nullable=False)
    office =  db.Column(db.String, unique=False, nullable=False)
    office_type =  db.Column(db.String, unique=False, nullable=False)
    phone =  db.Column(db.String, unique=False, nullable=False)
    pin =  db.Column(db.String, unique=False, nullable=False)
    region =  db.Column(db.String, unique=False, nullable=False)
    related_headoffice =  db.Column(db.String, unique=False, nullable=False)
    related_suboffice =  db.Column(db.String, unique=False, nullable=False)
    state_id =  db.Column(db.String, unique=False, nullable=False)
    taluk =  db.Column(db.String, unique=False, nullable=False)
#   "": "Delivery",
#   "": "Dakshina Kannada",
#   "": "Mangalore",
#   "": "Not Available",
#   "": "Not Available",
#   "": "Shakthinagar (Dakshina Kannada) S.O",
#   "": "S.O",
#   "": "0824-2232076",
#   "": 575016,
#   "": "South Karnataka",
#   "": "Kulshekar H.O",
#   "": "Not Available",
#   "": 15,
#   "": "Mangalore"
# state
# state_id

# district
# district_id
# state_id

# taluk
# taluk_id
# district_id


# {
#   "circle": "Karnataka",
#   "delivery": "Delivery",
#   "district": "Dakshina Kannada",
#   "division": "Mangalore",
#   "latitude": "Not Available",
#   "longitude": "Not Available",
#   "office": "Shakthinagar (Dakshina Kannada) S.O",
#   "office_type": "S.O",
#   "phone": "0824-2232076",
#   "pin": 575016,
#   "region": "South Karnataka",
#   "related_headoffice": "Kulshekar H.O",
#   "related_suboffice": "Not Available",
#   "state_id": 15,
#   "taluk": "Mangalore"
# }