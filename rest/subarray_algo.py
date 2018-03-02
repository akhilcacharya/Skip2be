test_array = [0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,0,0,0,0]
end = -1
for i in range(len(test_array)):
    if test_array[i] == 1 and i > end:
        #find maximizing endpoint
        max_sum = 0
        curr_sum = 0
        for x in range(i,len(test_array)):
            if test_array[x] ==1:
                curr_sum+=1
            else:
                curr_sum-=1
            if curr_sum>= max_sum:
                max_sum = curr_sum
                end = x    
        #after, don't restart search for
        #1 until after the end of the maximizing array
        print(i,end)