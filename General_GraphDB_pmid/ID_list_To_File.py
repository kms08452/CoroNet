f_out = open("fox1_query.txt","w")

f = open("fox1_ID_list","r")


while True:
    temp = f.readline().rstrip("\n")
    if not temp:break
    f_out.write("\""+temp+"\",")

f.close()
f_out.close()