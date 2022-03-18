import ctypes

grib = ctypes.cdll.LoadLibrary('./grib/go_grib.so')
parse_grib = grib.parse_grib
parse_grib.argtypes = [ctypes.c_int]
parse_grib.restype = ctypes.c_void_p
ptr = parse_grib(ctypes.c_int(0))
out = ctypes.string_at(ptr)
print(out.decode('utf-8')[1:20])


