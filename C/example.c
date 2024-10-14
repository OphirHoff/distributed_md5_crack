#include <stdio.h>
#include <stdlib.h>

#define md5_uint8_t_arr_size 16

char* global_var = "hello";

void hello() {
    printf("Hello from C!\n");
}

int add(int a, int b) {
    return a + b;
}

void zeroFill(int number, char *result) {
    // Use snprintf to format the number with leading zeros
    snprintf(result, 11, "%010d", number); // 10 digits, padded with zeros
}

int tryThis() {
	
	int i = 123456789;
	
	char* curr_num = (char *)malloc(md5_uint8_t_arr_size);
	zeroFill(i, curr_num);
	printf("%s\n", curr_num);
	return i;
}

void setGlobalVar(char* x) {
	global_var = x;
}

void printGlobalVar() {
	printf("%s\n", global_var);
}

// int getGlobalVar() {
	// return global_var;
// }