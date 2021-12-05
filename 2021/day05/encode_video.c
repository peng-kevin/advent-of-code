#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#include "encode_video.h"

#define FFMPEG_LOG_LEVEL "info"
#define CODEC "libx265"
#define CODEC_PARAM "-x265-params"
#define CODEC_LOG_LEVEL "log-level=error"
#define CRF_SLOW "10"
#define CRF_FAST "20"
#define ENCODER_PRESET_SLOW "veryslow"
#define ENCODER_PRESET_FAST "veryfast"


int open_pipe(int fps, char* filename, int* outfd, pid_t* pid) {
    // create the pipe
    int pipefd[2];
    if (pipe(pipefd) == -1) {
        return -1;
    }
    //initiate ffmpeg
    *pid = fork();
    if (*pid == -1) {
        return -1;
    } else if(*pid == 0) {
        // convert arguments to strings
        char fpsbuf[256];
        snprintf(fpsbuf, 256, "%d", fps);
        close(pipefd[1]);
        dup2(pipefd[0], STDIN_FILENO);
        close(pipefd[0]);
        execlp("ffmpeg", "ffmpeg", "-hide_banner", "-loglevel", FFMPEG_LOG_LEVEL, "-f", "image2pipe", "-framerate", fpsbuf, "-i", "-", "-vcodec", "libwebp", "-lossless", "1", "-compression_level", "6", "-q:v", "80", "-loop", "0", filename, (char *) NULL);
        return -1;
    }
    close(pipefd[0]);
    *outfd = pipefd[1];

    return 0;
}

void close_pipe(int outfd, pid_t pid) {
    close(outfd);
    waitpid(pid, NULL, 0);
}
