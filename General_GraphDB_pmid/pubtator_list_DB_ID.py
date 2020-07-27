f_out = open("pubtator_list_DB_Fox1_result.txt","w")

f = open("pubtator_list_Fox1_result.txt","r")

while True:
    line = f.readline()
    if not line : break
    if('\n' == line) : continue
    if('|t|' in line or '|a|' in line) : continue
    temp = line.rstrip('\n').split('\t')
    if(temp[-1] == '-') : continue
    if('Mutation' in temp[-2]):
        continue
    temp2 = temp[-1]
    for i in temp2.split(";"):
        try:
            if(temp[-2] == 'Gene'): temp3 = "GeneID:"+str(i)
            elif (temp[-2] == 'Species'): temp3 = "TAXID:" + str(i)
            else:
                if(str(i) == ""):
                    continue
                temp3 = str(i)
        except:
            print("text_size_error")
            temp3 = temp3
        f_out.write(str(temp3)+"\n")


f.close()
f_out.close()