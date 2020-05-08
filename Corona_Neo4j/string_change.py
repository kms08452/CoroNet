
f = open("./bern_niclosamide_edge_combination_sorted_merged2.txt","r")
f_out = open("./bern_niclosamide_edge_combination_sorted_merged2_.txt","w")


pmid_temp = "aaaa"
while True:
    line = f.readline()
    if not line : break

    temp = line.replace("\"","_")
    f_out.write(temp)

f.close()
f_out.close()