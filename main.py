import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


img = cv2.imread('img1.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
n = img.shape[0]
m = img.shape[1]
tot = n*m
arr_flattend = np.reshape(img,tot)
# to not go out of bounds
arr_flattend = np.append(arr_flattend,0)
sliding_window = 100
look_ahead = 60
# go back / length of matching / next charachter to send
# at first i have empty search buffer and full look ahead buffer
encoded_tuple = np.array([])
encoded_charachter = np.array([],dtype=np.uint8); 
# initialize search buffer to be equal sliding_window-look_ahead
search_buffer_length = sliding_window-look_ahead
for i in range(search_buffer_length):
    encoded_tuple = np.append(encoded_tuple,(0,0))
    encoded_charachter = np.append(encoded_charachter,arr_flattend[i])

search_buffer_ptr = 0
while search_buffer_length+search_buffer_ptr < tot:
    current_character_ptr = search_buffer_length+search_buffer_ptr
    # match charachters in search buffer from look ahead buffer

    charchter_to_encode = arr_flattend[current_character_ptr]
    # to get max length search for all ocurence of charachter to encode in search buffer
    occurence_indecies = np.array([],dtype=np.int16)
    for i in range(search_buffer_ptr,search_buffer_length+search_buffer_ptr):
        if( arr_flattend[i] == charchter_to_encode ):
            occurence_indecies = np.append(occurence_indecies,i)
    # if there is a match find longest one
    max_match = 0
    max_match_go_back = 0
    # check if no match
    if( occurence_indecies.size == 0 ):
        encoded_charachter = np.append(encoded_charachter,charchter_to_encode)
        encoded_tuple = np.append(encoded_tuple,(0,0))
    else:
        
        for index in occurence_indecies:
                match_length = 0
                go_back = current_character_ptr - index
                current_index  = 0
                while current_character_ptr+current_index < tot  and arr_flattend[index+current_index] == arr_flattend[current_character_ptr+current_index]:
                    match_length += 1
                    current_index += 1
                if match_length > max_match:
                    max_match = match_length
                    max_match_go_back = go_back
        encoded_tuple = np.append(encoded_tuple,(max_match_go_back,max_match))
        encoded_charachter = np.append(encoded_charachter,arr_flattend[current_character_ptr+current_index])
    # slide the window to next look ahead buffer position
    search_buffer_ptr += max_match+1

print('encode charachter')
print(encoded_charachter.size)
print('encoded tuple')
print(encoded_tuple.size)
# h = 0
# i = 0
# while i < encoded_tuple.size:
#     if i%2 != 0:
#         if encoded_tuple[i] == 0:
#             h += 1
#         else:
#              h += encoded_tuple[i]
#     i += 1
# print("length of reconstruct")
# print(h)
# decoding
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
plt.figure(1)
plt.imshow(np.reshape(np.reshape(img,n*m),(n,m)),cmap='gray')

plt.figure(2)
plt.imshow(decoded_arr,cmap='gray')
plt.show()

    

