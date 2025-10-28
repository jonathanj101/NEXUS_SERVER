response = {}


# SUCCESS STATUS

response["SUCCESS"] = {"STATUS": True}

# SUCCESS CODES

response["SUCCESS_CODES"] = {
    "STANDARD": 200,
    "CREATED": 201,
    "ACCEPTED": 202,
    "NOCONTENT": 204,
}

# SERVER ERROR

response["SERVER_ERROR"] = {"CODE": 500, "MESSAGE": "DB_ERROR", "STATUS": False}

# # ERROR

# response["ERROR"] = {
#     "CODE":400
# }

# BAD_REQUEST

response["BAD_REQUEST"] = {"CODE": 400, "MESSAGE": "BAD_REQUEST"}

# UN_AUTHORIZED

response["UN_AUTHORIZED"] = {
    "STATUS": False,
    "CODE": 401,
    "MESSAGE": "NOT_AUTHORIZED",
}

# FORBIDDEN_ACCESS
response["FORBIDDEN_ACCESS"] = {"CODE": 403, "MESSAGE": "FORBIDDEN_ACCESS"}

# RESOURCE NOT FOUND

response["PAGE404"] = {
    "CODE": 404,
    "MESSAGE": "PAGE_NOT_FOUND",
}

# METHOD NOT FOUND

response["METHOD_NOT_FOUND"] = {
    "CODE": 405,
    "MESSAGE": "METHOD_NOT_FOUND",
}

# CONFLICT, client request  accepted but does not match server state
response["CONFLICT"] = {"CODE": 409}

# UNPROCESSIBLE ENTITY
response["UNPROCESSIBLE_ENTITY"] = {
    "STATUS": False,
    "CODE": 422,
    "MESSAGE": "UNPROCESSIBLE_ENTITY",
}

SUCCESS = response["SUCCESS"]
SUCCESS_CODE = response["SUCCESS_CODES"]
SERVER_ERROR = response["SERVER_ERROR"]
BAD_REQUEST = response["BAD_REQUEST"]
UNPROCESSIBLE_ENTITY = response["UNPROCESSIBLE_ENTITY"]
UN_AUTHORIZED = response["UN_AUTHORIZED"]
FORBIDEN_ACCESS = response["FORBIDDEN_ACCESS"]
NOT_FOUND = response["PAGE404"]
METHOD_NOT_FOUND = response["METHOD_NOT_FOUND"]
CONFLICT = response["CONFLICT"]
