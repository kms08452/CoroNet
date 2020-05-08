
f = open("./bern_niclosamide_results.txt","r")
f_out = open("./bern_niclosamide_document_count.txt","w")

Special_key = ["Toxicity","Inhalation","Inhalation toxicity","Acute inhalation","Acute inhalation toxicity","Aroma","Inhaler","Aerosol","Spray","Airway","Respiratory","Respiratory disease","Asthma","COPD","Chronic Obstructive Pulmonary","Chronic Obstructive Pulmonary Disease"]

pmid_temp = "aaaa"
while True:
    line = f.readline()
    if not line : break
    #29458023	35	44	HCoV-229E	gene	CUI-less
    temp = line.split("\t")
    temp_len = len(temp)
    #-------------------------------!#$A!#

    if("|a|" in line or "|t|" in line):
        #31391337|t|Niclosamide repurposed for the treatment of inflammatory airway disease.
        if("|a|" in line) : temp = line.split("|a|")
        else :
            temp = line.split("|t|")
            f_out.write("-------------------------------!#$A!#\n")
        temp_len = len(temp)
        for j in Special_key:
            if (j not in line): continue
            # 31391337@#$0@#$11@#$Niclosamide@#$drug@#$MESH:D009534|BERN:4598003
            f_out.write(temp[0])
            f_out.write("@#$")
            f_out.write("123")
            f_out.write("@#$")
            f_out.write("123")
            f_out.write("@#$")
            f_out.write(j)
            f_out.write("@#$")
            f_out.write("Special")
            f_out.write("@#$")
            f_out.write("BMDRC_Special" + j)
            f_out.write("\n")

    if(temp_len >= 3):
        if(temp_len == 6):
            # if(pmid_temp != temp[0]):
            #     f_out.write("-------------------------------!#$A!#\n")
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