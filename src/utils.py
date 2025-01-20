from datetime import datetime, timedelta


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


def find_streaks(data):
    delta = timedelta(1)
    data = sorted(data, key=lambda x:x['created_at'])
    if not data:
        return []
    alls = []
    streak = [data[0]]
    for i, e in enumerate(data[1:], 1):
        if not (e['created_at'] - delta) == streak[-1]['created_at']:
            alls.append(streak)
            streak = []
        streak.append(e)
            
    alls.append(streak)
    return alls


def align_with_even_length(s1, s2, n=32):
     MIN = 4
     char = ' '
     m = n - len(s1) - len(s2)
     return s1 + char * max(MIN, m) + s2