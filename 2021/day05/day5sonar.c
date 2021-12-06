#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

#include "encode_video.h"
#include "process_image.h"
#include "util.h"

#define ARRAY_RESIZE_INC 3
#define COLOR_MAP_FILENAME "CET-L15.csv"
//defines the value at which the output color is saturated
#define MAXVAL 3
// how many iterations
#define N_ITERATIONS 4200
// how many iterations between each fram
#define ITERS_PER_FRAME 10

// reads the file and puts the lines in the out array formatted
// as [x1, y1, yx2, y2, x1, y1, x2, y2, ...] and puts information
// about the length of the array, and the minimum and maxmimum x and y values
// in the location of the pointer
void parse_file(FILE *file, int **lines, int *len, int *xmin, int *ymin, int *xmax, int *ymax) {
    int x1, y1, x2, y2;
    int xmin_l, ymin_l, xmax_l, ymax_l;
    int maxlen = ARRAY_RESIZE_INC;
    int len_l = 0;
    *lines = malloc_or_die(4 * maxlen * sizeof(**lines));
    if (fscanf(file, "%d,%d -> %d,%d\n", &x1, &y1, &x2, &y2) == 4) {
        (*lines)[0] = x1;
        (*lines)[1] = y1;
        (*lines)[2] = x2;
        (*lines)[3] = y2;
        len_l++;
        xmin_l = min(x1, x2);
        xmax_l = max(x1, x2);
        ymin_l = min(y1, y2);
        ymax_l = max(y1, y2);
    } else {
        *len = 0;
        return;
    }

    while (fscanf(file, "%d,%d -> %d,%d\n", &x1, &y1, &x2, &y2) == 4) {
        if (len_l >= maxlen) {
            int *next = malloc_or_die(4 * (maxlen + ARRAY_RESIZE_INC) * sizeof(*next));
            memcpy(next, *lines, 4 * maxlen * sizeof(**lines));
            maxlen += ARRAY_RESIZE_INC;
            free(*lines);
            *lines = next;
        }
        (*lines)[len_l * 4 + 0] = x1;
        (*lines)[len_l * 4 + 1] = y1;
        (*lines)[len_l * 4 + 2] = x2;
        (*lines)[len_l * 4 + 3] = y2;
        len_l++;
        xmin_l = min(xmin_l, min(x1, x2));
        xmax_l = max(xmax_l, max(x1, x2));
        ymin_l = min(ymin_l, min(y1, y2));
        ymax_l = max(ymax_l, max(y1, y2));
    }
    *len = len_l;
    *xmin = xmin_l;
    *xmax = xmax_l;
    *ymin = ymin_l;
    *ymax = ymax_l;
}

void write_image (struct Color *image, int width, int height, int fd) {
    ssize_t written;
    // write the header
    dprintf(fd, "P6\n%d %d 255\n", width, height);
    //write the image
    written = write(fd, image, width * height * sizeof(*image));
    if (written != width * height * (long int) sizeof(*image)) {
        fprintf(stderr, "Error writing to pipe\n");
        exit(1);
    }
}

void prepare_and_write_image (double *glow_map, double *line_map, int width, int height, struct ColorMap colormap, int nframes, int fd) {
    double *total_map = malloc_or_die(height * width * sizeof(*total_map));
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++) {
            int index = row * width + col;
            total_map[index] = glow_map[index] + line_map[index];
        }
    }
    struct Color *prepared_image = color_image(total_map, width, height, colormap, MAXVAL);
    free(total_map);
    for (int i = 0; i < nframes; i++) {
        write_image(prepared_image, width, height, fd);
    }
    free(prepared_image);
}

int main(int argc, char *argv[]) {
    if (argc < 3 || argc > 4) {
        fprintf(stderr, "usage: %s infile outfile [scale]\n", argv[0]);
        exit(1);
    }
    FILE *input = fopen(argv[1], "r");
    if (input == NULL) {
        perror("input");
        exit(1);
    }

    // will_scale is a boolean
    int will_scale = 0;
    // check if we have scale
    if (argc == 4 && !strcmp(argv[3], "scale")) {
        will_scale = 1;
        printf("will scale output\n");
    }

    // load color map
    struct ColorMap colormap = load_colormap(COLOR_MAP_FILENAME);
    if (colormap.length == -1) {
        fprintf(stderr, "Error: Failed to load colormap from %s\n", COLOR_MAP_FILENAME);
        exit(1);
    }

    //initiate FFmpeg
    int outfd;
    pid_t pid;
    // check whether we have a mp4 or webp
    enum Encoder encoder;
    int flen = strlen(argv[2]);
    if (flen >= 4 && !strcmp(&(argv[2][flen - 4]), ".mp4")) {
        if (will_scale) {
            printf("No option to scale mp4\n");
            exit(1);
        } else {
            encoder = MP4;
        }
    } else if (flen >= 5 && !strcmp(&(argv[2][flen - 5]), ".webp")) {
        if (will_scale) {
            encoder = WEBP_SCALE;
        } else {
            encoder = WEBP;
        }
    } else if (flen >= 4 && !strcmp(&(argv[2][flen-4]), ".gif")) {
        if (will_scale) {
            encoder = GIF_SCALE;
        } else {
            encoder = GIF;
        }
    } else {
        fprintf(stderr, "Error: only mp4 and webp4 output are supported. To select a format, choose a filename ending with .mp4 or .webp\n");
        exit(1);
    }
    if (open_pipe(60, argv[2], encoder, &outfd, &pid) == -1) {
        perror("Error");
        exit(1);
    }

    
    // load input
    int xmin, ymin, xmax, ymax, len;
    int *lines;
    parse_file(input, &lines, &len, &xmin, &ymin, &xmax, &ymax);
    fclose(input);
    if (len == 0) {
        fprintf(stderr, "Error: invalid format\n");
        exit(1);
    }
    // expand dimensions to a minimum of 16x16 for FFmpeg
    if (xmax - xmin < 16) {
        int diff = 16 - (xmax - xmin);
        xmin -= diff/2;
        xmax += ((double) diff + 0.5)/2;
    }
    if (ymax - ymin < 16) {
        int diff = 16 - (ymax - ymin);
        ymin -= diff/2;
        ymax += ((double) diff + 0.5)/2;
    }

    printf("xmin: %d, ymin: %d, xmax: %d, ymax: %d\n", xmin, ymin, xmax, ymax);

    int height = ymax - ymin + 1;
    int width = xmax - xmin + 1;
    double *map = calloc(height * width, sizeof(*map));
    // keep track of which frame we're on
    // iterate
    for (int i = 0; i < len; i++) {
        int x1 = lines[4 * i];
        int y1 = lines[4 * i + 1];
        int x2 = lines[4 * i + 2];
        int y2 = lines[4 * i + 3];

        int x = x1;
        int y = y1;
        // adds line to map one pixel at a time
        while (1) {
            map[width * (y - ymin) + (x - xmin)] += 1;
            if (x == x2 && y == y2) {
                break;
            }
            if (x2 > x) {
                x++;
            } else if (x2 < x) {
                x--;
            }
            if (y2 > y) {
                y++;
            } else if (y2 < y) {
                y--;
            }
        }
    }
    // create glow
    double *glowing_map = add_glow(map, width, height, 6, 1.5);
    free(map);
    // cut off all points greater than MAXVAl
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++) {
            if (glowing_map[row * width + col] > MAXVAL) {
                glowing_map[row * width + col] = MAXVAL;
            }
        }
    }
    double *sonar_glow_map = malloc_or_die(height * width * sizeof(*sonar_glow_map));
    double *sonar_line_map = malloc_or_die(height * width * sizeof(*sonar_line_map));
    memset(sonar_glow_map, 0, height * width * sizeof(*sonar_glow_map));
    memset(sonar_line_map, 0, height * width * sizeof(*sonar_line_map));
    // animate sonar map
    // only write frames after a full loop
    //printf("\n\n\n\n\n");
    double dir = -M_PI;
    for (int i = 0; i < N_ITERATIONS * 2; i++) {
        //printf("\033[1A\r%3d/%d\n", i + 1, N_ITERATIONS * 2);
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                int index = row * width + col;
                // distance between point and line
                double distance = fabs(cos(dir) * (height / 2.0 - row) - sin(dir) * (width / 2.0 - col));
                // check which side we are on
                double side = cos(dir) * (col - width/2.0) + sin(dir) * (row - height/2.0);
                if (distance < 1.5 && side > 0) {
                    sonar_line_map[index] = 1;
                    sonar_glow_map[index] = glowing_map[index];
                } else {
                    if (sonar_line_map[index] > 0) {
                        sonar_line_map[index] -= (10.0 / N_ITERATIONS);
                    }
                    if (sonar_glow_map[index] > 0) {
                        sonar_glow_map[index] -= ((1.0 * (double)MAXVAL) / N_ITERATIONS);
                    }

                }
            }
        }
        dir += (2.0 * M_PI) / N_ITERATIONS;
        if (i >= N_ITERATIONS && i % ITERS_PER_FRAME == 0) {
            prepare_and_write_image(sonar_glow_map, sonar_line_map, width, height, colormap, 1, outfd);
        }
    }
    close_pipe(outfd, pid);
    free(sonar_glow_map);
    free(sonar_line_map);
    free(lines);
    destroy_colormap(colormap);
}