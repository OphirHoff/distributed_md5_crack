#include <string.h>
#include "md5_source\md5.h"
#include "md5_source\md5.c"

#define MD5_UINT8_T_ARR_SIZE 16
#define HEX_STR_LEN 32
#define PASS_LEN 10

long long stoi(char *number)
{
    long long num = 0;
    
    while (*number)
    {
        num = num * 10 + *number - '0';
        number++;
    }
    
    return num;
}

void zeroFill(long long number, char *result) {
    // Use snprintf to format the number with leading zeros
    snprintf(result, 11, "%010lld", number); // 10 digits, padded with zeros
}

void printMD5Hex(const uint8_t digest[16]) {
    char buffer[33];  // 32 hex characters + 1 for the null terminator
    for (int i = 0; i < 16; i++) {
        sprintf(&buffer[i * 2], "%02X", digest[i]);
    }
    buffer[32] = '\0';  // Null-terminate the string
    printf("%s\n", buffer);  // Print the entire string at once
}

void hexToUint8Array(const char *hexStr, uint8_t *array) {

    for (size_t i = 0; i < HEX_STR_LEN; i++) {
        sscanf(hexStr + 2 * i, "%2hhx", &array[i]);
    }
}

int compare(const uint8_t *arr1, const uint8_t *arr2) {
    return memcmp(arr1, arr2, MD5_UINT8_T_ARR_SIZE) == 0;
}

int main(int argc, char *argv[]) {
	
	if (argc < 4) {
		printf("Need to pass argument, like so: %s <MD5 To find> <rangeStart> <rangeEnd>\n", argv[0]);
		return 1;
	}
	
	uint8_t target[MD5_UINT8_T_ARR_SIZE];
	hexToUint8Array(argv[1], target);
	long long rangeStart = stoi(argv[2]);
	long long rangeEnd = stoi(argv[3]);
	
	uint8_t curr[MD5_UINT8_T_ARR_SIZE];
	char curr_num[PASS_LEN];
	
	for(long long i = rangeStart; i <= rangeEnd; i++) {
		
		zeroFill(i, curr_num);
		md5String(curr_num, curr);

		if (compare(curr, target)) {
			printf("%lld", i);  // Output the found number
			return 0;
		}
	}
	// If not found, print X
	printf("X");
	return 0;
}