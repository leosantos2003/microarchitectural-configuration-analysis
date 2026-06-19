#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define N 15000
#define PI 3.14159265358979323846

typedef struct {
    float real;
    float imag;
} Complex;

void fft(Complex *x, int n) {
    int logn = (int)(log2(n));
    for (int i = 0; i < n; i++) {
        int j = 0, bit;
        for (int k = 0; k < logn; k++) {
            bit = (i >> k) & 1;
            j |= bit << (logn - 1 - k);
        }
        if (j > i) {
            Complex temp = x[i];
            x[i] = x[j];
            x[j] = temp;
        }
    }
    
    for (int s = 1; s <= logn; s++) {
        int m = 1 << s;
        float angle = -2.0f * PI / m;
        Complex wm = {cosf(angle), sinf(angle)};
        for (int k = 0; k < n; k += m) {
            Complex w = {1.0f, 0.0f};
            for (int j = 0; j < m/2; j++) {
                Complex t = {w.real * x[k + j + m/2].real - w.imag * x[k + j + m/2].imag,
                             w.real * x[k + j + m/2].imag + w.imag * x[k + j + m/2].real};
                Complex u = x[k + j];
                x[k + j].real = u.real + t.real;
                x[k + j].imag = u.imag + t.imag;
                x[k + j + m/2].real = u.real - t.real;
                x[k + j + m/2].imag = u.imag - t.imag;
                Complex wtemp = {w.real * wm.real - w.imag * wm.imag, w.real * wm.imag + w.imag * wm.real};
                w = wtemp;
            }
        }
    }
}

int main() {
    Complex *x = (Complex *)malloc(N * sizeof(Complex));
    if (x == NULL) {
        printf("Erro ao alocar memoria para %d pontos\n", N);
        return 1;
    }
    for (int i = 0; i < N; i++) {
        x[i].real = rand() % 1000;
        x[i].imag = 0.0f;
    }

    fft(x, N);
    printf("Done FFT with %d points\n", N);
    free(x);
    return 0;
}