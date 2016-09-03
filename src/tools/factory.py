#!/usr/bin/env python3

#
#
# a Class of factories


class Factory():

	def __init__(self,cls,include_baseclase = True):
		self.cls = cls
		self.include_baseclase = include_baseclase
	
	@staticmethod
	def rec_subclasses(cls):
		for subcls in cls.__subclasses__():
			yield from Factory.rec_subclasses(subcls)
			yield subcls

	def __iter__(self):
		"""
		iterates over all subclasses of self.cls and self.cls
		"""
		yield from Factory.rec_subclasses(self.cls)

		if self.include_baseclase:
			yield self.cls

	def __call__(self,cls_name,*args):
		for cls in self:
			if cls.__name__ == cls_name:
				return cls(*args)
		return None


if __name__ == "__main__":
	import testclass
	import testcls
	f = Factory(testclass.test)
	t = f("tc")
	for cls in f:
		print(cls.__name__)
	print(t.name)
