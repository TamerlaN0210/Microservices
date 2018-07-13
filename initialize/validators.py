users_validator = {
    '$jsonSchema': {
         'bsonType': "object",
         'required': ["username", "password", "created_at"],
         'properties': {
            'username': {
                'bsonType': "string",
                'description': "must be a string and is required"
            },
            'password': {
                'bsonType': "binData",
                'description': "must be a bytes and is required"
            },
            'created_at': {
                'bsonType': "int",
                'description': "must be an integer and is required"
            }
         }
    }
}
offers_validator = {
    '$jsonSchema': {
         'bsonType': "object",
         'required': ["user_id", "title", "text", "created_at"],
         'properties': {
              'user_id': {
                 'bsonType': "int",
                 'description': "must be a integer and is required"
              },
              'title': {
                 'bsonType': "string",
                 'description': "must be a string and is required"
              },
              'text': {
                 'bsonType': "string",
                 'description': "must be a string and is required"
              },
              'created_at': {
                 'bsonType': "int",
                 'description': "must be an integer and is required"
              }
         }
    }
}
