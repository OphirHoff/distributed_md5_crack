import hashlib, time

def md5(num):
    md5_item = hashlib.md5()
    md5_item.update(str(num).encode().zfill(10))
    return md5_item.hexdigest()

num = 123456
target = md5(num).upper()
print(target)

times = []

# for k in range(3):
#     t1 = time.time()
#     for i in range(99999999):
#         curr = md5(i)
#         # print(curr)
#         if curr == target:
#             t2 = time.time()
#             print("Found!", str(i).zfill(10))
#             break

#     times.append(t2-t1)

# print("Avg: " + str(sum(times)/len(times)) + " sec.")