

from bson.codec_options import CodecOptions
from bson.binary import STANDARD

from pymongo.write_concern import WriteConcern
import main

def do():
    jsonUsers = {
        "bsonType": "object",
        "properties": {
            "username": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "email": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "level_id": {
                "bsonType": "objectId",
                "description": "must be a objectId and is required"
            },
            "password": {
                "bsonType": "string",
                "description": "must be a string and is required"
            }
        }
    }

    jsonLevels = {
        "bsonType": "object",
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "description": {
                "bsonType": "string",
                "description": "must be a string and is required"
            }
        }
    }

    jsonAdvice = {
        "bsonType": "object",
        "properties": {
            "rec_id": {
                "bsonType": "objectId",
                "description": "must be a objectId and is required"
            },
            "time": {
                "bsonType": "string",
                "description": "must be a string and is required"
            }
        }
    }

    jsonRecords = {
        "bsonType": "object",
        "properties": {
            "xspeed": {
                "bsonType": "double",
                "description": "must be a double and is required"
            },
            "yspeed": {
                "bsonType": "double",
                "description": "must be a double and is required"
            },
            "zspeed": {
                "bsonType": "double",
                "description": "must be a double and is required"
            },
            "angle": {
                "bsonType": "int",
                "description": "must be an int and is required"
            }
        }
    }

    jsonTasks = {
        "bsonType": "object",
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "link": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "user_id": {
                "bsonType": "objectId",
                "description": "must be a objectId and is required"
            },
            "rec_id": {
                "bsonType": "objectId",
                "description": "must be a objectId and is required"
            },
            "level_id": {
                "bsonType": "objectId",
                "description": "must be a objectId and is required"
            },
            "text": {
                "bsonType": "string",
                "description": "must be a string and is required"
            }
        }
    }

    jsonSessions = {
        "bsonType": "object",
        "properties": {
            "user_id": {
                "bsonType": "objectId",
                "description": "must be a objectId and is required"
            },
            "rec_id": {
                "bsonType": "objectId",
                "description": "must be a objectId and is required"
            },
            "instructor_id": {
                "bsonType": "objectId",
                "description": "must be a objectId and is required"
            },
            "task_id": {
                "bsonType": "objectId",
                "description": "must be a objectId and is required"
            },
            "dtstart": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "dtfinish": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
        }
    }

    
    main.db.create_collection(
        "users1",
        codec_options=CodecOptions(uuid_representation=STANDARD),
        write_concern=WriteConcern(w="majority"),
        validator={"$jsonSchema": jsonUsers})
    main.db.create_collection(
        "levels1",
        codec_options=CodecOptions(uuid_representation=STANDARD),
        write_concern=WriteConcern(w="majority"),
        validator={"$jsonSchema": jsonLevels})
    main.db.create_collection(
        "advice1",
        codec_options=CodecOptions(uuid_representation=STANDARD),
        write_concern=WriteConcern(w="majority"),
        validator={"$jsonSchema": jsonAdvice})
    main.db.create_collection(
        "records1",
        codec_options=CodecOptions(uuid_representation=STANDARD),
        write_concern=WriteConcern(w="majority"),
        validator={"$jsonSchema": jsonRecords})
    main.db.create_collection(
        "tasks1",
        codec_options=CodecOptions(uuid_representation=STANDARD),
        write_concern=WriteConcern(w="majority"),
        validator={"$jsonSchema": jsonTasks})
    main.db.create_collection(
        "sessions1",
        codec_options=CodecOptions(uuid_representation=STANDARD),
        write_concern=WriteConcern(w="majority"),
        validator={"$jsonSchema": jsonSessions})

    # main.db.users1.insert([
    #     {"username": "Anne", "email": "a@gmail.com", "level_id": "1", "password": "123" },])