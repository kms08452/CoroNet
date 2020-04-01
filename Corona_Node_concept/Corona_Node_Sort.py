from operator import itemgetter

f = open("./bern_species_cui.txt","r")
f_out = open("./bern_species_cui_sorted.txt","w")
temp_list = []
while True:
    line = f.readline()
    if not line : break

    temp = line.split("@#$")
    temp_list.append(temp)

temp_list = sorted(temp_list, key = itemgetter(2,0,1))

i_temp = ["A","B","C"]
for i in temp_list:
    if(i_temp == i): continue
    if(i_temp[2] == i[2]): continue
    i_temp = i
    f_out.write(i[0])
    f_out.write("@#$")
    f_out.write(i[1])
    f_out.write("@#$")
    f_out.write(i[2])

f.close()
f_out.close()