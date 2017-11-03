import pickle, sys

class TwitterData(object):
	""" Keep track of twitter data in a serialized fashion """
	def __init__(self, file_loc):
		""" Construct the object. Reads the given file_loc for
    any existing data. If it exists and is unpickleable, it
		loads it. Otherwise it uses an empty list
		"""
		self.data = []
		self.file_loc = file_loc
		try:
			sys.stdout.write("Attempting to read stored data from '{}'... ".format(file_loc))
			sys.stdout.flush()
			with open(file_loc, 'rb') as f:
				self.data = pickle.load(f)
				sys.stdout.write("Read {} tweets.\n".format(len(self.data)))
		except:
			sys.stderr.write("\n --> File not found or file not unpickleable -- using empty dataset\n")

	def add_data(self, data):
		""" Adds a data point to the object """
		self.data.append(data)
		self.serialize()

	def get_data(self):
		""" Returns all data stored in the object """
		return self.data

	def serialize(self):
		""" Serializes the object. Writes its data to a file """
		with open(self.file_loc, 'wb') as f:
			pickle.dump(self.data, f)
