#import openpyxl
import fileinput
import time
import sys
import operator
import math

import requests
import json


from neo4j import GraphDatabase


#url = "bolt://175.121.89.176:8685"
url = "bolt://1.233.215.39:7687"

driver = GraphDatabase.driver(url,auth=("kms0845","neo4j"))


class Nodes_Noe4j:
    def __init__(self, type=""):
        self.type = type
        self.nodes = {}
        #self.nodes = self.all_nodes()
        self.cnt = 1
        self.data = {}
        self.open_query_filter_cnt = 521817

        self.read_nodes_lables = ["Chemical", "Disease", "Gene", "Species", "Pro"]
        self.lable_web_dictionary = {"Query": ["1"], "Drug": ["2"], "Disease": ["3"], "Mutation": ["4"], "Gene": ["5"], "Species": ["6"], "CellLine": ["7"],
                            "Hallmark": ["8"], "Pro" : ["9"], "Pro_Sub" : ["10"], "Chemical" : ["11"], "miRNA" : ["12"], "pathway" : ["13"], "approved_drug" : ["14"]}
        self.lable_reverse_dictionary = {1: "Chemical", 2: "Disease", 3: "Mutation", 4: "Gene", 5: "Species", 6: "CellLine",
                                    7: "Hallmark", 8: "Pro"}
        self.lable_dictionary = {"Chemical": 1, "Disease": 2, "Mutation": 3, "Gene": 4, "Species": 5, "CellLine": 6,
                            "Hallmark": 7, "Pro" : 8}
        # web layout
        self.m = [20, 140, 20, 100]
        self.w = 948 - self.m[1] - self.m[3]
        self.h = 600 - self.m[0] - self.m[2]
        self.center_x = self.w / 2 + self.m[1]
        self.center_y = self.h / 2 + self.m[0]
    def load_all_nodes(self):
        start_time = time.time()
        self.nodes = self.all_nodes()
        #print("all node loaded.")
        end_time = time.time()
        #print("Node Load Time: {} sec".format(end_time - start_time))
    def data_info_add(self):
        self.data['nodes'] = sorted(self.data['nodes'],key= lambda x: x['group'])

        import cx_Oracle as oci
        Oracle_url = "192.168.0.132"
        conn = oci.connect('neo4j/neo1234@192.168.0.132:1521/graph')
        #print(conn.version)
        cursor = conn.cursor()
        # self.lable_web_dictionary = {"Query": 1, "Chemical": 2, "Disease": 3, "Mutation": 4, "Gene": 5, "Species": 6,
        #                              "CellLine": 7,
        #                              "Hallmark": 8}
        for i in range(2,9):
            query_ID_temp = ""
            query_ID_temp2 = ""
            for j in self.data['nodes']:
                if(j['group'] == i) :
                    if(i == 5 and 'Gene' in j['cd']):
                        #query_ID_temp2 = query_ID_temp + "NODEID = \'" + j['cd'] + "\' Or "
                        query_ID_temp = query_ID_temp + "NODEID = \'" + j['cd'] + "\' Or "
                    query_ID_temp = query_ID_temp + "NODEID = \'" + j['cd'] + "\' Or "
            if(query_ID_temp == ""): continue
            if(i == 2):
                query_ID_temp = query_ID_temp.replace("NODEID","CHEMICALID")
                query_ID_temp = query_ID_temp.rstrip(" Or ")
                #print('select CHEMICALID, DESCRIPTION from NEO4J_CHEMICAL_POPUP_MERGE2 where ' + query_ID_temp)
                cursor.execute('select CHEMICALID, DESCRIPTION from NEO4J_CHEMICAL_POPUP_MERGE where '+query_ID_temp)
            if (i == 3):
                query_ID_temp = query_ID_temp.replace("NODEID", "DISEASEID")
                query_ID_temp = query_ID_temp.rstrip(" Or ")
                #print('select DISEASEID, DEFINITION from NEO4J_DISEASE_POPUP4 where ' + query_ID_temp)
                cursor.execute('select DISEASEID, DEFINITION from NEO4J_DISEASE_POPUP where ' + query_ID_temp)

            if (i == 5):
                query_ID_temp = query_ID_temp.replace("NODEID", "PROID")
                query_ID_temp = query_ID_temp.rstrip(" Or ")
                #print('select PROID, DEFINITION from NEO4J_GENE_POPUP_NEW where ' + query_ID_temp)
                cursor.execute('select PROID, DEFINITION from NEO4J_GENE_POPUP_NEW where ' + query_ID_temp)
            if (i == 6):
                query_ID_temp = query_ID_temp.replace("NODEID", "SPECIESID")
                query_ID_temp = query_ID_temp.rstrip(" Or ")
                #print('select SPECIESID, SPECIESPOPUP from NEO4J_SPECIES_POP_UP where ' + query_ID_temp)
                cursor.execute('select SPECIESID, SPECIESPOPUP from NEO4J_SPECIES_POP_UP where ' + query_ID_temp)
            #if(i == 5): continue
            for k in cursor.fetchall():
                for o, o_node in enumerate(self.data['nodes']):
                    if o_node['cd'] == k[0]:
                        o_node['tdesc'] = k[1]
                        self.data['nodes'][o]['tdesc'] = k[1]
                        break

        for j,j_node in enumerate(self.data['nodes']):
            if j_node['group'] == 1 :
                self.data['nodes'][j]['tdesc'] = "this is the target data"
            if 'tdesc' not in j_node:
                self.data['nodes'][j]['tdesc'] = 'Null'
                j_node['tdesc'] = 'Null'

        cursor.close()
        conn.close()
        #for i in a.data["nodes"]:

    def data_check(self):
        seach_check = False
        for cnt,i in enumerate(self.data["links"]):
            if('cnt' not in i['properties']):
                print("edge without cnt")
                print(i)
                #print(cnt)
            seach_check = False
            for j in self.data["nodes"]:
                if(j["id"] == i["startNode"]):
                    seach_check = True
                    break
            if(seach_check == False):
                print("source error : ",i["source"])
            seach_check = False
            for j in self.data["nodes"]:
                if(j["id"] == i["endNode"]):
                    seach_check = True
                    break
            if (seach_check == False):
                print("target error : ", i["target"])
    def conditional_start(self, arg):
        start_time = time.time()

        #a.load_all_nodes()
        #a.close_discovery_with_year(start_target_label_type="Species", start_target_id="TAXID:9606", end_target_label_type="Disease", end_target_id="MESH:D006331")

        #print(a.open_discovery())

        if(len(arg) >= 3) :

            # if(str(arg[3]) == 'Gene'):
            #     query_ID_temp = str(arg[2])
            #     arg[2] = "GeneID:"+query_ID_temp.split(":")[1]
            #
            # if(str(arg[5]) == 'Gene'):
            #     query_ID_temp = str(arg[4])
            #     arg[4] = "GeneID:" + query_ID_temp.split(":")[1]

            if(arg[1]== str(1)):
                arg_target_id = str(arg[2])
                arg_target_domain = str(arg[3])
                arg_start_year = 2020
                arg_end_year = 2020
                #arg_start_year = int(arg[4])
                #arg_end_year = int(arg[5])
                self.open_discovery_CORONET(target_label_type = arg_target_domain, target_id = arg_target_id, open_query_filter_cnt = 20, start_years = arg_start_year, end_years = arg_end_year)
            elif(arg[1] == str(2)):
                arg_start_target_id = str(arg[2])
                arg_start_target_domain = str(arg[3])
                arg_end_target_id = str(arg[4])
                arg_end_target_domain = str(arg[5])
                arg_start_year = int(arg[6])
                arg_end_year = int(arg[7])
                self.close_discovery_with_year(start_target_label_type= arg_start_target_domain , start_target_id= arg_start_target_id,
                                            end_target_label_type= arg_end_target_domain , end_target_id= arg_end_target_id, start_years = arg_start_year, end_years = arg_end_year)
            elif(arg[1] == str(3)) :
                arg_target_id = str(arg[2])
                arg_target_domain = str(arg[3])
                arg_start_year = int(arg[4])
                arg_end_year = int(arg[5])
                self.shortestpath_discovery_with_years(start_target_label_type= arg_target_domain, start_target_id= arg_target_id, start_years = arg_start_year, end_years = arg_end_year)
            elif (arg[1] == str(4)):
                arg_target_id = str(arg[2])
                arg_target_domain = str(arg[3])
                arg_start_year = int(arg[4])
                arg_end_year = int(arg[5])
                self.neighbor_discovery_with_years(start_target_label_type=arg_target_domain,
                                                    start_target_id=arg_target_id, start_years = arg_start_year, end_years = arg_end_year)
            else:
                print("arg error  : ",arg[1])
                driver.close()
                sys.exit()
        else :
            self.open_discovery_with_year(target_label_type = "Gene", target_id = "GeneID:7157", open_query_filter_cnt = 20, start_years = 2000, end_years = 2010)


        #(target_label_type = "Gene", target_id = "PR:000003035")



        self.data_check()
        #self.data_info_add()
        php_dump(self.data)
        end_time = time.time()
    def all_nodes(self):
        with driver.session() as session:
            return session.read_transaction(self.read_nodes)

    def read_nodes(self, tx):
        all_node = {}
        for record in tx.run("MATCH (A)"
                             "RETURN ID(A), A.ID, A.type"):
            if(record[2] in self.read_nodes_lables):
                all_node[record[1]] = record[0]
        return all_node

    def node_id(self, node1_name = "abc"):
        with driver.session() as session:
            return session.read_transaction(self.check_node_id, node1_name)
    @staticmethod
    def check_node_id(tx, node1_name: str = "abc"):
        temp001 = "MATCH (A {ID:\""+node1_name+"\"})\nRETURN ID(A)"
        try:
            return tx.run(temp001).single().value()
        except:
            #print("node id not found : "+node1_name)
            return -1
    def node_id_with_lable(self, node1_name: str = "abc", node1_domain: str = "Chemical"):
        if "Gene:" in node1_name:
            node1_name = "GeneID:"+node1_name.split(":")[1]
        with driver.session() as session:
            return session.read_transaction(self.check_node_id_with_lable, node1_name, node1_domain)
    @staticmethod
    def check_node_id_with_lable(tx, node1_name: str = "abc", node1_domain: str = "Chemical"):
        temp001 = "MATCH (A:"+node1_domain+" {ID:\""+node1_name+"\"})\nRETURN ID(A)"
        node = None
        try:
            for record in tx.run(temp001):
                for node in record:
                    return node
        except:
            print("node id not found : "+node1_name)
            return -1
        if(node == None):
            print("node id not found : " + node1_name)
            return -1
    def create_relationship(self, node1_name: str = "abc", node2_name: str = "abc", relationship_type: str = "knows", properties: dict = {}) :
        node1_id = 0
        node2_id = 0
        try:
            node1_id = self.nodes[node1_name]
        except:
            try : node1_id = self.node_id(node1_name)
            except:
                print(node1_name + " key error !")
                return
        try:
            node2_id = self.nodes[node2_name]
        except:
            try : node2_id = self.node_id(node2_name)
            except:
                print(node2_name + " key error !")
                return
        with driver.session() as session:
            session.read_transaction(self.tx_relationship, node1_id, node2_id, relationship_type, **properties)

    def create_relationship_with_domain(self, node1_name: str = "MESH", node1_domain: str = "Chemical", node2_name: str = "TAXID", node2_domain: str = "Chemical",relationship_type: str = "knows", properties: dict = {}) :
        node1_id = 0
        node2_id = 0
        try:
            node1_id = self.node_id_with_lable(node1_name, node1_domain)
        except:
            print(node1_name + " key error !")
            return
        try:
            node2_id = self.node_id_with_lable(node2_name, node2_domain)
        except:
            print(node2_name + " key error !")
            return
        with driver.session() as session:
            session.read_transaction(self.tx_relationship, node1_id, node2_id, relationship_type, **properties)

    def create_relationship_by_id(self, node1_id: int = 0, node2_id: int = 0, relationship_type: str = "knows", properties: dict = {}) :
        with driver.session() as session:
            session.read_transaction(self.tx_relationship, node1_id, node2_id, relationship_type, **properties)
    @staticmethod
    def tx_relationship(tx, id1, id2, relationship_type="Genus_Species_pair",**properties):
        try:
            if(len(properties) > 0):
                temp_properties = " {"
                for key in properties.keys():
                    contents = str(key)
                    if(contents) == "TYPE":
                        continue
                    contents = contents.replace("'", "\'")
                    contents = contents.replace(",", "\,")
                    temp_properties = temp_properties + key + " : " + str(properties[key]) + ", "
                temp_properties = temp_properties[:-2] + "}"
                temp = "MATCH (a),(b)\n" + "WHERE ID(a) = "+ str(id1)+ " AND ID(b) = " + str(id2) + "\n" + "CREATE (a)-[r:" + relationship_type + " " + temp_properties + "]->(b)\n"
            else :
                temp = "MATCH (a),(b)\n" + "WHERE ID(a) = "+ str(id1) + " AND ID(b) = " + str(id2) + "\n" + "CREATE (a)-[r:" + relationship_type + " " + "]->(b)\n"

            #print(temp)
            tx.run(temp)
            return

        except:
            print(id1 + " or " + id2 + " search failed")
            return

    def create_relationship_with_domain_with_direction(self, node1_name: str = "MESH", node1_domain: str = "Chemical", node2_name: str = "TAXID", node2_domain: str = "Chemical",relationship_type: str = "knows", properties: dict = {}) :
        node1_id = 0
        node2_id = 0
        try:
            node1_id = self.node_id_with_lable(node1_name, node1_domain)
        except:
            print(node1_name + " key error !")
            return
        try:
            node2_id = self.node_id_with_lable(node2_name, node2_domain)
        except:
            print(node2_name + " key error !")
            return
        with driver.session() as session:
            session.read_transaction(self.tx_relationship_with_direction, node1_id, node2_id, relationship_type, **properties)

    def create_relationship_by_id_with_direction(self, node1_id: int = 0, node2_id: int = 0, relationship_type: str = "knows", properties: dict = {}) :
        #only directed relationship is supported in neo4j currently.
        with driver.session() as session:
            session.read_transaction(self.tx_relationship_with_direction, node1_id, node2_id, relationship_type, **properties)
    def tx_relationship_with_direction(self, tx, id1, id2, relationship_type="Genus_Species_pair",**properties):
        try:
            if(len(properties) > 0):
                temp_properties = " {"
                for key in properties.keys():
                    contents = str(key)
                    if(contents) == "TYPE":
                        continue
                    contents = contents.replace("'", "\'")
                    contents = contents.replace(",", "\,")
                    temp_properties = temp_properties + key + " : " + str(properties[key]) + ", "
                temp_properties = temp_properties[:-2] + "}"
                temp = "MATCH (a),(b)\n" + "WHERE ID(a) = "+ str(id1)+ " AND ID(b) = " + str(id2) + "\n" + "CREATE (a)-[r:" + relationship_type + " " + temp_properties + "]->(b)\n"
            else :
                temp = "MATCH (a),(b)\n" + "WHERE ID(a) = "+ str(id1) + " AND ID(b) = " + str(id2) + "\n" + "CREATE (a)-[r:" + relationship_type + " " + "]->(b)\n"

            #print(temp)
            tx.run(temp)
            return

        except:
            print(id1 + " or " + id2 + " search failed")
            return

    def add_nodes(self, label_type, **properties):
        with driver.session() as session:
            self.nodes[properties['ID']] =  session.write_transaction(self.tx_nodes, label_type, **properties)
            return
    @staticmethod
    def tx_nodes(tx, label_type, **properties):
        try:

            temp = "CREATE(a:" + label_type+ " {"
            for key in properties.keys():
                contents = str(key)
                contents = contents.replace("'", "\'")
                contents = contents.replace(",", "\,")
                temp = temp + key + " : {" + contents + "}, "
            temp = temp[:-2] +"}) \n"+ "RETURN ID(a)"
            #print (temp)
            return tx.run(temp, **properties).single().value()


            # contents = ""
            # for key in properties.keys():
            #     contents = str(properties[key])
            #     contents = contents.replace("'", "\'")
            #     contents = contents.replace(",", "\,")
            #     temp = temp + key + " : '" + contents + "', "
            # temp = temp[:-2]+"})\n"
            # temp = temp +"RETURN ID(a)"
            #print(temp)


        except Exception as ex:
            print(properties['ID'] + ' : ' + label_type + " node add error")
            return -1


    def open_discovery(self, target_label_type = "Gene", target_id = "PR:000003035") :
        result = {}
        result2 = {}
        sorted_cnt = {}
        visit = []
        temp3 = 0
        with driver.session() as session:
            result = session.read_transaction(self.open_discovery_tx, target_label_type, target_id, self.open_query_filter_cnt)
            result2 = session.read_transaction(self.open_discovery_tx2, target_label_type, target_id)

            visit2 = False
            for i,i_id in enumerate(result.keys()):
                print(i)
                visit2 = False
                for j, j_id in enumerate(result2.values()):
                    temp3 = self.check_relationships_by_id(i_id, j_id)
                    if(temp3 > 0) : visit2 = True
                    break
                if(visit2 == True): visit.append(False)
                else : visit.append(True)
            for i,i_id in enumerate(result.keys()):
                cnt = 0
                if(visit[i] == False) :
                    result[i_id] = cnt
                    continue
                for j,j_id in enumerate(result2.values()):
                    if(j == 0): continue # j = 0 : start node
                    temp3 = self.check_relationships_by_id(i_id,j_id)
                    #print(temp3)
                    if(temp3 > 0) : cnt += 1
                result[i_id] = cnt

        print("MATCH(n)")
        print("WHERE ID(n) IN[")
        print(result2.values())
        print("]\nRETURN n")
        print("sorted results : ")
        sorted_cnt = sorted(result.items(),key=operator.itemgetter(1), reverse= True)
        for i, n in enumerate(sorted_cnt):
            if(i == 10): break
            print(str(n[0]),end=",")


        return 1
    @staticmethod
    def open_discovery_tx(tx, target_label_type="Gene", target_id="PR:000003035", query_filter_cnt = 0):
        result_nodes = {}
        #run_text = "Match (Gene00001: "+target_label_type+" {ID: \""+target_id+ "\" })-[s]-(Gene_web)-[r]-(n)\n"+"where toInteger(split(Gene_web.count, \";\")[-1]) > 521817\n"+"return ID(Gene_web)"


        run_text = ""
        run_text = run_text + "MATCH (General_Node00001: " + target_label_type + " {ID: \"" + target_id + "\"})-[s] - (General_Node_web)\n"
        run_text = run_text + "with distinct General_Node00001, General_Node_web\n"
        run_text = run_text + "Order by toInteger(split(General_Node_web.count, \";\")[-1]) desc limit 10 \n"
        run_text = run_text + "Match (General_Node_web)-[r]-(n)\n"
        run_text = run_text + "where toInteger(split(n.count, \";\")[-1]) > "+str(query_filter_cnt)+" and (General_Node00001) <> (n) and not (General_Node00001)--(n)\n"
        run_text = run_text + "return distinct ID(n)"
        print(run_text)
        print("number of second layers : ")

        for record in tx.run(run_text):
            result_nodes[record[0]] = 1
        print(len(result_nodes))
        return result_nodes
    @staticmethod
    def open_discovery_tx2(tx, target_label_type="Gene", target_id="PR:000003035"):
        result_nodes = {}

        run_text = ""
        run_text = run_text + "MATCH (General_Node00001: " + target_label_type + " {ID: \"" + target_id + "\"})-[s] - (General_Node_web)\n"
        run_text = run_text + "with distinct General_Node00001, General_Node_web\n"
        run_text = run_text + "Order by toInteger(split(General_Node_web.count, \";\")[-1]) desc limit 10 \n"
        run_text = run_text + "with General_Node00001 + collect(General_Node_web) as temp_results\n"
        run_text = run_text + "unwind temp_results as out_results\n"
        run_text = run_text + "return id(out_results),out_results.ID"
        #run_text = run_text + "LIMIT 10"
        #apoc.node.degree(n,\"\")
        print(run_text)
        for record in tx.run(run_text):
            print(str(record[0]) + "<->" + str(record[1]))
            #print(record[1] + " count = " + str(result_counts[record[1]]))
            result_nodes[record[1]] = record[0]

        # sorted_cnt = sorted(result_nodes.items(),key=operator.itemgetter(1), reverse= True)
        # for i, n in enumerate(sorted_cnt):
        #     if(i == 10): break
        #     print(str(n[0]),end=",")
        return result_nodes

    def open_discovery_CORONET(self, target_label_type = "Gene", target_id = "GeneID:7157", open_query_filter_cnt = 20, start_years = 2000, end_years = 2010) :
        result = {}
        result2 = {}
        sorted_cnt = {}
        visit = []
        temp3 = 0
        with driver.session() as session:
            result = session.read_transaction(self.open_discovery_tx_CORONET, target_label_type, target_id, open_query_filter_cnt, start_years, end_years)

        for i in self.data['nodes']:
            if(i["properties"]["cd"] == target_id):
                i["labels"] = ["1"] # Query : 1
        return 1
    def open_discovery_tx_CORONET(self, tx, endNode_label_type="Gene", endNode_id="GeneID:7157", query_filter_cnt = 0, start_years = 2000, end_years = 2010):

        result_nodes = {}
        #run_text = "Match (Gene00001: "+endNode_label_type+" {ID: \""+endNode_id+ "\" })-[s]-(Gene_web)-[r]-(n)\n"+"where toInteger(split(Gene_web.count, \";\")[-1]) > 521817\n"+"return ID(Gene_web)"

        #MATCH (General_Node00001: Gene {ID: "GeneID:7157"})-[s] - (General_Node_web)
        #WHERE exists(s.cnt_2009) or exists(s.cnt_2008) or exists(s.cnt_2007) or exists(s.cnt_2006) or exists(s.cnt_2005) or exists(s.cnt_2004) or exists(s.cnt_2003) or exists(s.cnt_2002) or exists(s.cnt_2001) or exists(s.cnt_2000)
        #WITH s, coalesce(s.cnt_2009,0) + coalesce(s.cnt_2008, 0) +  coalesce(s.cnt_2007, 0) +  coalesce(s.cnt_2006, 0) +  coalesce(s.cnt_2005, 0) +  coalesce(s.cnt_2004, 0) +  coalesce(s.cnt_2003, 0) +  coalesce(s.cnt_2002, 0) +  coalesce(s.cnt_2001, 0) +  coalesce(s.cnt_2000, 0) as cnt
        #order by cnt desc
        #return s,cnt
        #limit 10

        cnt_text = ""
        coalesce_text = ""
        cnt_property_text = ""
        run_text = ""
        run_text = run_text + "MATCH (General_Node00001: " + endNode_label_type + " {ID: \"" + endNode_id + "\"})-[s:PMID_cooccurnce] - (General_Node_web)\n"
        #cnt_text = "WHERE "
        #coalesce_text = "WITH General_Node00001, General_Node_web, s, "
        # for i in range(start_years, end_years) :
        #     cnt_property_text = "cnt_" + str(i)
        #     cnt_text = cnt_text + "exists(s."+cnt_property_text+") or "
        #     coalesce_text = coalesce_text + "coalesce(s."+cnt_property_text+", 0) +"
        #cnt_text = cnt_text[:-3]
        #coalesce_text = coalesce_text[:-2] + " as cnt"
        # run_text = run_text + cnt_text + '\n'
        # run_text = run_text + coalesce_text + '\n'
        # run_text = run_text + "Order by cnt desc \n"
        run_text = run_text + "return s, General_Node00001, General_Node_web \n"
        run_text = run_text + "Order by s.PMID_CNT desc \n"
        run_text = run_text + "limit 100"
        #print(run_text)

        nodes = []
        links_temp = []
        nodes_propreties = {}
        links_properties = {}
        for edge in tx.run(run_text):
            edges = edge[0]
            total_edge_cnt = edge[0]['PMID_CNT']
            start_node = edge[0].start_node
            end_node = edge[0].end_node

            links_properties["cnt"] = total_edge_cnt
            links_temp.append({"type": "PMID_test1", "startNode": str(edges.start_node.id), "endNode": str(edges.end_node.id), "properties" : links_properties})

            nodes_propreties = {}
            nodes_propreties["cd"] = start_node._properties['ID']
            nodes_propreties["nm"] = start_node._properties['text']
            nodes.append({"id":str(start_node.id),"labels":self.lable_web_dictionary[start_node._properties['type']],"properties":nodes_propreties})

            nodes_propreties = {}
            nodes_propreties["cd"] = end_node._properties['ID']
            nodes_propreties["nm"] = end_node._properties['text']
            nodes.append({"id": str(end_node.id),
                          "labels": self.lable_web_dictionary[end_node._properties['type']], "properties":nodes_propreties})
        # print(links)
        links = []

        General_Node00001 = start_node
        #for starting point of open query

        sorted_links = sorted(links_temp, key=lambda k: k['properties']['cnt'], reverse=True)

        sorted_nodes = []
        for i in range(0, 20):
            links_properties = {}
            links_properties["cnt"] = sorted_links[i]['properties']['cnt']
            links.append({'type' : sorted_links[i]['type'], 'startNode' : sorted_links[i]['startNode'],'endNode' : sorted_links[i]['endNode'], 'properties': links_properties})
            sorted_nodes.append(sorted_links[i]['startNode'])
            sorted_nodes.append(sorted_links[i]['endNode'])

        settype_nodes = set()
        ex_nodes = []
        for d in sorted_nodes:
            t = tuple([d])
            if t not in settype_nodes:
                settype_nodes.add(t)
                ex_nodes.append(d)

        final_nodes = []
        for i in ex_nodes:

            for j in nodes:
                if (j['id'] == i):
                    final_nodes.append(j)
                    break



        # first_layer_len = len(final_nodes)
        # arcradius = 100
        # circleradius = 10
        # n = first_layer_len
        # m = [20, 140, 20, 100]
        # w = 948 - m[1] - m[3]
        # h = 600 - m[0] - m[2]
        # center_x = w / 2 + m[1]
        # center_y = h / 2 + m[0]
        #
        # for i in range(0,first_layer_len):
        #     if(final_nodes[i]['cd'] == endNode_id):
        #         final_nodes[i]['fix_x'] = center_x
        #         final_nodes[i]['fix_y'] = center_y
        #     else:
        #         ang = (math.pi * 2 * i) / (first_layer_len-1)
        #         circle_x = arcradius * math.sin(ang) + center_x
        #         circle_y = arcradius * math.cos(ang) + center_y
        #         final_nodes[i]['fix_x'] = circle_x
        #         final_nodes[i]['fix_y'] = circle_y


        self.data['nodes'] = final_nodes
        self.data['links'] = links

        #MATCH (SSS)
        #Where ID(SSS) = 12359409
        #With SSS
        #Match (a)
        #Where ID(a) = 12359409 Or ID(a) = 132876 Or ID(a) = 144511 Or ID(a) = 142261 Or ID(a) = 126034 Or ID(a) = 144942 Or ID(a) = 125798 Or ID(a) = 144570 Or ID(a) = 131423 Or ID(a) = 143620 Or ID(a) = 136735 Or ID(a) = 143082 Or ID(a) = 125821 Or ID(a) = 205145 Or ID(a) = 129790 Or ID(a) = 79141798 Or ID(a) = 79133404 Or ID(a) = 79133405 Or ID(a) = 126000 Or ID(a) = 133595 Or ID(a) = 145655 With SSS, a
        #Match (a)-[r]-(b)
        #Where not (SSS)--(b)
        #return ID(b),count(*)
        #order by count(*) Desc
        #limit 100



        run_text = ""
        run_text = run_text + "MATCH (SSS)"+"\n"
        run_text = run_text + "Where ID(SSS) = " + str(General_Node00001.id) + "\n"
        run_text = run_text + "With SSS\n"
        run_text = run_text + "Match (a)\n"
        nodes_text = "Where "

        first_layer_node_list = []
        for i in final_nodes:
            nodes_text = nodes_text + "ID(a) = " + str(i["id"]) + " Or "
            first_layer_node_list.append(i["id"])
        nodes_text = nodes_text[:-3]
        run_text = run_text + nodes_text
        run_text = run_text + "With SSS, a\n"
        run_text = run_text + "Match (a)-[r]-(b)\n"
        run_text = run_text + "Where not (SSS)--(b)\n"
        run_text = run_text + "with a,r,b\n"
        run_text = run_text + "return ID(b),count(*)\n"
        run_text = run_text + "order by count(*) Desc\n"
        run_text = run_text + "limit 10\n"


        #print("number of second layers : ")


        #-----------------------------------------------------------------------------------------------------------
        #second layer part
        # print(links)
        temp_links = []
        first_second_edges = []
        second_layer_nodes = []
        second_layer_cnt = 0
        for record in tx.run(run_text):
            second_layer_nodes.append(record[0])
            second_layer_cnt = record[1]


        run_text = ""
        run_text = run_text + "MATCH (SSS)" + "\n"
        run_text = run_text + "Where ID(SSS) = " + str(General_Node00001.id) + "\n"
        run_text = run_text + "With SSS\n"
        run_text = run_text + "Match (a)\n"
        nodes_text = "Where "
        first_layer_node_list = []
        for i in final_nodes:
            nodes_text = nodes_text + "ID(a) = " + str(i["id"]) + " Or "
            first_layer_node_list.append(i["id"])
        nodes_text = nodes_text[:-3]
        run_text = run_text + nodes_text
        run_text = run_text + "With SSS, a\n"
        run_text = run_text + "Match (b)\n"
        nodes_text = "Where "
        first_layer_node_list = []
        for i in second_layer_nodes:
            nodes_text = nodes_text + "ID(b) = " + str(i) + " Or "
        nodes_text = nodes_text[:-3]
        run_text = run_text + nodes_text +"\n"
        run_text = run_text + "With a, b\n"
        run_text = run_text + "Match (a)-[r]-(b)\n"
        # cnt_text = "WHERE "
        # coalesce_text = "WITH a, r, b, "
        # for i in range(start_years, end_years) :
        #     cnt_property_text = "cnt_" + str(i)
        #     cnt_text = cnt_text + "exists(r." + cnt_property_text + ") or "
        #     coalesce_text = coalesce_text + "coalesce(r." + cnt_property_text + ", 0) +"
        # cnt_text = cnt_text[:-3]
        # coalesce_text = coalesce_text[:-2] + " as cnt"
        # run_text = run_text + cnt_text + '\n'
        # run_text = run_text + coalesce_text + '\n'
        run_text = run_text + "return r,b\n"
        run_text = run_text + "Order by r.PMID_CNT desc \n"
        run_text = run_text + "limit 100"

        links_temp = []



        for edge in tx.run(run_text):
            edges = edge[0]
            total_edge_cnt = edge[0]['PMID_CNT']
            end_node = edge[1]

            #a.data['links'].append({"startNode": str(edges.start_node.id), "endNode": str(edges.end_node.id), "cnt": total_edge_cnt, "lables": 1})
            links_properties = {}
            links_properties["cnt"] = total_edge_cnt
            self.data['links'].append(
                {"type": "PMID_TEST2", "startNode": str(edges.start_node.id), "endNode": str(edges.end_node.id),"properties" : links_properties})

            nodes_propreties = {}
            nodes_propreties["cd"] = end_node._properties['ID']
            nodes_propreties["nm"] = end_node._properties['text']
            self.data['nodes'].append(
                {"id": str(end_node.id),
                 "labels": self.lable_web_dictionary[end_node._properties['type']],"properties":nodes_propreties})


        nodes = []
        nodes = self.data['nodes']
        settype_nodes = set()
        ex_nodes = []
        for d in nodes:
            t = tuple([d["id"]])
            if t not in settype_nodes:
                settype_nodes.add(t)
                ex_nodes.append(d)
        #
        self.data['nodes'].clear()

        # second_layer_len = len(ex_nodes)-first_layer_len
        #
        # circleradius = 10
        #
        # ang_cnt = 0
        for i in ex_nodes:
        #     if('fix_x' in i and 'fix_y' in i):
        #         self.data['nodes'].append(i)
        #         continue
        #     ang_cnt = ang_cnt + 1
        #     ang = (math.pi * 2 * ang_cnt) / second_layer_len
        #     circle_x = (arcradius + 100) * math.sin(ang) + center_x
        #     circle_y = (arcradius + 100) * math.cos(ang) + center_y
        #     i['fix_x'] = circle_x
        #     i['fix_y'] = circle_y
             self.data['nodes'].append(i)


        return result_nodes

    def open_discovery_with_year(self, target_label_type = "Gene", target_id = "GeneID:7157", open_query_filter_cnt = 20, start_years = 2000, end_years = 2010) :
        result = {}
        result2 = {}
        sorted_cnt = {}
        visit = []
        temp3 = 0
        with driver.session() as session:
            result = session.read_transaction(self.open_discovery_tx_with_year, target_label_type, target_id, open_query_filter_cnt, start_years, end_years)

        for i in self.data['nodes']:
            if(i["cd"] == target_id):
                i["group"] = 1 # Query : 1
        return 1
    def open_discovery_tx_with_year(self, tx, target_label_type="Gene", target_id="GeneID:7157", query_filter_cnt = 0, start_years = 2000, end_years = 2010):

        result_nodes = {}
        #run_text = "Match (Gene00001: "+target_label_type+" {ID: \""+target_id+ "\" })-[s]-(Gene_web)-[r]-(n)\n"+"where toInteger(split(Gene_web.count, \";\")[-1]) > 521817\n"+"return ID(Gene_web)"

        #MATCH (General_Node00001: Gene {ID: "GeneID:7157"})-[s] - (General_Node_web)
        #WHERE exists(s.cnt_2009) or exists(s.cnt_2008) or exists(s.cnt_2007) or exists(s.cnt_2006) or exists(s.cnt_2005) or exists(s.cnt_2004) or exists(s.cnt_2003) or exists(s.cnt_2002) or exists(s.cnt_2001) or exists(s.cnt_2000)
        #WITH s, coalesce(s.cnt_2009,0) + coalesce(s.cnt_2008, 0) +  coalesce(s.cnt_2007, 0) +  coalesce(s.cnt_2006, 0) +  coalesce(s.cnt_2005, 0) +  coalesce(s.cnt_2004, 0) +  coalesce(s.cnt_2003, 0) +  coalesce(s.cnt_2002, 0) +  coalesce(s.cnt_2001, 0) +  coalesce(s.cnt_2000, 0) as cnt
        #order by cnt desc
        #return s,cnt
        #limit 10

        cnt_text = ""
        coalesce_text = ""
        cnt_property_text = ""
        run_text = ""
        run_text = run_text + "MATCH (General_Node00001: " + target_label_type + " {ID: \"" + target_id + "\"})-[s] - (General_Node_web)\n"
        cnt_text = "WHERE "
        coalesce_text = "WITH General_Node00001, General_Node_web, s, "
        for i in range(start_years, end_years) :
            cnt_property_text = "cnt_" + str(i)
            cnt_text = cnt_text + "exists(s."+cnt_property_text+") or "
            coalesce_text = coalesce_text + "coalesce(s."+cnt_property_text+", 0) +"
        cnt_text = cnt_text[:-3]
        coalesce_text = coalesce_text[:-2] + " as cnt"
        run_text = run_text + cnt_text + '\n'
        run_text = run_text + coalesce_text + '\n'
        run_text = run_text + "Order by cnt desc \n"
        run_text = run_text + "return s, cnt, General_Node00001, General_Node_web \n"
        run_text = run_text + "limit 100"
        #print(run_text)
        nodes = []
        links_temp = []
        for edge in tx.run(run_text):
            edges = edge[0]
            total_edge_cnt = edge[1]
            start_node = edge[2]
            end_node = edge[3]

            links_temp.append({"source": str(edges.start_node.id), "target": str(edges.end_node.id),
                               "cnt": total_edge_cnt, "group": 1})
            nodes.append({"nid":str(start_node.id),"cd":start_node._properties['ID'],"nm": start_node._properties['text'],"group":self.lable_web_dictionary[start_node._properties['type']]})
            nodes.append({"nid": str(end_node.id), "cd": end_node._properties['ID'],
                          "nm": end_node._properties['text'],
                          "group": self.lable_web_dictionary[end_node._properties['type']]})
        # print(links)
        links = []

        General_Node00001 = start_node
        #for starting point of open query

        sorted_links = sorted(links_temp, key=lambda k: k['cnt'], reverse=True)

        sorted_nodes = []
        for i in range(0, 20):
            links.append({'source' : sorted_links[i]['source'],'target' : sorted_links[i]['target'], 'cnt': sorted_links[i]['cnt'], 'group' : sorted_links[i]['group']})
            sorted_nodes.append(sorted_links[i]['source'])
            sorted_nodes.append(sorted_links[i]['target'])

        settype_nodes = set()
        ex_nodes = []
        for d in sorted_nodes:
            t = tuple([d])
            if t not in settype_nodes:
                settype_nodes.add(t)
                ex_nodes.append(d)

        final_nodes = []
        for i in ex_nodes:

            for j in nodes:
                if (j['nid'] == i):
                    final_nodes.append(j)
                    break



        first_layer_len = len(final_nodes)
        arcradius = 100
        circleradius = 10
        n = first_layer_len
        m = [20, 140, 20, 100]
        w = 948 - m[1] - m[3]
        h = 600 - m[0] - m[2]
        center_x = w / 2 + m[1]
        center_y = h / 2 + m[0]

        for i in range(0,first_layer_len):
            if(final_nodes[i]['cd'] == target_id):
                final_nodes[i]['fix_x'] = center_x
                final_nodes[i]['fix_y'] = center_y
            else:
                ang = (math.pi * 2 * i) / (first_layer_len-1)
                circle_x = arcradius * math.sin(ang) + center_x
                circle_y = arcradius * math.cos(ang) + center_y
                final_nodes[i]['fix_x'] = circle_x
                final_nodes[i]['fix_y'] = circle_y


        self.data['nodes'] = final_nodes
        self.data['links'] = links

        #MATCH (SSS)
        #Where ID(SSS) = 12359409
        #With SSS
        #Match (a)
        #Where ID(a) = 12359409 Or ID(a) = 132876 Or ID(a) = 144511 Or ID(a) = 142261 Or ID(a) = 126034 Or ID(a) = 144942 Or ID(a) = 125798 Or ID(a) = 144570 Or ID(a) = 131423 Or ID(a) = 143620 Or ID(a) = 136735 Or ID(a) = 143082 Or ID(a) = 125821 Or ID(a) = 205145 Or ID(a) = 129790 Or ID(a) = 79141798 Or ID(a) = 79133404 Or ID(a) = 79133405 Or ID(a) = 126000 Or ID(a) = 133595 Or ID(a) = 145655 With SSS, a
        #Match (a)-[r]-(b)
        #Where not (SSS)--(b)
        #return ID(b),count(*)
        #order by count(*) Desc
        #limit 100



        run_text = ""
        run_text = run_text + "MATCH (SSS)"+"\n"
        run_text = run_text + "Where ID(SSS) = " + str(General_Node00001.id) + "\n"
        run_text = run_text + "With SSS\n"
        run_text = run_text + "Match (a)\n"
        nodes_text = "Where "

        first_layer_node_list = []
        for i in final_nodes:
            nodes_text = nodes_text + "ID(a) = " + str(i["nid"]) + " Or "
            first_layer_node_list.append(i["nid"])
        nodes_text = nodes_text[:-3]
        run_text = run_text + nodes_text
        run_text = run_text + "With SSS, a\n"
        run_text = run_text + "Match (a)-[r]-(b)\n"
        run_text = run_text + "Where not (SSS)--(b)\n"
        run_text = run_text + "with a,r,b\n"
        run_text = run_text + "return ID(b),count(*)\n"
        run_text = run_text + "order by count(*) Desc\n"
        run_text = run_text + "limit 10\n"


        #print("number of second layers : ")


        #-----------------------------------------------------------------------------------------------------------
        #second layer part
        # print(links)
        temp_links = []
        first_second_edges = []
        second_layer_nodes = []
        second_layer_cnt = 0
        for record in tx.run(run_text):
            second_layer_nodes.append(record[0])
            second_layer_cnt = record[1]


        run_text = ""
        run_text = run_text + "MATCH (SSS)" + "\n"
        run_text = run_text + "Where ID(SSS) = " + str(General_Node00001.id) + "\n"
        run_text = run_text + "With SSS\n"
        run_text = run_text + "Match (a)\n"
        nodes_text = "Where "
        first_layer_node_list = []
        for i in final_nodes:
            nodes_text = nodes_text + "ID(a) = " + str(i["nid"]) + " Or "
            first_layer_node_list.append(i["nid"])
        nodes_text = nodes_text[:-3]
        run_text = run_text + nodes_text
        run_text = run_text + "With SSS, a\n"
        run_text = run_text + "Match (b)\n"
        nodes_text = "Where "
        first_layer_node_list = []
        for i in second_layer_nodes:
            nodes_text = nodes_text + "ID(b) = " + str(i) + " Or "
        nodes_text = nodes_text[:-3]
        run_text = run_text + nodes_text +"\n"
        run_text = run_text + "With a, b\n"
        run_text = run_text + "Match (a)-[r]-(b)\n"
        cnt_text = "WHERE "
        coalesce_text = "WITH a, r, b, "
        for i in range(start_years, end_years) :
            cnt_property_text = "cnt_" + str(i)
            cnt_text = cnt_text + "exists(r." + cnt_property_text + ") or "
            coalesce_text = coalesce_text + "coalesce(r." + cnt_property_text + ", 0) +"
        cnt_text = cnt_text[:-3]
        coalesce_text = coalesce_text[:-2] + " as cnt"
        run_text = run_text + cnt_text + '\n'
        run_text = run_text + coalesce_text + '\n'
        run_text = run_text + "Order by cnt desc \n"
        run_text = run_text + "return r, b, cnt \n"
        run_text = run_text + "limit 100"

        links_temp = []



        for edge in tx.run(run_text):
            edges = edge[0]
            end_node = edge[1]
            total_edge_cnt = edge[2]
            #a.data['links'].append({"source": str(edges.start_node.id), "target": str(edges.end_node.id), "cnt": total_edge_cnt, "group": 1})
            self.data['links'].append(
                {"source": str(edges.start_node.id), "target": str(edges.end_node.id),'cnt': total_edge_cnt , "group": 2})
            self.data['nodes'].append(
                {"nid": str(end_node.id), "cd": end_node._properties['ID'], "nm": end_node._properties['text'],
                 "group": self.lable_web_dictionary[end_node._properties['type']]})
        nodes = []
        nodes = self.data['nodes']
        settype_nodes = set()
        ex_nodes = []
        for d in nodes:
            t = tuple([d["nid"]])
            if t not in settype_nodes:
                settype_nodes.add(t)
                ex_nodes.append(d)
        #
        self.data['nodes'].clear()

        second_layer_len = len(ex_nodes)-first_layer_len

        circleradius = 10

        ang_cnt = 0
        for i in ex_nodes:
            if('fix_x' in i and 'fix_y' in i):
                self.data['nodes'].append(i)
                continue
            ang_cnt = ang_cnt + 1
            ang = (math.pi * 2 * ang_cnt) / second_layer_len
            circle_x = (arcradius + 100) * math.sin(ang) + center_x
            circle_y = (arcradius + 100) * math.cos(ang) + center_y
            i['fix_x'] = circle_x
            i['fix_y'] = circle_y
            self.data['nodes'].append(i)


        return result_nodes

    def check_relationships(self, node1_name: str = "abc", node2_name: str = "abc", relationship_type: str = "Null01234"):
        node1_id = 0
        node2_id = 0
        try:
            node1_id = self.node_id(node1_name)
        except:
            print(node1_name + " key error !")
            return
        try:
            node2_id = self.node_id(node2_name)
        except:
            print(node2_name + " key error !")
            return
        with driver.session() as session:
            return session.read_transaction(self.tx_check_relationship, node1_id, node2_id)
    def check_relationships_by_id(self, node1_id: int = 0, node2_id: int = 0, relationship_type: str = "knows"):
        with driver.session() as session:
            return session.read_transaction(self.tx_check_relationship, node1_id, node2_id, relationship_type)

    @staticmethod
    def tx_check_relationship(tx, id1, id2, relationship_type="Null01234"):
        if(relationship_type == "Null01234"): temp0002 = "MATCH (a)-[r]-(b)\n" + "WHERE ID(a) = "+str(id1)+" AND ID(b) = " + str(id2)+ "\n" + "RETURN id(r)\n"
        else : temp0002 = "MATCH (a)-[r:"+str(relationship_type)+"]-(b)\n" + "WHERE ID(a) = "+str(id1)+" AND ID(b) = " + str(id2)+ "\n" + "RETURN id(r)\n"
        try:
            return tx.run(temp0002).single().value()
        except AttributeError:
            return -1
        else :
            print("예상치 못한 에러 발생_Relationship_Check")
            return -2

    def check_relationships_by_id_with_properties(self, node1_id: int = 0, node2_id: int = 0, relationship_type: str = "knows"):
        with driver.session() as session:
            return session.read_transaction(self.tx_check_relationship_with_properties, node1_id, node2_id, relationship_type)

    def tx_check_relationship_with_properties(self, tx, id1, id2, relationship_type="Null01234"):
        if(relationship_type == "Null01234"): temp0002 = "MATCH (a)-[r]-(b)\n" + "WHERE ID(a) = "+str(id1)+" AND ID(b) = " + str(id2)+ "\n" + "RETURN r\n"
        else : temp0002 = "MATCH (a)-[r:"+str(relationship_type)+"]-(b)\n" + "WHERE ID(a) = "+str(id1)+" AND ID(b) = " + str(id2)+ "\n" + "RETURN r\n"
        try:
            temp = tx.run(temp0002)
            if(temp.session == None) : return -1
            else: return temp
        except AttributeError:
            return -1
        else :
            print("예상치 못한 에러 발생_Relationship_Check")
            return -2

    def update_relationships_cnt_by_id(self, node1_id: int = 0, node2_id = 0, relationship_id: int = 0):
        with driver.session() as session:
            session.read_transaction(self.tx_update_relationship_cnt, node1_id, node2_id, relationship_id)

    @staticmethod
    def tx_update_relationship_cnt(tx,node1_id=0,node2_id=0, Rel_id1=0):
        temp0002 = "MATCH (a)-[r]-(b)\n" + "WHERE id(a) = "+str(node1_id)+" AND id(b) = "+str(node2_id)+" and id(r) = {Rel_ID1}\n" + "SET r.cnt=r.cnt+1\n"
        try:
            tx.run(temp0002, Rel_ID1=Rel_id1)
            return
        except:
            print("예상치 못한 에러 발생_Relationship_Check")
        else :
            print("예상치 못한 에러 발생_Relationship_Check")

    def update_relationships_cnt_by_id_with_year(self, node1_id: int = 0, node2_id = 0, relationship_id: int = 0, relationship_type="Null01234", year = 0, temp_year_cnt = 1):
        with driver.session() as session:
            session.read_transaction(self.tx_update_relationship_cnt_with_year, node1_id, node2_id, relationship_id, relationship_type, year, temp_year_cnt)


    @staticmethod
    def tx_update_relationship_cnt_with_year(tx,node1_id=0,node2_id=0, Rel_id1=0, relationship_type="Null01234", year = 0, temp_year_cnt = 1):
        # Match(n) - [r] - (m)
        # where
        # id(n) = 132426 and Id(m) = 144989 and id(r) = 551305
        # MERGE(n) - [rel: cnt_merged_cooccurnce_test]->(m)
        #   ON MATCH SET
        # rel += {cnt_2000: 1111, cnt_2002: 0}
        temp0002 = "MATCH (a)-[r:"+relationship_type+"]-(b)\n"
        temp0002 = temp0002 + "WHERE id(a) = "+str(node1_id)+" AND id(b) = "+str(node2_id)+" and id(r) = "+ str(Rel_id1) + "\n"
        temp0002 = temp0002 + "MERGE (a)-[rel:"+relationship_type+"]->(b)\n"
        temp0002 = temp0002 + "  ON MATCH SET rel += {"+"cnt_"+str(year)+":"+str(temp_year_cnt)+"}\n"
        try:
            tx.run(temp0002)
            return
        except:
            print("예상치 못한 에러 발생_Relationship_Check")
        else :
            print("예상치 못한 에러 발생_Relationship_Check")


    #node1_id, node2_id, relationship_type, **properties
    def merge_relationships_cnt_by_id_with_year(self, node1_id: int = 0, node2_id=0, relationship_type: str = "cooccurnce", properties : dict = {}):
        with driver.session() as session:
            session.read_transaction(self.tx_merge_relationships_cnt_by_id_with_year, node1_id, node2_id, relationship_type,
                                     properties)
    def tx_merge_relationships_cnt_by_id_with_year(self, tx, node1_id: int = 0, node2_id=0, relationship_type: str = "cooccurnce", properties : dict = {}):

        temp3 = self.check_relationships_by_id_with_properties(node1_id,node2_id,"Disease_Tree")

        if (temp3 == -1 and temp3 == -2):
            #create edge
            temp0002 = "MATCH (a)-[r:" + relationship_type + "]-(b)\n"
        else:
            #empty relationship

            # copy cnt
            # for j in temp3._properties:
            #     i._properties += j

            temp0002 = "MATCH (a)-[r:" + relationship_type + "]-(b)\n"
            temp0002 = temp0002 + "WHERE id(a) = " + str(node1_id) + " AND id(b) = " + str(
                node2_id) + " and id(r) = " + str(Rel_id1) + "\n"
            temp0002 = temp0002 + "MERGE (a)-[rel:" + relationship_type + "]->(b)\n"
            temp0002 = temp0002 + "  ON MATCH SET rel += {" + "cnt_" + str(year) + ":" + str(temp_year_cnt) + "}\n"
        try:
            tx.run(temp0002)
            return
        except:
            print("예상치 못한 에러 발생_Relationship_Check")
        else:
            print("예상치 못한 에러 발생_Relationship_Check")

    def close_discovery(self, start_target_label_type="Gene", start_target_id="PR:000003035", end_target_label_type="Gene", end_target_id="PR:000003035"):

        #just formatting for close discovery

        search_start_temp = self.node_id(start_target_id)
        search_end_temp = self.node_id(end_target_id)
        cnt = 0
        result = {}
        with driver.session() as session:
            result = session.write_transaction(self.close_discovery_tx, start_target_label_type, start_target_id, end_target_label_type, end_target_id)

        print("\n")
        print("MATCH (n)")
        print("WHERE id(n) IN [",end='')
        for i in result:
            print(str(i), end=',')
            cnt += 1
            if (cnt == 15):
                print("\n")
                cnt = 0
            # for i,j in enumerate(result2):
            #     print(str(i), end=',')
        print(str(search_start_temp)+","+str(search_end_temp)+"]")
        print("Return n")
        return result

    def close_discovery_tx(self, tx, start_target_label_type="Gene", start_target_id="PR:000003035", end_target_label_type="Gene", end_target_id="PR:000003035",):
        result_nodes = {}
        #with size((c)--()) as N, ID(c) as M
        #return M,N ORDER BY N DESC LIMIT 10

        # run_text = run_text + "MATCH (General_Node00001: " + target_label_type + " {ID: \"" + target_id + "\"})-[s] - (General_Node_web)\n"
        # run_text = run_text + "with distinct General_Node00001, General_Node_web\n"
        # run_text = run_text + "Order by toInteger(split(c.count, \";\")[-1]) desc limit 10 \n"
        run_text = ""
        run_text = run_text + "Match (General00001:" + start_target_label_type + " {ID: \"" + start_target_id + "\" })--(c)--(General00002:" + end_target_label_type + " {ID: \"" + end_target_id + "\" })\n"
        run_text = run_text + "with distinct c\n"
        run_text = run_text + "Order by toInteger(split(c.count, \";\")[-1]) desc limit 10 \n"
        run_text = run_text + "return id(c)"
        print(run_text)
        for record in tx.run(run_text):
            result_nodes[record[0]] = 1
        return result_nodes.keys()

    def close_discovery_with_year(self, start_target_label_type="Gene", start_target_id="PR:000003035",
                        end_target_label_type="Gene", end_target_id="PR:000003035", start_years = 1990, end_years = 2000):

        # just formatting for close discovery

        search_start_temp = self.node_id_with_lable(start_target_id, start_target_label_type)
        search_end_temp = self.node_id_with_lable(end_target_id, end_target_label_type)
        cnt = 0
        result = {}
        with driver.session() as session:
            result = session.write_transaction(self.close_discovery_tx_with_year, start_target_label_type, start_target_id,
                                               end_target_label_type, end_target_id, start_years, end_years)

        for i in self.data['nodes']:
            if(i["cd"] == start_target_id):
                i["group"] = 1 # Query : 1
            if (i["cd"] == end_target_id):
                i["group"] = 1  # Query : 1
            # if ("fix_x" not in i and "fix_y" not in i):
            #     i["fix_x"] = self.center_x
            #     i["fix_y"] = self.center_y

        for i in self.data['links']:
            if (i["source"] == str(search_start_temp)): i["group"] = 1 # Direct_connection : 1
            if (i["source"] == str(search_end_temp)): i["group"] = 1  # Direct_connection : 1
            if (i["target"] == str(search_start_temp)): i["group"] = 1  # Direct_connection : 1
            if (i["target"] == str(search_end_temp)): i["group"] = 1  # Direct_connection : 1
        #print("\n")
        #print("MATCH (n)")
        #print("WHERE id(n) IN [", end='')
        for i in result:
            #print(str(i), end=',')
            cnt += 1
            if (cnt == 15):
                #print("\n")
                cnt = 0
            # for i,j in enumerate(result2):
            #     print(str(i), end=',')
        #print(str(search_start_temp) + "," + str(search_end_temp) + "]")
        #print("Return n")
        return result


    def close_discovery_tx_with_year(self, tx, start_target_label_type="Gene", start_target_id="PR:000003035", end_target_label_type="Gene", end_target_id="PR:000003035", start_years = 1990, end_years = 2000):


        result_nodes = {}

        nodes = []
        # lable_web_dictionary = {"Chemical": 2, "Disease": 3, "Mutation": 4, "Gene": 5, "Species": 6, "CellLine": 7,
        #                     "Hallmark": 8}

        # with size((c)--()) as N, ID(c) as M
        # return M,N ORDER BY N DESC LIMIT 10



        run_text = ""
        run_text = "MATCH (A:" + start_target_label_type + " {ID:\"" + start_target_id + "\"})\nRETURN A"
        try:
            for record in tx.run(run_text):
                for node in record:
                    nodes.append({"nid": str(node.id), "cd": node._properties['ID'], "nm": node._properties['text'],
                                  "group": self.lable_web_dictionary[node._properties['type']],"fix_x" : self.m[1], "fix_y" : self.center_y})
                    break
        except:
            print("node id not found : " +start_target_id)
            return -1


        #web layout examples
                # final_nodes[i]['x'] = center_x
                # final_nodes[i]['y'] = center_y


        run_text = ""
        run_text = "MATCH (A:" + end_target_label_type + " {ID:\"" + end_target_id + "\"})\nRETURN A"
        try:
            for record in tx.run(run_text):
                for node in record:
                    nodes.append({"nid": str(node.id), "cd": node._properties['ID'], "nm": node._properties['text'],
                                  "group": self.lable_web_dictionary[node._properties['type']],"fix_x" : self.w+self.m[3], "fix_y" : self.center_y})
                    break
        except:
            print("node id not found : " + end_target_id)
            return -1


        run_text = ""
        run_text = run_text + "Match p = (General00001:" + start_target_label_type + " {ID: \"" + start_target_id + "\" })--(c)--(General00002:" + end_target_label_type + " {ID: \"" + end_target_id + "\" })\n"
        run_text = run_text + "RETURN c"
        #print(run_text)
        # run_text = run_text + "Match (General00001:" + start_target_label_type + " {ID: \"" + start_target_id + "\" })--(c)--(General00002:" + end_target_label_type + " {ID: \"" + end_target_id + "\" })\n"
        # run_text = run_text + "with distinct c\n"
        # run_text = run_text + "WHERE ALL (r IN relationships(p) WHERE exists(r.cnt_1999) or exists(r.cnt_1998) or exists(r.cnt_1997) or exists(r.cnt_1996) or exists(r.cnt_1995) or exists(r.cnt_1994) or exists(r.cnt_1993) or exists(r.cnt_1992) or exists(r.cnt_1991) or exists(r.cnt_1990))" + "\n"
        # run_text = run_text + "UNWIND relationships(p) as results" + "\n"
        # run_text = run_text + "return id(results), id(startNode(results)),id(endNode(results)), results.cnt_1999, results.cnt_1998, results.cnt_1997, results.cnt_1996, results.cnt_1995, results.cnt_1994, results.cnt_1993, results.cnt_1992, results.cnt_1991, results.cnt_1990" + "\n"
        # run_text = run_text + "LIMIT 1000"


        for record in tx.run(run_text):
            for node in record:
                nodes.append({"nid":str(node.id),"cd":node._properties['ID'],"nm":node._properties['text'],"group":self.lable_web_dictionary[node._properties['type']]})
                #print(node)
        settype_nodes = set()
        ex_nodes = []
        for d in nodes:
            t = tuple(d.items())
            if t not in settype_nodes:
                settype_nodes.add(t)
                ex_nodes.append(d)
        #print(ex_nodes)

        #print(a.data['nodes'])
        output_list = []
        links = []
        #],\"links\":[{\"source\":\"ds39\",\"target\":\"ge518\"},{\"source\":\"ds39\",\"target\":\"ge559\"}
        #match (n)-[r]-(m)
        #return id(startNode(r)),id(endNode(r))
        #limit 10

        run_text = ""
        run_text = run_text + "Match (General00001:" + start_target_label_type + " {ID: \"" + start_target_id + "\" })-[r1]-(c)-[r2]-(General00002:" + end_target_label_type + " {ID: \"" + end_target_id + "\" })\n"
        run_text = run_text + "RETURN r1,r2"
        links_temp = []
        for record in tx.run(run_text):
            total_edge_cnt = 0
            for edges in record:
                for i in range(start_years,end_years):
                    cnt_property_text = "cnt_"+str(i)
                    try :
                        total_edge_cnt += edges._properties[cnt_property_text]
                    except:
                        continue
            for edges in record:
                links_temp.append({"source":str(edges.start_node.id),"target":str(edges.end_node.id), "cnt":total_edge_cnt, "group" : 1})
                output_list.append(edges)

        #print(links)
        links.clear()
        sorted_links = sorted(links_temp, key=lambda k:k['cnt'], reverse=True)


        sorted_nodes = []
        for i in range(0,50):
            links.append(sorted_links[i])
            sorted_nodes.append(sorted_links[i]['source'])
            sorted_nodes.append(sorted_links[i]['target'])

        settype_nodes = set()
        ex_nodes = []
        for d in sorted_nodes:
            t = tuple([d])
            if t not in settype_nodes:
                settype_nodes.add(t)
                ex_nodes.append(d)


        final_nodes = []
        for i in ex_nodes:
            for j in nodes:
                if(j['nid'] == i) :
                    final_nodes.append(j)
                    break

        run_text = ""
        run_text = run_text + "Match (FinalNodes) \n"
        nodes_text = "Where "
        for i in final_nodes:
            nodes_text = nodes_text + "ID(FinalNodes) = " + str(i["nid"]) + " Or "
        nodes_text = nodes_text[:-3]
        run_text = run_text + nodes_text +"\n"
        run_text = run_text + "WITH collect(FinalNodes) as nodes" + "\n"
        run_text = run_text + "UNWIND nodes as n" + "\n"
        run_text = run_text + "UNWIND nodes as m" + "\n"
        run_text = run_text + "Match (n)-[r1]-(m)\n"
        run_text = run_text + "RETURN r1"
        links_temp = []

        for record in tx.run(run_text):
            for edges in record:
                total_edge_cnt = 0
                for i in range(start_years, end_years):
                    cnt_property_text = "cnt_"+str(i)
                    try :
                        total_edge_cnt += edges._properties[cnt_property_text]
                    except:
                        continue
                if(total_edge_cnt == 0): continue

                links_temp.append({"source": str(edges.start_node.id), "target": str(edges.end_node.id),
                                   "cnt": total_edge_cnt, "group": 3})
                links.append({"source": str(edges.start_node.id), "target": str(edges.end_node.id),
                                   "cnt": total_edge_cnt, "group": 3})

        self.data['nodes'] = final_nodes


        self.data['links'] = links
        #print(a.data['links'])

        return output_list

    def shortestpath_discovery_with_years(self, start_target_label_type="Disease", start_target_id="MESH:D018784", years = 1990):
        # just formatting for close discovery

        search_start_temp = self.node_id_with_lable(start_target_id,start_target_label_type)
        cnt = 0
        result = {}
        with driver.session() as session:
            result = session.write_transaction(self.shortestpath_discovery_with_years_tx, start_target_label_type= start_target_label_type, start_target_id=search_start_temp, years = years)

        for i in self.data['nodes']:
            if(i["cd"] == start_target_id):
                i["group"] = 1 # Query : 1
        #print("\n")
        #print("MATCH (n)")
        #print("WHERE id(n) IN [", end='')
        for i in result:
            #print(str(i), end=',')
            cnt += 1
            if (cnt == 15):
                #print("\n")
                cnt = 0
            # for i,j in enumerate(result2):
            #     print(str(i), end=',')
        #print(str(search_start_temp) + "]")
        #print("Return n")
        return result


    def shortestpath_discovery_with_years_tx(self, tx, start_target_label_type="Disease", start_target_id="124302", years=1990):
        #년도 별로 적용해야 될 필요성 있
        result_nodes = {}

        #MATCH(s: Disease)
        #where ID(s) = 124302
        #WITH s
        # MATCH
        # p = shortestpath((Disease00001:Disease {ID:"MESH:D018784"}) - [*0..3] - (disease_web:Disease))
        # WHERE ALL(r IN relationships(p) WHERE exists(r.cnt_1999) or exists(r.cnt_1998))
        # UNWIND relationships(p) as results
        # return id(results), results.cnt_1999, results.cnt_1998
        # LIMIT
        # 100

        run_text = ""
        run_text = run_text + "MATCH (s:"+start_target_label_type+")" + "\n"
        run_text = run_text + "WHERE ID(s) = " + str(start_target_id) + "\n"
        run_text = run_text + "WITH s" + "\n"
        run_text = run_text + "MATCH p = shortestpath((s) - [*0..3] - (General_web:" + start_target_label_type +"))"+"\n"
        run_text = run_text + "WHERE ALL (r IN relationships(p) WHERE exists(r.cnt_1999) or exists(r.cnt_1998) or exists(r.cnt_1997) or exists(r.cnt_1996) or exists(r.cnt_1995) or exists(r.cnt_1994) or exists(r.cnt_1993) or exists(r.cnt_1992) or exists(r.cnt_1991) or exists(r.cnt_1990))"+"\n"
        run_text = run_text + "UNWIND relationships(p) as results"+"\n"
        run_text = run_text + "return id(results), id(startNode(results)),id(endNode(results)), results.cnt_1999, results.cnt_1998, results.cnt_1997, results.cnt_1996, results.cnt_1995, results.cnt_1994, results.cnt_1993, results.cnt_1992, results.cnt_1991, results.cnt_1990"+"\n"
        run_text = run_text + "LIMIT 1000"

        #print(run_text)
        result_list = []
        property_dic = {}
        sorted_cnt = []
        for record in tx.run(run_text):
            sum_value = 0
            for j,value in enumerate(record):
                if(j == 0 and j == 1 and j == 2) : continue
                elif (value == None): continue
                else : sum_value = sum_value + int(value)
            result_list.append([record[0],record[1],record[2],sum_value])
            #result_list.append(sum_value)
        sorted_cnt = sorted(result_list, key=operator.itemgetter(3), reverse=True)

        run_text = ""
        run_text = run_text + "MATCH (a)-[r]-(b)\n"
        run_text = run_text + "WHERE ID(r) IN[\n"
        # {"nodes": [{"nid":"ds39","cd":"H00031","nm":"Breast cancer","group":1}]
        len_sorted_cnt = len(sorted_cnt)
        for j in range(100):
            if(j == len_sorted_cnt): break
            run_text = run_text + str(sorted_cnt[j][0]) + ","
        run_text = run_text.rstrip(",")
        run_text = run_text + "]\nwith a,b as c \nRETURN c"

        nodes = []
        # lable_web_dictionary = {"Chemical": 2, "Disease": 3, "Mutation": 4, "Gene": 5, "Species": 6, "CellLine": 7,
        #                     "Hallmark": 8}
        for record in tx.run(run_text):
            for node in record:
                nodes.append({"nid":str(node.id),"cd":node._properties['ID'],"nm":node._properties['text'],"group":self.lable_web_dictionary[node._properties['type']]})
                #print(node)
        settype_nodes = set()
        ex_nodes = []
        for d in nodes:
            t = tuple(d.items())
            if t not in settype_nodes:
                settype_nodes.add(t)
                ex_nodes.append(d)
        #print(ex_nodes)
        self.data['nodes'] = ex_nodes
        #print(a.data['nodes'])
        output_list = []
        links = []
        #],\"links\":[{\"source\":\"ds39\",\"target\":\"ge518\"},{\"source\":\"ds39\",\"target\":\"ge559\"}
        #match (n)-[r]-(m)
        #return id(startNode(r)),id(endNode(r))
        #limit 10
        node_seach_check = False
        for j in range(len(sorted_cnt)):
            node_seach_check = False
            for k in ex_nodes:
                if k["nid"] == str(sorted_cnt[j][1]) :
                    node_seach_check = True
                    break
            if(node_seach_check == False) : continue
            node_seach_check = False
            for k in ex_nodes:
                if k["nid"] == str(sorted_cnt[j][2]) :
                    node_seach_check = True
                    break
            if (node_seach_check == False): continue
            links.append({"source":str(sorted_cnt[j][1]),"target":str(sorted_cnt[j][2]), "group" : 1})
            output_list.append(sorted_cnt[j])

        #print(links)

        self.data['links'] = links
        #print(a.data['links'])
        return output_list


    def neighbor_discovery_with_years(self, start_target_label_type="Disease", start_target_id="MESH:D018784", start_years = 1990, end_years = 2000):
        # just formatting for close discovery

        search_start_temp = self.node_id_with_lable(start_target_id,start_target_label_type)
        if(search_start_temp == -1):
            print(str(start_target_label_type) + " " + str(start_target_id) + " Search Failed!! [no starting node in our neo4j server]")
            return 0
        cnt = 0
        result = {}
        with driver.session() as session:
            result = session.write_transaction(self.neighbor_discovery_with_years_tx, start_target_label_type= start_target_label_type, start_target_id=search_start_temp, start_years = start_years, end_years = end_years)

        if(result == 0):
            return 0
        for i in self.data['nodes']:
            if(i["cd"] == start_target_id):
                i["group"] = 1 # Query : 1
        #print("\n")
        #print("MATCH (n)")
        #print("WHERE id(n) IN [", end='')
        #for i in result:
            #print(str(i), end=',')
         #   cnt += 1
          #  if (cnt == 15):
                #print("\n")
           #     cnt = 0
            # for i,j in enumerate(result2):
            #     print(str(i), end=',')
        #print(str(search_start_temp) + "]")
        #print("Return n")
        return result


    def neighbor_discovery_with_years_tx(self, tx, start_target_label_type="Disease", start_target_id="124302", start_years=1990, end_years=2000):

        result_nodes = {}

        #MATCH(s: Disease)
        #where ID(s) = 124302
        #WITH s
        # MATCH
        # p = shortestpath((Disease00001:Disease {ID:"MESH:D018784"}) - [*0..3] - (disease_web:Disease))
        # WHERE ALL(r IN relationships(p) WHERE exists(r.cnt_1999) or exists(r.cnt_1998))
        # UNWIND relationships(p) as results
        # return id(results), results.cnt_1999, results.cnt_1998
        # LIMIT
        # 100
        cnt_text = ""
        coalesce_text = ""
        cnt_property_text = ""
        run_text = ""
        run_text = run_text + "MATCH (General_Node00001:"+start_target_label_type+")" + "\n"
        run_text = run_text + "WHERE ID(General_Node00001) = " + str(start_target_id) + "\n"
        run_text = run_text + "WITH General_Node00001" + "\n"
        run_text = run_text + "MATCH p = (General_Node00001) - [s:cooccurnce] - (General_Node_web)"+"\n"
        cnt_text = "WHERE "
        coalesce_text = "WITH General_Node00001, General_Node_web, s, "
        for i in range(start_years, end_years):
            cnt_property_text = "cnt_" + str(i)
            cnt_text = cnt_text + "exists(s." + cnt_property_text + ") or "
            coalesce_text = coalesce_text + "coalesce(s." + cnt_property_text + ", 0) +"
        cnt_text = cnt_text[:-3]
        coalesce_text = coalesce_text[:-2] + " as cnt"
        run_text = run_text + cnt_text + '\n'
        run_text = run_text + coalesce_text + '\n'
        run_text = run_text + "Order by cnt desc \n"
        run_text = run_text + "return s, cnt, General_Node00001, General_Node_web \n"
        run_text = run_text + "limit 1000"

        nodes = []
        links_temp = []
        node_check = False
        for edge in tx.run(run_text):
            node_check = True
            edges = edge[0]
            total_edge_cnt = edge[1]
            start_node = edge[2]
            end_node = edge[3]

            links_temp.append({"source": str(edges.start_node.id), "target": str(edges.end_node.id),
                               "cnt": total_edge_cnt, "group": 1})
            try:
                nodes.append(
                    {"nid": str(start_node.id), "cd": start_node._properties['ID'], "nm": start_node._properties['text'],
                     "group": self.lable_web_dictionary[start_node._properties['type']]})

                nodes.append({"nid": str(end_node.id), "cd": end_node._properties['ID'],
                          "nm": end_node._properties['text'],
                          "group": self.lable_web_dictionary[end_node._properties['type']]})
            except:
                print("except")

        links = []
        if(node_check == False):
            print(str(start_target_label_type) + " "+ str(start_target_id)+" Search Failed!! [no connected edgein our neo4j server]")
            self.data['nodes'] = 0
            return 0
        General_Node00001 = start_node
        # for starting point of open query

        sorted_links = sorted(links_temp, key=lambda k: k['cnt'], reverse=True)

        sorted_nodes = []
        for i in range(0, 20):
            try:
                links.append({'source': sorted_links[i]['source'], 'target': sorted_links[i]['target'], 'cnt':sorted_links[i]['cnt'],
                              'group': sorted_links[i]['group']})
                sorted_nodes.append(sorted_links[i]['source'])
                sorted_nodes.append(sorted_links[i]['target'])
            except:
                break

        settype_nodes = set()
        ex_nodes = []
        for d in sorted_nodes:
            t = tuple([d])
            if t not in settype_nodes:
                settype_nodes.add(t)
                ex_nodes.append(d)

        final_nodes = []
        for i in ex_nodes:

            for j in nodes:
                if (j['nid'] == i):
                    final_nodes.append(j)
                    break

        self.data['nodes'] = final_nodes
        self.data['links'] = links

        run_text = ""
        run_text = run_text + "MATCH (SSS)" + "\n"
        run_text = run_text + "Where ID(SSS) = " + str(General_Node00001.id) + "\n"
        run_text = run_text + "With SSS\n"
        run_text = run_text + "Match (a)\n"
        nodes_text = "Where "

        first_layer_node_list = []
        for i in final_nodes:
            nodes_text = nodes_text + "ID(a) = " + str(i["nid"]) + " Or "
            first_layer_node_list.append(i["nid"])
        nodes_text = nodes_text[:-3]
        run_text = run_text + nodes_text
        run_text = run_text + "With SSS, a\n"

        run_text = run_text + "Match (b)\n"

        nodes_text = "Where "
        for i in final_nodes:
            nodes_text = nodes_text + "ID(b) = " + str(i["nid"]) + " Or "
        nodes_text = nodes_text[:-3]

        run_text = run_text + nodes_text
        run_text = run_text + "With SSS, a, b\n"
        run_text = run_text + "Match (a)-[r:cooccurnce]-(b)\n"
        cnt_text = "WHERE "
        coalesce_text = "WITH a, r, b, "
        for i in range(start_years, end_years):
            cnt_property_text = "cnt_" + str(i)
            cnt_text = cnt_text + "exists(r." + cnt_property_text + ") or "
            coalesce_text = coalesce_text + "coalesce(r." + cnt_property_text + ", 0) +"
        cnt_text = cnt_text[:-3]
        coalesce_text = coalesce_text[:-2] + " as cnt"
        run_text = run_text + cnt_text + '\n'
        run_text = run_text + coalesce_text + '\n'
        run_text = run_text + "Order by cnt desc \n"
        run_text = run_text + "return r, a, b, cnt \n"
        #run_text = run_text + "limit 1000"

        links_temp = []
        nodes = []
        for edge in tx.run(run_text):
            edges = edge[0]
            start_node = edge[1]
            end_node = edge[2]
            total_edge_cnt = edge[3]
            if(start_node.id == General_Node00001.id or end_node.id == General_Node00001.id) : continue
            # a.data['links'].append({"source": str(edges.start_node.id), "target": str(edges.end_node.id), "cnt": total_edge_cnt, "group": 1})
            self.data['links'].append(
                {"source": str(edges.start_node.id), "target": str(edges.end_node.id), "cnt":total_edge_cnt, "group": 4})

        return result_nodes
    def neighbor_nodes_query(self, start_target_label_type="Disease", start_target_id="MESH:D018784", relationtype="Disease_Tree"):
        # just formatting for close discovery

        # MESH:C
        # 7410146

        start_target_label_type = "Disease_hierarchy"
        search_start_temp = self.node_id_with_lable(start_target_id,start_target_label_type)
        cnt = 0
        result = {}
        with driver.session() as session:
            result = session.write_transaction(self.neighbor_nodes_query_tx, start_target_label_type= start_target_label_type, start_target_id=search_start_temp, relationtype=relationtype)


        return result


    def neighbor_nodes_query_tx(self, tx, start_target_label_type="Disease", start_target_id="124302", relationtype="Disease_Tree"):

        #MESH:C
        #7410146
        start_target_id = "7410146"

        result_nodes = {}

        run_text = ""
        run_text = run_text + "MATCH (General_Node00001:"+start_target_label_type+")" + "\n"
        run_text = run_text + "WHERE ID(General_Node00001) = " + str(start_target_id) + "\n"
        run_text = run_text + "WITH General_Node00001" + "\n"
        run_text = run_text + "MATCH (General_Node00001) - [s:" + str(relationtype) + "] - (General_Node_web)"+"\n"
        run_text = run_text + "Return General_Node_web"

        nodes = tx.run(run_text)

        return nodes

    def hierarchy_edge_update(self, start_target_label_type="Disease", start_target_id="MESH:D018784", relationtype="Disease_Tree"):
        # just formatting for close discovery

        # MESH:C
        # 7410146

        start_target_label_type = "Disease"
        search_start_temp = self.node_id_with_lable(start_target_id,start_target_label_type)
        cnt = 0
        result = {}
        with driver.session() as session:
            result = session.write_transaction(self.hierarchy_edge_update_tx, start_target_label_type= start_target_label_type, start_target_id=search_start_temp, relationtype=relationtype)


        return result


    def hierarchy_edge_update_tx(self, tx, start_target_label_type="Disease", start_target_id="124302", relationtype="Disease_Tree"):

        #MESH:C
        #7410146

        relationtype1 = "cooccurnce"

        run_text = ""
        run_text = run_text + "MATCH (General_Node00001:"+start_target_label_type+")" + "\n"
        run_text = run_text + "WHERE ID(General_Node00001) = " + str(start_target_id) + "\n"
        run_text = run_text + "WITH General_Node00001" + "\n"
        run_text = run_text + "MATCH (General_Node00001) - [s:" + str(relationtype1) + "] - (General_Node_web)"+"\n"
        run_text = run_text + "Return s"


        for i in tx.run(run_text):
            #relationship_type: str = "cooccurnce", ** properties
            #update relationship
            temp3 = self.check_relationships_by_id_with_properties(i[0].start, i[0].end, "Disease_Tree")
            self.merge_relationships_cnt_by_id_with_year(i[0].start,i[0].end,"cooccurnce",i[0]._properties)
        return 1


def csv_parser(temp_in):
    #for eliminationg , between double qutation
    temp_list = []
    temp_str = ""
    quote_cnt = 0
    for c in temp_in:
        if c == ',' and quote_cnt % 2 == 0:
            if(quote_cnt != 0 and temp_str[-1] != "\""):
                if c == "\"": quote_cnt += 1
                #if c == "\"" or c == "\'": quote_cnt += 1
                #5'-nucleotidase 때문에 안됨
                temp_str += c
                continue
            quote_cnt = 0
            temp_list.append(temp_str)
            temp_str = ""
        else:
            if c == "\"": quote_cnt += 1
            temp_str += c
    temp_list.append(temp_str)
    temp_str = ""
    return temp_list


def express_js(data= {'msg':"Hi!!!"}):
    #url = "http://localhost:3000"
    url = "http://192.168.0.82:3000"
    headers = {'Content-type':'application/json', 'Accept' : 'text/plain'}
    #r = requests.post(url, data = json.dumps(data), headers = headers)

    for i in data.keys():
        for j,a in enumerate(data[i]):
            for k in a.keys():
                if("\"" in str(data[i][j][k])):
                    #print(data[i][j][k])
                    data[i][j][k] = data[i][j][k].replace("\"","_")
    r1 = requests.post(url, data = json.dumps(data), headers = headers)

    print(json.dumps(data))
    #headers = {'Content-type':'applications/json', 'Accept' : 'text/plain'}
    #r = requests.post(url, data = json.dumps(data), headers = headers)


    return
def php_dump(data= {'msg':"Hi!!!"}):
    data['relationships'] = data['links']
    del data['links']
    # in neo4jd3 'links' change into 'relationships'  2020_05_08 mskim
    for i in data.keys():
        for j,a in enumerate(data[i]):
            for k in a.keys():
                # if(i == 'nodes' and k == 'id'):
                #     temp = data[i][j]['properties']['nm']
                #     data[i][j][k] = ""
                #     data[i][j][k] = temp
                if("\"" in str(data[i][j][k])):
                    #print(data[i][j][k])
                    data[i][j][k] = data[i][j][k].replace("\"","_")

    print(json.dumps(data))
    #headers = {'Content-type':'applications/json', 'Accept' : 'text/plain'}
    #r = requests.post(url, data = json.dumps(data), headers = headers)

if __name__ == '__main__':
    start_time = time.time()

    a = Nodes_Noe4j()
    #a.load_all_nodes()

    arg = '/var/www/cgi-bin/LionDB_Bolts_Class.py 1 BERN:4567303 Drug'.split(" ")


    a.conditional_start(arg)

    #edge_year_input("/3TB/test/191231/pmid_result_Gene_filtered_pro_191230.psv")

    #a.load_all_nodes()
    #a.close_discovery_with_year(start_target_label_type="Species", start_target_id="TAXID:9606", end_target_label_type="Disease", end_target_id="MESH:D006331")

    #print(a.open_discovery())

    #(target_label_type = "Gene", target_id = "PR:000003035")
    #express_js(a.data)


    #a.load_all_nodes()
    #a.close_discovery_with_year(start_target_label_type="Species", start_target_id="TAXID:9606", end_target_label_type="Disease", end_target_id="MESH:D006331")

    #print(a.open_discovery())


    #edge_input_domain_fix('./pro_ncbi_edge.csv')
    # edge_year_input("/3TB/test/191230/pmid_result_Gene_filtered_pro_191230.csv")
    #edge_year_input_node_loaded("./pmid_results_sorted_2020_cnt3.csv")

    #print("Query Working Time: {} sec".format(end_time - start_time))
    #a.close_discovery(start_target_label_type="Chemical", start_target_id="MESH:D016685", end_target_label_type="Cellline", end_target_id="CVCL_0023")


    #count_bioconcept()
    #node_input(sys.argv[1])
    #edge_input(sys.argv[1])

    #print(a.check_relationships("TAXID:24","CVCL_IJ15"))
    #a.create_relationship()
    #a.create_relationship("MESH:C528072", "MESH:C528070")
    #print(a.nodes)
    #output_csv(["CVCL_V362","CVCL_IP58"])
    driver.close()