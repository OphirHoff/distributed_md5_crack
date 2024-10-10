import sys, subprocess, time, os

def md5(target, range_start, range_end):
    # return subprocess.run(f"D:\\Cyber\\OS\\md5_crack\\C\\md5_source\\md5.exe {str(num).zfill(10)}", \
    #                       stdout=subprocess.PIPE).stdout.decode().strip()
    # os.system(f"D:\\Cyber\\OS\\md5_crack\\C\\md5_source\\md5.exe {str(num).zfill(10)}").stdout.decode().strip()

    return subprocess.run(f"D:\\Cyber\\OS\\md5_crack\\C\\search.exe {target} {range_start} {range_end}", stdout=subprocess.PIPE).stdout.decode()


target = "83A6725E1FFFD41FC1173AD0E68DA1A2"

output = md5(target, 0, 999999)
if "Found" in output:
    print(output)

# num = 1234
# target = md5(num)

# times = []

# for k in range(3):
#     t1 = time.time()
#     for i in range(9999):
#         curr = md5(i)
#         print(curr)
#         if curr == target:
#             t2 = time.time()
#             print("Found!", k)
#             break

#     times.append(t2-t1)

# print("Avg: " + str(sum(times)/len(times)))