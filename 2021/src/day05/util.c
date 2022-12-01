#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include "util.h"

void* malloc_or_die(size_t size) {
    void *ptr = malloc(size);
    if(ptr == NULL) {
        perror("malloc failed");
        exit(1);
    }
    return ptr;
}