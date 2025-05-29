def strict(func):
    def wrapper(*args, **kwargs):
        annotation_values = list(func.__annotations__.values())
        arg_list = list(args)
        arg_list.extend(kwargs.values())
        for i in range(len(arg_list)):
            if not isinstance(arg_list[i], annotation_values[i]):
                raise ValueError(
                    "Типы переданных в вызов функции аргументов не соответствуют "
                    "типам аргументов, объявленным в прототипе функции."
                )
        res = func(*args, **kwargs)
        if not isinstance(res, annotation_values[-1]):
            raise ValueError(
                "Тип выходных данных функции не соответствует "
                "типу, объявленному в прототипе функции."
            )
        return res
    return wrapper
