from cffi import FFI

ffi = FFI()

ffi.cdef("double multiply(double, double);")

lib = ffi.dlopen('./libmult.dylib')

result = lib.multiply(6.5, 2)
print(f"The result is: {result}")
