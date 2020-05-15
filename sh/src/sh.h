#define M_PI 3.14159265358979323846
#include <math.h>

double getY(int l, int m);
double getSH(int l, int m, const float * normal);
unsigned long int at( int x, int y, int z, int WIDTH, int DEPTH );
unsigned long int at2d( int x, int y, int WIDTH);
void ySH(const float * normals, double *data_out, const unsigned int height, const unsigned int width, const int l, const int m);