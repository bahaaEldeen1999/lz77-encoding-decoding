import cv2
import numpy as np
print('enter path of tuples for lzzz eg:tuples.npy.....')
file_path = input()
print('enter path of charachters sent for lzzz eg:chars.npy.....')
file_path2 = input()
print('enter image first dimension.....')
n = input()
n = int(n)

print('enter image second dimension.....')
m = input()
m = int(m)
tot = n*m

encoded_tuple = np.load(file_path)
encoded_charachter = np.load(file_path2)

decoded_arr = np.array([])
k = 0
i = 0
while i < encoded_tuple.size:
    go_back = encoded_tuple[i]
    charachter = encoded_charachter[k]
    k += 1
    i += 1
    length = int(encoded_tuple[i])
    i += 1
    if(go_back == 0):
        decoded_arr = np.append(decoded_arr,charachter)
    else:
        sizy = decoded_arr.size
        for j in range(length):
            if(int(sizy-go_back+j)<decoded_arr.size ):
                decoded_arr = np.append(decoded_arr,decoded_arr[int(sizy-go_back+j)])
        if  decoded_arr.size<tot:
            decoded_arr = np.append(decoded_arr,charachter)
    


decoded_arr = np.reshape(decoded_arr,(n,m))
#save decoded image
cv2.imwrite('decoded.jpg', decoded_arr)