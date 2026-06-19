#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 1400

int main() {
    int arr[N];
    srand(time(NULL));
    for (int i = 0; i < N; i++) {
        arr[i] = rand() % N;
    }
	
	for (int i = 0; i < N-1; i++) {
        for (int j = 0; j < N-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }

    printf("Done Bubble Sort\n");
    return 0;
}