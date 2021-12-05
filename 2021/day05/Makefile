day5: day5.c encode_video.h encode_video.c process_image.h process_image.c util.h util.c
	$(CC) -Wall -Wextra -Werror -O3 -o $@ $< encode_video.c process_image.c util.c -lm

.PHONY: clean
clean:
	rm day5
