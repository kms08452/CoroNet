
f = open("./bern_results.txt","r")
f_out = open("./bern_document_count.txt","w")


pmid_temp = "aaaa"
while True:
    line = f.readline()
    if not line : break
    #29458023	35	44	HCoV-229E	gene	CUI-less
    temp = line.split("\t")
    temp_len = len(temp)
    if(temp_len >= 3):
        if(temp_len == 6):
            if(pmid_temp != temp[0]):
                f_out.write("-------------------------------!#$A!#\n")
            pmid_temp = temp[0]
            f_out.write(temp[0])
            f_out.write("@#$")
            f_out.write(temp[1])
            f_out.write("@#$")
            f_out.write(temp[2])
            f_out.write("@#$")
            f_out.write(temp[3])
            f_out.write("@#$")
            f_out.write(temp[4])
            f_out.write("@#$")
            f_out.write(temp[5])
            #f_out.write("\n")
        else:
            print("Strange Pattern")
            print(line)


f.close()
f_out.close()