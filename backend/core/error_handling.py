import time

class LogItem():
    def __init__(self, time, error, message, class_name, function_name, import_name = None):
        self.time = time
        self.error = error
        self.message = message
        self.class_name = class_name
        self.function_name = function_name
        self.import_name = import_name

    def __str__(self):
        message = f"{self.time}: {self.error} in {self.class_name}.{self.function_name}" + \
            (f" (importing {self.import_name})" if self.import_name else "") + \
            self.message
        return message

def log(error, message, class_name, function_name, import_name = None):
    new_log_item = LogItem(time.time(),error,message,class_name,function_name,import_name)
    print(new_log_item)
    return new_log_item

class ConnectionError(Exception):
    """Exception raised when errors are found in WorkFlow connectivity"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)