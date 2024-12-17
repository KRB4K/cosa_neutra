from datetime import datetime

def only(d: str, keys: str|list[str]) -> dict:
	"""Returns a dictionary where only `keys` are kept"""
	if not '__iter__' in dir(keys) or isinstance(keys, str):
		return {keys: d[keys]}
	new = {}
	for k in keys:
		try:
			new[k] = d[k]
		except KeyError:
			continue
	return new

def sliced(iterable, n, stub=True):
    """Yields slices of n elements"""
    a = iter(iterable)
    while True:
        x = []
        for _ in range(n):
            try:
                y = next(a)
                x.append(y)
            except StopIteration:
                if stub and x:
                    yield x
                return
        yield x

def today():
    """Returns the current date at midnight"""
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)