#include "sh.h"

double getY(int l, int m){
    switch(l){
        case 0:
            return 0.5 * sqrt(1 / M_PI);
            break;
        case 1:
            return sqrt(3.0 / (4.0 * M_PI));
            break;
        case 2:
            if(m < 0 || m == 1)
                return  0.5 * sqrt(15.0 / M_PI);
            else if(m == 0)
                return 0.25 * sqrt(5.0 / M_PI) * 0.25;
            else
                return 0.25 * sqrt(15.0 / M_PI) * 0.5;
            break;
        default:
            return 0;
    }
}

double getSH(int l, int m, const float * normal){
    switch(l){
        case 0:
            return getY(l,m);
        case 1:
            switch(m){
                case -1:
                    return getY(l,m) * normal[1];
                case 0:
                    return getY(l,m) * normal[2];
                case 1:
                    return getY(l,m) * normal[0];
            }
        case 2:
            switch(m){
                case -2:
                    return getY(l,m) * normal[0] * normal[1];
                case -1:
                    return getY(l,m) * normal[1] * normal[2];
                case 0:
                    return getY(l,m) * (3.0 * normal[2] * normal[2] - 1.0);
                case 1:
                    return getY(l,m) * normal[0] * normal[2];
                case 2:
                    return getY(l,m) *(normal[0] * normal[0] - normal[1] * normal[1]);
            }

        default:
            return 0;
    }
}

unsigned long int at( int x, int y, int z, int WIDTH, int DEPTH ) {
    return z + DEPTH * (y + WIDTH * x);
}

unsigned long int at2d( int x, int y, int WIDTH) {
    return y + WIDTH * x;
}


void ySH(const float * normals, double *data_out, const unsigned int height, const unsigned int width, const int l, const int m){
    
    unsigned int i, j, c = 0;
    int degree = 2;
    int num_coef = (degree+1)*(degree+1);

    for(i= 0; i< height; i++){
        for(j= 0; j< width; j++){
                unsigned long int index = at2d(i,j, width);
                unsigned long int index_normals = at(i,j,0, width, 3);
                data_out[index] = getSH(l, m, &normals[index_normals]);
        }
    }
}
