

class Logger:
	def __init__(self, tag):
		self.tag = tag

	def write(self, msg):
		print ("[%s] %s" % (self.tag, msg))


class Util:
	def __init__(self):
		pass

	@staticmethod
	def flatten(l):
		return reduce(lambda x,y:x+y,l)