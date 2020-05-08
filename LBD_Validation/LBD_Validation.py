

f = open("C://Users//kms0845//Desktop//LionLBD//pmid_results_sorted_pro_2020_cnt_heading.csv","r")
f2 = open("C://Users//kms0845//Desktop//LionLBD//pmid_results_sorted_pro_2020_cnt_heading2.csv","w")
while True:
    line = f.readline()
    if not line : break
    if("\t" in line):
        print(line)
        temp = line.split("\t")
        if("PR" in str(temp[0])) : temp[1] = str(8)
        if ("PR" in str(temp[2])): temp[3] = str(8)
        temp2 = str(temp[0]) + "," + str(temp[1]) + "," + str(temp[2]) + "," + str(temp[3]) + "," + str(temp[4]) + "," + str(temp[5]) + "," + str(temp[6]) + "\n"
        print(temp2)
        f2.write(temp2)
    else: f2.write(line)
f.close()
f2.close()