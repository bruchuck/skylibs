#include <math.h>
//#include <stdio.h>

#define M_PI 3.14159265358979323846

float amm(float m);
float amn(float m, float n);
float bmn(float m, float n);
float Pmm(float m, float x);
float Pmn(float m, float n, float x);
void generateAssociatedLegendreFactors(const float N, float *data_out, const float * nodes, const unsigned int num_nodes);
