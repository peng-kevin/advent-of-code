all: day5draw day5sonar

day5draw: day5draw.c encode_video.h encode_video.c process_image.h process_image.c util.h util.c
	$(CC) -Wall -Wextra -Werror -O3 -o $@ $< encode_video.c process_image.c util.c -lm -fopenmp

day5sonar: day5sonar.c encode_video.h encode_video.c process_image.h process_image.c util.h util.c
	$(CC) -Wall -Wextra -Werror -O3 -o $@ $< encode_video.c process_image.c util.c -lm -fopenmp

.PHONY: clean
clean:
	rm day5draw day5sonar
