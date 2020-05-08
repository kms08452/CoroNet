
f = open("./bern_niclosamide_results.txt","r")
f_out = open("bern_special.txt", "w")

Special_key = ["Toxicity","Inhalation","Inhalation toxicity","Acute inhalation","Acute inhalation toxicity","Aroma","Inhaler","Aerosol","Spray","Airway","Respiratory","Respiratory disease","Asthma","COPD","Chronic Obstructive Pulmonary","Chronic Obstructive Pulmonary Disease"]
while True:
    line = f.readline()
    if not line : break
    #29458023	35	44	HCoV-229E	gene	CUI-less
    if ("|a|" in line or "|t|" in line):
        # 31391337|t|Niclosamide repurposed for the treatment of inflammatory airway disease.
        if ("|a|" in line):
            temp = line.split("|a|")
        else:
            temp = line.split("|t|")
        temp_len = len(temp)

        for j in Special_key:
            if(j not in line) : continue
            f_out.write(j)
            f_out.write("@#$")
            f_out.write("Special")
            f_out.write("@#$")
            f_out.write("BMDRC_Special"+j)
            f_out.write("\n")

f.close()
f_out.close()