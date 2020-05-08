#-*- coding:utf-8 -*-

f = open("DrugBank_MeSH_Mapping_output.csv","r")
f2 = open("DrugBank_MeSH_UniqueID_mapping_output.txt","r")
f3 = open("DrugBank_Corona_Node.txt","w")

input_list=[]
line = f.readline()
while True:
    line = f.readline()
    if not line: break
    if("\"" in line):
        temp3 = line.rstrip("\n").split("\"")[1]
        line = line.rstrip("\n").split("\"")[2]
        temp = line.rstrip("\n").split(",")
        temp2 = []
        temp2.append(temp3)
        temp2.append(temp[1])
        temp2.append(temp[2])
        input_list.append(temp2)
    else:
        temp = line.rstrip("\n").split(",")
        temp2 = []
        temp2.append(temp[0])
        temp2.append(temp[1])
        temp2.append(temp[2])
        input_list.append(temp2)

len = len(input_list)

cnt = 0

matched_list = []
while True:
    line = f2.readline()
    if not line: break
    temp = line.rstrip("\n").split("\t")
    matched_list.append(temp)

check = False
for i in input_list:
    # if(i[0] == "tetrakis(2-methoxyisobutylisocyanide)copper(i) tetrafluoroborate"):
    #     i[0] = i[0]
    for j in matched_list:

        if(i[0] == j[0]):
            i[1] = j[1]
            check = True

    if(check == True) :
        check = False
        if(i[1] == ''):
            temp3 = str(i[0]) + "@#$approved_drug" + "@#$" + "DrugBank:" + str(i[2]) + "@#$" + "DrugBank:" + str(i[2])  + "\n"
            #temp3 = str(i[0]) + "\t" + str("None") + "\t" + str(i[2]) + "\n"
            cnt = cnt + 1
        else:
            temp3 = str(i[0]) + "@#$approved_drug" + "@#$" + "MESH:" + str(i[1]) + "@#$" + "DrugBank:" + str(i[2]) + "\n"
            #temp3 = str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]) + "\n"
        f3.write(temp3)

    elif(check == False):
        check = False
        #temp3 = str(i[0]) + "\t" + str("None") + "\t" + str(i[2]) + "\n"
        temp3 = str(i[0]) + "@#$approved_drug" + "@#$" + "DrugBank:" + str(i[2]) + "@#$" + "DrugBank:" + str(i[2]) + "\n"
        cnt = cnt + 1
        f3.write(temp3)

#<id>:23646ID:BERN:4217803LABLE:entityOID:BERN:4217803remarkts:text:Tannic-acidtype:Drug
#Head and Neck Squamous Cell Carcinoma@#$disease@#$BERN:254577901

print(cnt)
f.close()
f2.close()
f3.close()