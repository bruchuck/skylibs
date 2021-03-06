from cffi import FFI
import os
from glob import glob
ffibuilder = FFI()

# For every function that you want to have a python binding,
# specify its declaration here
ffibuilder.cdef(r"""
    void ySH(const float * normals, double *data_out, const unsigned int height, const unsigned int width, const int l, const int m);
                """)




source_dir = os.path.join(os.getcwd(), "sh", "src")

if(not os.path.exists(source_dir)):
    source_dir = os.path.join(os.getcwd(), "skylibs", "sh", "src")
# Here go the sources, most likely only includes and additional functions if necessary
ffibuilder.set_source("_libsh",
    r"""
        #include "sh.h"
    """,
    #sources=[os.path.join(source_dir, "sh.c")],
    sources=[os.path.join("sh", "src", "sh.c")],
    include_dirs = [source_dir]
)



if __name__ == "__main__":
    ffibuilder.compile(verbose=True)