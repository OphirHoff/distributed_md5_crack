#include <string.h>
#include "md5_source\md5.h"
#include "md5_source\md5.c"

#define md5_uint8_t_arr_size 16

void zeroFill(int number, char *result) {
    // Use snprintf to format the number with leading zeros
    snprintf(result, 11, "%010d", number); // 10 digits, padded with zeros
}

void printMD5Hex(const uint8_t digest[16]) {
    char buffer[33];  // 32 hex characters + 1 for the null terminator
    for (int i = 0; i < 16; i++) {
        sprintf(&buffer[i * 2], "%02X", digest[i]);
    }
    buffer[32] = '\0';  // Null-terminate the string
    printf("%s\n", buffer);  // Print the entire string at once
}

void hexToUint8Array(const char *hexStr, uint8_t *array, int size) {
    size_t len = strlen(hexStr);
    size = len / 2; // Each byte is represented by two hex characters

    for (size_t i = 0; i < size; i++) {
        sscanf(hexStr + 2 * i, "%2hhx", &array[i]);
    }
}

int compare(const uint8_t *arr1, const uint8_t *arr2, size_t length) {
    return memcmp(arr1, arr2, length * sizeof(uint8_t)) == 0;
}

int main(int argc, char *argv[]) {
	
	if (argc < 4) {
		printf("Need to pass argument, like so: %s <MD5 To find> <rangeStart> <rangeEnd>\n", argv[0]);
		return 1;
	}
	
	uint8_t target[md5_uint8_t_arr_size];
	hexToUint8Array(argv[1], target, md5_uint8_t_arr_size);
	int rangeStart = atoi(argv[2]);
	int rangeEnd = atoi(argv[3]);
	
	int i;
	for(i = rangeStart; i <= rangeEnd; i++) {
		
		uint8_t curr[md5_uint8_t_arr_size];
		char curr_num[11];
		zeroFill(i, curr_num);
		md5String(curr_num, curr);

		if (compare(curr, target, md5_uint8_t_arr_size)) {
			printf("Found! %s\n", curr_num);
			break;
		}
	}
	return 0;
}