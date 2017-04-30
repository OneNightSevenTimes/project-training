class BaseResponse(object):
    def __init__(self):
        self.status = True
        self.data = None
        self.error = None