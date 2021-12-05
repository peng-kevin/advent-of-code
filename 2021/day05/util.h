#ifndef UTIL_H
#define UTIL_H

#include <stddef.h>

/**
 * Attempts to malloc size bytes, exits on failure
 */
void* malloc_or_die(size_t size);

static inline int min(int a, int b) {
     return a < b ? a : b;
}

static inline int max(int a, int b) {
     return a > b ? a : b;
}

#endif
