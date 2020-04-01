import itertools
from operator import itemgetter

def edge_combination(concept_list = []):

    a = []
    b = []
    c = []
    d = []
    line_temp = []
    for i in concept_list:
        line_temp = [i[3],i[4],i[5]]
        if ('CUI-less' in line_temp[2]):
            line_temp[2] = "CUI-less-"+str(line_temp[0])
        a.append(line_temp)

    b = sorted(a, key=itemgetter(1, 2, 0))
    b_temp = ""
    for i in b:
        if(b_temp == i[2]):continue
        else :
            c.append(i)
            b_temp = i
    d = list(itertools.combinations(c,2))
    return d

f = open("./bern_document_count.txt","r")
f_out = open("./bern_edge_combination.txt","w")


pmid_temp = "aaaa"
concept_list = []
f_out_temp = []


while True:
    line = f.readline()
    if not line : break
    if(line == "-------------------------------!#$A!#\n"):
        print_temp = edge_combination(concept_list)
        for j in print_temp:
            f_out_temp2 = []
            f_out_temp2.append(j[0][0])
            f_out_temp2.append(j[0][1])
            f_out_temp2.append(j[0][2])
            f_out_temp2.append(j[1][0])
            f_out_temp2.append(j[1][1])
            f_out_temp2.append(j[1][2])
            f_out_temp2.append(pmid_temp)


            for k in f_out_temp2:
                f_out.write(str(k))
                if (k != f_out_temp2[-1]): f.write("@#$")
            f_out.write("\n")

    line = line.rstrip("\n")
    temp = line.split("@#$")
    temp_len = len(temp)
    if(temp_len >= 3):
        if(temp_len == 6):
            if(pmid_temp != temp[0]):
                concept_list.clear()
            pmid_temp = temp[0]
            concept_list.append(temp)
        else:
            print("Strange Pattern")
            print(line)


# #f_out_temp3 = sorted(f_out_temp, key=itemgetter(2, 5))
# f_out_temp3 = f_out_temp
# for i in f_out_temp3:
#     for j in i:
#         f_out.write(str(j))
#         if(j != i[-1]): f.write("@#$")
#     f_out.write("\n")

f.close()
f_out.close()