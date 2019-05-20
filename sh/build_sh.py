from cffi import FFI

ffibuilder = FFI()

# For every function that you want to have a python binding,
# specify its declaration here
ffibuilder.cdef("""
    void ySH(const float * normals, double *data_out, const unsigned int height, const unsigned int width, const int l, const int m);
                """)

# Here go the sources, most likely only includes and additional functions if necessary
ffibuilder.set_source("libsh",
    """
    #include "sh.h"
    """, sources=["sh.c"])

if __name__ == "__main__":
    ffibuilder.compile()