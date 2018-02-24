import os, sys
tsv_directory = "data/tsv/"
classified_directory = "data/classified/"
tsv_files = os.listdir(tsv_directory)
classified_files = os.listdir(classified_directory)
prunedlist = []

for each in tsv_files:
    vid_id = each.split('.')[0]
    if "chunk_output.tsv" in each and vid_id+".classified.txt" not in classified_files:
        prunedlist.append(each)
#print(prunedlist)

#exit if there are no files to classify
if len(prunedlist) == 0:
    print("no files to tag :)")
    sys.exit(0)

tsv_file = open(tsv_directory+prunedlist[0])


contents = tsv_file.readlines()
print(contents)
write_array = ["" for i in range(len(contents))]

print ("Now classifying: ", tsv_file.name)
print()

i = 0
while i <len(contents):

    print(contents[i].split('\t')[1],end='')
    is_ad = input("  Has ad?(y/N/b): ")

    if(len(is_ad) == 0 or is_ad == "n"):
        #code to mark as no
        line = contents[i]
        string = ""
        for each in line.split('\t')[1].split():
            string+='(n,'+each+') '
        write_array[i]=[
            line.split('\t')[0]+\
            '\t'+\
            string+'\n'
        ]
        i+=1
    elif(is_ad == 'y'):
        #code to mark as yes
        
        line = contents[i].split('\t')[1]
        string = ""
        words = line.split()
        for x in range(len(words)):
            print(str(x)+":"+words[x]+" ",end='')
        print()
        yes_range = input("range?(all):")
        if yes_range == "":
            yes_range = "0-"+str(len(words)-1)
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
            assert(low_num<high_num)
        except Exception as e:
            print("format is lower int followed by higher int")
            continue
        try:
            assert(low_num >=0 and low_num < len(words))
            assert(high_num >=0 and high_num < len(words))
        except AssertionError as e:
            print("numbers must be in specified range")
            continue
        
        for x in range(low_num):
            string+='(n,'+words[x]+') '
        for x in range(low_num,high_num+1):
            string+='(y,'+words[x]+') '
        for x in range(high_num+1,len(words)):
            string+='(n,'+words[x]+') '
        write_array[i]=[
           contents[i].split('\t')[0]+\
            '\t'+\
            string+'\n'
        ]
        i+=1
    elif(is_ad == 'b'):
        #code to back up one
        i-=1
    else:
        #not one of the options
        print("Please enter 'y', 'n', or 'b'")

print(write_array)
output_file = open(classified_directory+prunedlist[0].split('.')[0]+".classified.txt",'w')
for line in write_array:
    for text in line:
        output_file.write(text)
output_file.close
tsv_file.close