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


int open_pipe(int fps, char* filename, enum Encoder encoder, int* outfd, pid_t* pid) {
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
        switch(encoder) {
            case MP4:
                execlp("ffmpeg", "ffmpeg", "-hide_banner", "-loglevel", FFMPEG_LOG_LEVEL, "-f", "image2pipe", "-framerate", fpsbuf, "-i", "-", "-c:v", "libx264", "-preset", "veryslow", "-crf", "0", "-pix_fmt", "yuv444p", filename, (char *) NULL);
                break;
            case MP4_RGB:
                execlp("ffmpeg", "ffmpeg", "-hide_banner", "-loglevel", FFMPEG_LOG_LEVEL, "-f", "image2pipe", "-framerate", fpsbuf, "-i", "-", "-c:v", "libx264rgb", "-preset", "veryslow", "-crf", "0", "-pix_fmt", "yuv444p", filename, (char *) NULL);
                break;
            case WEBP:
                execlp("ffmpeg", "ffmpeg", "-hide_banner", "-loglevel", FFMPEG_LOG_LEVEL, "-f", "image2pipe", "-framerate", fpsbuf, "-i", "-", "-vcodec", "libwebp", "-lossless", "1", "-compression_level", "6", "-q:v", "100", "-loop", "0", filename, (char *) NULL);
                break;
            case WEBP_LOSSY:
                execlp("ffmpeg", "ffmpeg", "-hide_banner", "-loglevel", FFMPEG_LOG_LEVEL, "-f", "image2pipe", "-framerate", fpsbuf, "-i", "-", "-vcodec", "libwebp", "-lossless", "0", "-compression_level", "6", "-q:v", "85", "-loop", "0", filename, (char *) NULL);
                break;
            case WEBP_SCALE:
                execlp("ffmpeg", "ffmpeg", "-hide_banner", "-loglevel", FFMPEG_LOG_LEVEL, "-f", "image2pipe", "-framerate", fpsbuf, "-i", "-", "-vf", "scale=300:-1", "-sws_flags", "sinc", "-vcodec", "libwebp", "-lossless", "1", "-compression_level", "6", "-q:v", "100", "-loop", "0", filename, (char *) NULL);
                break;
            case GIF:
                execlp("ffmpeg", "ffmpeg", "-hide_banner", "-loglevel", FFMPEG_LOG_LEVEL, "-f", "image2pipe", "-framerate", fpsbuf, "-i", "-", "-c:v", "gif", "-vf", "split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse", "-loop", "0", filename, (char *) NULL);
                break;
            case GIF_SCALE:
                execlp("ffmpeg", "ffmpeg", "-hide_banner", "-loglevel", FFMPEG_LOG_LEVEL, "-f", "image2pipe", "-framerate", fpsbuf, "-i", "-", "-c:v", "gif", "-vf", "fps=30,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse", "-loop", "0", filename, (char *) NULL);
                break;
        }
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
