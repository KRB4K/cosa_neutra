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