
f = open("./bern_species.txt","r")
f_out = open("./bern_species_cui.txt","w")

temp = [1,1,1,1]
while True:
    line = f.readline()
    if not line : break
    #29458023	35	44	HCoV-229E	gene	CUI-less
    temp = line.rstrip("\n").split("@#$")
    if("CUI-less" in temp[2]):
        f_out.write(temp[0])
        f_out.write("@#$")
        f_out.write(temp[1])
        f_out.write("@#$")
        f_out.write("CUI-less-"+str(temp[0]).replace("\"","_"))
        f_out.write("\n")
    else:
        f_out.write(temp[0])
        f_out.write("@#$")
        f_out.write(temp[1])
        f_out.write("@#$")
        f_out.write(temp[2])
        f_out.write("\n")


f.close()
f_out.close()