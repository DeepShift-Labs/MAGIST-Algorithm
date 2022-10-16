# import xmlrpc.client
# import time
#
# proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:8080")
#
# # print(proxy.system.listMethods())
#
#
# params = {"point": {"x": 5, "y": 5}, "m": 2}
#
# params = {"n": 5.0, "scale": 10.0, "scalar": 1.0}
#
# start = time.time()
# move_right = proxy.pos_embedding(params)
# end = time.time()
#
# print(move_right)
# print("Time consumed in working: ",(end - start))



import time
import numpy as np

def __positional_embedding_function(n, scale=0.1, scalar=1):
	"""Computes the positional embedding.

	:param n: The position to be computed.
	:param scale: The scale of the positional embedding function.
	:param scalar: The scalar multiplier to the output of the positional embedding.

	:return: The positional embedding.
	"""
	x = np.multiply(n, scale)
	part1 = np.sin(np.multiply(n, x))
	part2 = np.sin(np.divide(1, x))
	return np.multiply(np.abs(np.multiply(part1, part2)), scalar)

values = []

for i in range(10):
	start = time.time()
	out = __positional_embedding_function(50)
	end = time.time()
	print("Time consumed in working: ",(end - start)*1000000000)
	print(out)
	values.append((end - start)*1000000000)

print(values)