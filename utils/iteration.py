

def keep_while(func, items):
    for item in items:
        result = func(item)
        if result:
            yield item
