import time

class LogItem():
    def __init__(self, time, error, message, class_name, function_name, identifier = None):
        self.time = time
        self.error = error
        self.message = message
        self.class_name = class_name
        self.function_name = function_name
        self.identifier = identifier

    def __str__(self):
        message = f"{self.time}: {self.error} in {self.class_name}.{self.function_name}" + \
            (f" (id: {self.identifier})" if self.identifier else "") + \
            self.message
        return message

def log(log, error, message, class_name, function_name, identifier = None):
    new_log_item = LogItem(time.time(),error,message,class_name,function_name,identifier)
    log.append(new_log_item)
    #return new_log_item

class ConnectionError(Exception):
    """Exception raised when errors are found in WorkFlow connectivity"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ActivationError(Exception):
    """Exception raised when nodes are unable to activate"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class MissingDataError(Exception):
    """Exception raised when nodes required data is missing"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)