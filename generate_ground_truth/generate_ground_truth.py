import os, sys
tsv_directory = "../data/tsv/"
classified_directory = "../data/classified/"
tsv_files = os.listdir(tsv_directory)
classified_files = os.listdir(classified_directory)
prunedlist = []

for each in tsv_files:
    vid_id = each.split('.')[0]
    if "chunk_output.tsv" in each and vid_id+".classified.tsv" not in classified_files:
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
last_was_ad = False
while i <len(contents):
    precent_through = int(i/len(contents)*100)
    percent_str = str(precent_through)+"%"
    print(percent_str,end=' ')

    #print(contents[i])
    print(contents[i].split('\t')[1].strip())
    print(percent_str,end=' ')
    is_ad = ""
    if(last_was_ad):
        is_ad = input("\t \t\tHas ad?(Y/n/b): \n")
    else:
        is_ad = input("\t \t\tHas ad?(y/N/b): \n")

    if( is_ad == "" and last_was_ad):
        is_ad = "y"
    elif(is_ad == "" and not last_was_ad):
        is_ad = "n"

    #print(is_ad)
    if( is_ad == "n"):
        #code to mark as no
        last_was_ad = False
        write_array[i] = contents[i].strip()+' 0'
        i+=1
    elif(is_ad == 'y'):
        #code to mark as yes
        last_was_ad = True
        write_array[i] = contents[i].strip()+' 1'
        i+=1
    elif(is_ad == 'b'):
        #code to back up one
        i-=1
    else:
        #not one of the options
        print("Please enter 'y', 'n', or 'b'")

#print(write_array)
output_file = open(classified_directory+prunedlist[0].split('.')[0]+".classified.tsv",'w')
for line in write_array:
    output_file.write(line+'\n')
output_file.close()
tsv_file.close()
