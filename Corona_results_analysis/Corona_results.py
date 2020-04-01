
f = open("./bern_ACE2_results.txt","r")
f_out = open("./bern_SARS-COV-2_results.txt","w")


pmid_temp = "aaaa"
while True:
    line = f.readline()
    if not line : break
    #29458023	35	44	HCoV-229E	gene	CUI-less
    if("SARS-CoV-2" in line):
        f_out.write(line)
    elif("Severe Acute Respiratory Syndrome Coronavirus 2" in line):
        f_out.write(line)



f.close()
f_out.close()