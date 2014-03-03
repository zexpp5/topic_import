

import pymysql
import os   
import os.path   



conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='noriental',charset='utf8')
cur = conn.cursor()

cur.execute("DELETE FROM t_stage")
cur.execute("DELETE FROM t_subject")

stage = ["初中","高中"]
dStage = {1:"初中",2:"高中"}
subject = ["语文","数学","英语","物理","化学","生物","历史","地理","政治"]
cur.execute("INSERT INTO t_stage VALUES ("+str(1)+",'2014-03-03 18:44:54','"+stage[0]+"','2014-03-03 18:44:54')")
cur.execute("INSERT INTO t_stage VALUES ("+str(2)+",'2014-03-03 18:44:54','"+stage[1]+"','2014-03-03 18:44:54')")

j = 0
for i in range(len(subject)):
    j+=1
    cur.execute("INSERT INTO t_subject VALUES ("+str(j)+",'2014-03-03 18:44:54','"+dStage[1]+subject[i]+"',1,'2014-03-03 18:44:54')")
    j+=1
    cur.execute("INSERT INTO t_subject VALUES ("+str(j)+",'2014-03-03 18:44:54','"+dStage[2]+subject[i]+"',2,'2014-03-03 18:44:54')")

conn.commit()
print(cur.description)

print()


cur.close()
conn.close()



