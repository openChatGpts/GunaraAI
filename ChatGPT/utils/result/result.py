
from django.http import JsonResponse


def err_result(msg, code=500):
    return JsonResponse(
        {
            "code": code, 
            "error":{
                "message":msg,
                "type": "request_error",
                "param": "null",
                "code": code
            }
            }
        )


def result(data):
    return JsonResponse({"code": 200, "data": data})




ResError = err_result
ResSuccess = result
