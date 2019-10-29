def fiware_headers(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        fiware_service = self.request.META.get('HTTP_FIWARE_SERVICE', '')
        fiware_service_path = self.request.META.get('HTTP_FIWARE_SERVICEPATH', '/')
        return func(*args, **kwargs, fiware_service=fiware_service, fiware_service_path=fiware_service_path)
    return wrapper


def extract_faas_function_param(func):
    def wrapper(*args, **kwargs):
        request = kwargs.get('request')
        name = request.data.pop('name')
        code = request.data.pop('code')
        language = request.pop('language')
        parameters = []
        if 'parameters' in request.data:
            parameters = request.data.pop('parameters')
        param = {
            'name': name,
            'code': code,
            'language': language,
            'parameters': parameters
        }

        return func(*args, **kwargs, param=param)
    return wrapper
