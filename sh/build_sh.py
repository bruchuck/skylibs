from cffi import FFI
import os



ffibuilder = FFI()


print(os.environ)

# For every function that you want to have a python binding,
# specify its declaration here
ffibuilder.cdef(r"""
    void ySH(const float * normals, double *data_out, const unsigned int height, const unsigned int width, const int l, const int m);
                """)



source_dir = os.path.join(os.getcwd(), "sh", "src")
# Here go the sources, most likely only includes and additional functions if necessary
ffibuilder.set_source("_libsh",
    r"""
        #include "sh.h"
    """,
    sources=[os.path.join(source_dir, "sh.c")],
    relative_to=__file__,
    include_dirs = [source_dir]
)



if __name__ == "__main__":
    ffibuilder.compile(verbose=True)