import os
import sys
import time
import pydoc
import inspect
import keyword
import datetime
import tokenize
import linecache


__UNDEF__ = []
DumpPath = ""


def SetDumpPath(dumps_path: str) -> None:
	global DumpPath
	DumpPath = dumps_path


def SaveDump(record: str, extend: str = None) -> None:
	dt = datetime.datetime.now()
	length = len(record)
	name = f"{dt.strftime('%Y-%m-%d')}_{length}.dmp"
	dumpfilepath = os.path.join(DumpPath, name)
	try:
		content = "\n".join((record, extend)) if extend is not None else record
		with open(dumpfilepath, "ab") as dumpfile:
			dumpfile.write(content.encode())
	except Exception:
		pass


def Lookup(name, frame, _locals) -> tuple:
	"""Find the value for a given name in the given environment."""
	if name in _locals:
		return "local", _locals[name]
	if name in frame.f_globals:
		return "global", frame.f_globals[name]
	if "__builtins__" in frame.f_globals:
		builtins = frame.f_globals["__builtins__"]
		if isinstance(builtins, dict):
			if name in builtins:
				return "builtin", builtins[name]
		else:
			if hasattr(builtins, name):
				return "builtin", getattr(builtins, name)
	return None, __UNDEF__


def ScanVars(reader, frame, localvars) -> list:
	"""Scan one line of Python and look up values of variables used."""
	cur_vars, lasttoken, parent, prefix, value = [], "", None, "", __UNDEF__
	for ttype, token, _, _, _ in tokenize.generate_tokens(reader):
		if ttype == tokenize.NEWLINE:
			break
		if ttype == tokenize.NAME and token not in keyword.kwlist:
			if lasttoken == ".":
				if parent is not __UNDEF__ and parent is not None:
					value = getattr(parent, token, __UNDEF__)
					cur_vars.append((prefix + token, prefix, value))
			else:
				where, value = Lookup(token, frame, localvars)
				cur_vars.append((token, where, value))
		elif token == ".":
			prefix += lasttoken + "."
			parent = value
		else:
			parent, prefix = None, ""
		lasttoken = token
	return cur_vars


def RecordVar(exc_info=None) -> str:
	_, _, tb = exc_info if exc_info else sys.exc_info()
	records = inspect.getinnerframes(tb, 5)

	list_records = ["Detail:"]
	frame, sourcefile, lnum, func, lines, index = records[-1]
	sourcefile = os.path.abspath(sourcefile) if sourcefile else "?"
	args, varargs, varkw, var_locals = inspect.getargvalues(frame)
	call = ""
	if func != "?":
		call = " in %s%s" % (func, inspect.formatargvalues(args, varargs, varkw, var_locals, formatvalue=lambda objvalue: f"={pydoc.text.repr(objvalue)}"))

	def reader(llnum=[lnum]):
		try:
			return linecache.getline(sourcefile, llnum[0])
		finally:
			llnum[0] += 1

	listvars = ScanVars(reader, frame, var_locals)

	list_records.append(f"  Current Dump Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
	list_records.append(f"  {sourcefile}{call}")
	if index is not None:
		i = lnum - index
		for line in lines:
			list_records.append("%6d %s" % (i, line.rstrip()))
			i += 1

	list_records.append("  Local Var:")

	done, dlist = {}, []
	for k, v in frame.f_globals.items():
		if not k.startswith("__"):
			dlist.append(f"    {k} = {pydoc.text.repr(v)}")

	for name, where, value in listvars:
		if name in done:
			continue
		if name in frame.f_globals:
			continue
		done[name] = 1
		if value is not __UNDEF__:
			if where == "global":
				name = "global " + name
			elif where == "builtin":
				name = "builtin " + name
			elif where != "local":
				name = where + name.split(".")[-1]
			dlist.append(f"    {name} = {pydoc.text.repr(value)}")
		else:
			dlist.append(f"    {name} undefined")

	list_records.append("\n".join(dlist))
	return "\n".join(list_records)
