#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 100

int main() {
    int A[N][N];
    int B[N][N];
    int C[N][N];

    srand(time(NULL));
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i][j] = rand() % 1000;
            B[i][j] = rand() % 1000;
            C[i][j] = 0;
        }
    }
	
	for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    printf("Done Matrix Multiplication\n");
    return 0;
}
