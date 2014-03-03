from __future__ import print_function

import pymysql
import os   
import os.path   

cModule = 0
cUnit = 0
cSeries = 0
cTopic = 0

# 插入module topic
def persistModuleFromFile(file, subject_id, stage_id, conn):
    global cModule  
    cm = cModule
    f = open(file,"r",encoding="utf-16")
    preModule = ""
    line = f.readline()
    while line:
        tri = line.split("\t")
        if preModule != tri[0]:
            cm += 1
            print(tri[0]+file[file.rfind("/"):len(file)])
            cur.execute("INSERT INTO t_module VALUES ("+str(cm)+",'','"+tri[0]+"','"+stage_id+"','"+subject_id+"')")
        preModule = tri[0]
        # print(+":"+tri[1]+":"+tri[2])
        line = f.readline()
    f.close()
    cModule = cm



# 插入unit
def persistUnitFromFile(file, subject_id, stage_id, conn):
    global module
    global cUnit 
    cu = cUnit
    f = open(file,"r",encoding="utf-16")
    preUnit = ""
    line = f.readline()
    while line:
        tri = line.split("\t")
        if preUnit != tri[1]:
            cu += 1
            print(tri[1]+file[file.rfind("/"):len(file)])
            cur.execute("INSERT INTO t_unit VALUES ("+str(cu)+",'','"+str(module[str(tri[0])])+"','"+tri[1]+"','"+stage_id+"','"+subject_id+"')")
        preUnit = tri[1]
        # print(+":"+tri[1]+":"+tri[2])
        line = f.readline()
    f.close()
    cUnit = cu

# 插入series
def persistSeriesFromFile(file, subject_id, stage_id, conn):
    global module
    global cSeries 
    cs = cSeries
    f = open(file,"r",encoding="utf-16")
    preSeries = ""
    line = f.readline()
    print(f)
    while line:
        tri = line.split("\t")
        print(tri[0])
        print(tri[1])
        if preSeries != tri[1]:
            cs += 1
            print(tri[1]+file[file.rfind("/"):len(file)])
            cur.execute("INSERT INTO t_series VALUES ("+str(cs)+",'','','"+str(module[str(tri[0])])+"','"+tri[1]+"','"+stage_id+"','"+subject_id+"')")
        preSeries = tri[1]
        # print(+":"+tri[1]+":"+tri[2])
        line = f.readline()
    f.close()
    cSeries = cs

# 插入topic
def persistTopicFromFile(file, subject_id, stage_id, conn):
    global module
    global cTopic 
    ct = cTopic
    f = open(file,"r",encoding="utf-16")
    preTopic = ""
    line = f.readline()
    while line:
        tri = line.split("\t")
        if preTopic != tri[2]:
            ct += 1
            print(tri[2]+file[file.rfind("/"):len(file)])
            cur.execute("INSERT INTO t_topic VALUES ("+str(ct)+",'','','"+tri[2]+"',0,'"+stage_id+"','"+subject_id+"','"+str(unit[str(tri[1])])+"')")
        preTopic = tri[2]
        # print(+":"+tri[1]+":"+tri[2])
        line = f.readline()
    f.close()
    cTopic = ct



conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='noriental',charset='utf8')

cur = conn.cursor()

rootDir = "/Users/lianghongyun/Documents/work/2.27知识图谱汇总/plain"



subject = {}
subjectId = {}
stage = {}
stageId = {}
module = {}
moduleId = {}
unit = {}
unitId = {}

# 加载学段
cur.execute("SELECT t.id, t.name FROM t_stage t")
for row in cur:
   stage[row[1]] = row[0]
   stageId[row[0]] = row[1]
# 加载学科
cur.execute("SELECT t.id, t.name, t.stage_id FROM t_subject t")
for row in cur:
    subjectId[str(row[0])] = str(row[1])
    subject[str(row[1])] = row[0]

#清空module表
cur.execute("DELETE FROM t_module")

#从文件load module
for parent,dirnames,filenames in os.walk(rootDir):   
    for filename in filenames:
        persistModuleFromFile(rootDir+"/"+filename,subject[filename[2:4]+filename[0:2]],stage[filename[2:4]],conn)

# 从数据库加载module
cur.execute("SELECT t.id, t.name FROM t_module t")
for row in cur:
   module[row[1]] = row[0]
   moduleId[row[0]] = row[1]

#清空unit表
cur.execute("DELETE FROM t_unit")

# 从文件load unit
for parent,dirnames,filenames in os.walk(rootDir):   
    for filename in filenames:
        if filename[4:6] == "主题":
            persistUnitFromFile(rootDir+"/"+filename,subject[filename[2:4]+filename[0:2]],stage[filename[2:4]],conn)

#清空unit表
cur.execute("DELETE FROM t_series")

# 从文件load series
for parent,dirnames,filenames in os.walk(rootDir):   
    for filename in filenames:
        if filename[4:6] == "专题":
            persistSeriesFromFile(rootDir+"/"+filename,subject[filename[2:4]+filename[0:2]],stage[filename[2:4]],conn)

# 从数据库加载unit
cur.execute("SELECT t.id, t.name FROM t_unit t")
for row in cur:
   unit[row[1]] = row[0]
   unitId[row[0]] = row[1]

# 从文件load series
for parent,dirnames,filenames in os.walk(rootDir):   
    for filename in filenames:
        if filename[4:6] == "主题":
            persistTopicFromFile(rootDir+"/"+filename,subject[filename[2:4]+filename[0:2]],stage[filename[2:4]],conn)


conn.commit()


cur.close()
conn.close()



