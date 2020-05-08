import itertools
from operator import itemgetter

f = open("./bern_niclosamide_edge_combination_sorted.txt","r")
f_out = open("./bern_niclosamide_edge_combination_sorted_merged.txt","w")


f_out_temp = []


temp = [1,1,1,1,1,1]
temp2 = []
pmid_list = []
while True:
    line = f.readline()
    if not line : break

    temp2 = line.rstrip("\n").split("@#$")
    
    if(temp[2] != temp2[2] or temp[5] != temp2[5]):
        if(temp == [1,1,1,1,1,1]) :
            temp = temp2
            pmid_list.append(temp2[-1])
            continue
        else :

            for i_cnt,i in enumerate(temp):
                f_out.write(i)
                if(i_cnt == 5):
                    f_out.write("@#$" + str(len(pmid_list)) )
                if(i != temp[-1]) : f_out.write("@#$")
                else : f_out.write("\n")
            temp = temp2
            pmid_list.clear()
            pmid_list.append(temp2[-1])
    else:
        check = False
        for j in pmid_list:
            if(j == temp2[-1]):
                check = True
                break
        if(check == True):
            continue
        temp.append(temp2[-1])
        pmid_list.append(temp2[-1])

f.close()
f_out.close()