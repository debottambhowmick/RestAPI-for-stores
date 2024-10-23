from marshmallow import Schema, fields

class ItemSchema(Schema):
    id = fields.Str(dump_only=True)  
    name = fields.Str(required=True) 
    price = fields.Float(required=True) 
    store_id = fields.Str(required=True) 



class ItemUpdateSchema(Schema):
    name = fields.Str() 
    price = fields.Float() 



class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)   



# so, now that we have got these schemas like i said, we are goin to use them for validating incomming data and for turning outgoing data into valid as per the schema.
