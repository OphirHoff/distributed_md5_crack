#include <string.h>
#include <time.h>
#include "md5_source\md5.h"
#include "md5_source\md5.c"

void zeroFill(int number, char *result) {
    // Use snprintf to format the number with leading zeros
    snprintf(result, 11, "%010d", number); // 10 digits, padded with zeros
}
	

void printMD5Hex(const uint8_t digest[16]) {
    char buffer[33];  // 32 hex characters + 1 for the null terminator
    for (int i = 0; i < 16; i++) {
        sprintf(&buffer[i * 2], "%02x", digest[i]);
    }
    buffer[32] = '\0';  // Null-terminate the string
    printf("%s\n", buffer);  // Print the entire string at once
}

int compare(const uint8_t *arr1, const uint8_t *arr2, size_t length) {
    return memcmp(arr1, arr2, length * sizeof(uint8_t)) == 0;
}

int main() {
	
	char num[11];
	zeroFill(1234567, num);
	printf("%s\n", num);
	uint8_t target[16];
	md5String(num, target);
	
	printMD5Hex(target);

	double times[3];
	int k;
	for (k = 0; k < 3; k++) {
	
		time_t start, end;
		int i;
		time(&start);
		for(i = 0; i < 9999999;  i++) {
			
			uint8_t curr[16];
			char curr_num[11];
			zeroFill(i, curr_num);
			md5String(curr_num, curr);
			
			// printMD5Hex(curr);
			if (compare(curr, target, 16)) {
				time(&end);
				printf("Found! %s\n", curr_num);
				break;
			}
			
		}
		double delta_t = end-start;
		times[k] = delta_t;
	}
	
	double avg = (double)(times[0] + times[1] + times[2]) / 3;
	
	// printf("t1: %ld, t2: %ld\n", start, end);
	printf("Avg: %f sec.\n", avg);
	
	return 0;
	
}