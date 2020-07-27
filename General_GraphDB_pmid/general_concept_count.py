f_out = open("general_concept_count_result.txt","w")



f = open("pubtator_list_DB_Fox1_result.txt","r")
db_list = []
while True:
    line = f.readline()
    if not line : break
    db_list.append(line.rstrip("\n"))

f.close()


f = open("general_concept_count_in","r")

while True:
    line = f.readline()
    if not line : break
    temp = line.rstrip("\n")
    cnt = 0
    for i in db_list:
        if (i == temp):
            cnt = cnt + 1
    f_out.write(temp+","+str(cnt)+"\n")

f.close()


f_out.close()