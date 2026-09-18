def log(error, message, class_name, function_name):
    print(f"{error} in {class_name}.{function_name}: {message}")
    return error(message)