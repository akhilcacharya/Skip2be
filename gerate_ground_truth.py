import os, sys
tsv_directory = "data/tsv/"
classified_directory = "data/classified/"
tsv_files = os.listdir(tsv_directory)
classified_files = os.listdir(classified_directory)
prunedlist = []

for each in tsv_files:
    vid_id = each.split('.')[0]
    if "token_output.tsv" in each and vid_id+".classified.tsv" not in classified_files:
        prunedlist.append(each)
#print(prunedlist)

#exit if there are no files to classify
if len(prunedlist) == 0:
    print("no files to tag :)")
    sys.exit(0)

tsv_file = open(tsv_directory+prunedlist[0])


contents = tsv_file.readlines()
#print(contents)
write_array = ["" for i in range(len(contents))]

print ("Now classifying: ", tsv_file.name)
print()

i = 0
WIND_LEN = 10
while i <len(contents):
    end_window = i+WIND_LEN
    if end_window > len(contents):
        end_window = len(contents)
    for x in range(i,end_window):
        print(contents[x].split('\t')[1].strip(),end=' ')
    print()
    is_ad = input("Has ad?(y/N/b): ")

    if(len(is_ad) == 0 or is_ad == "n"):
        #code to mark as no
        for x in range(i,end_window):
            write_array[x] = contents[x].strip()+' 0'
        
        i+=WIND_LEN
    elif(is_ad == 'y'):
        #code to mark as yes
        cnt = 0
        for x in range(i,end_window):
            print(str(cnt)+":"+contents[x].split('\t')[1].strip(),end = ' ')
            cnt+=1

        print()
        yes_range = input("range?(all):")
        if yes_range == "":
            yes_range = "0-"+str(end_window-i-1)
        #validate input
        try:
            assert('-' in yes_range)
            assert(len(yes_range.split('-')) == 2)
            low_num = yes_range.split('-')[0]
            high_num = yes_range.split('-')[1]
        except Exception as e:
            print("needs format like 0-2 with one hyphen between two digits")
            continue
        try:
            low_num = int(yes_range.split('-')[0])
            high_num = int(yes_range.split('-')[1])
            assert(low_num<=high_num)
        except Exception as e:
            print("format is lower int followed by higher int")
            continue
        try:
            assert(low_num >=0 and low_num < end_window-i)
            assert(high_num >=0 and high_num < end_window-i)
        except AssertionError as e:
            print("numbers must be in specified range")
            continue
        
        for x in range(i,i+low_num):
            write_array[x] = contents[x].strip()+' 0'
        for x in range(i+low_num,i+high_num+1):
           write_array[x] = contents[x].strip()+' 1'
        for x in range(i+high_num+1,end_window):
           write_array[x] = contents[x].strip()+' 0'
        i+=WIND_LEN
    elif(is_ad == 'b'):
        #code to back up one
        i-=WIND_LEN
    else:
        #not one of the options
        print("Please enter 'y', 'n', or 'b'")

#print(write_array)
output_file = open(classified_directory+prunedlist[0].split('.')[0]+".classified.tsv",'w')
for line in write_array:
    output_file.write(line+'\n')
output_file.close()
tsv_file.close()