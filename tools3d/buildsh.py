from cffi import FFI

ffibuilder = FFI()

# For every function that you want to have a python binding,
# specify its declaration here
ffibuilder.cdef("""
    void generateAssociatedLegendreFactors(const float N, float *data_out, const float * nodes, const unsigned int num_nodes);
                """)

# Here go the sources, most likely only includes and additional functions if necessary
ffibuilder.set_source("libspharm",
    """
    #include "spharm_tools.h"
    """, sources=["spharm_tools.c"])

if __name__ == "__main__":
    ffibuilder.compile()