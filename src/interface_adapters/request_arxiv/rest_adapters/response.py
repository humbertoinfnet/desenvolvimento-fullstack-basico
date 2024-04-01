

class SuccessResponse:
    def __init__(self, message=None, data=None):
        self.success = True
        self.message = message
        self.data = data

    def to_dict(self):
        response_dict = {'success': self.success}
        if self.message:
            response_dict['message'] = self.message
        if self.data:
            response_dict['data'] = self.data
        return response_dict

class ErrorResponse:
    def __init__(self, message):
        self.success = False
        self.error = message

    def to_dict(self):
        return {'success': self.success, 'error': self.error}
