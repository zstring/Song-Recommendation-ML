import spidermonkey
rt = spidermonkey.Runtime()
cx = rt.new_context()
cx.execute("var x = 3; x *= 4; x;")
12
class Orange(object):
	def is_ripe(self,arg):
		return "ripe %s" % arg
fruit = Orange()
cx.add_global("apple", fruit)
cx.execute('"Show me the " + apple.is_ripe("raisin");')
u'Show me the ripe raisin'