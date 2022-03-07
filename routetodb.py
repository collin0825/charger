import numpy as np
from python_tsp.distances import great_circle_distance_matrix
from python_tsp.exact import solve_tsp_dynamic_programming
# 引用必要套件
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from itertools import combinations
# 引用私密金鑰
cred = credentials.Certificate('serviceAccount.json')
# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred)
# 初始化firestore
db = firestore.client()

idata = list(range(1, 21))
sdata = []
for i in range(len(idata)):
    sdata.append(str(idata[i]));
select = list(combinations(sdata,1))


for j in range(len(select)):
    count = [0]*1 #總點數
    id1 = select[j][0]
    # id2 = select[j][1]
    # id3 = select[j][2]
    # id4 = select[j][3]

    a = []
    docs1 = db.collection(u'chargers').document(u'頭前國中地下停車場').collection(u'neighbor').where(u'id', u'==', id1).stream()
    for doc1 in docs1:
        lat1 = doc1.to_dict()['vlat']
        lng1 = doc1.to_dict()['vlng']
        a.append(lat1)
        a.append(lng1)
    print(a)
    
    # b = []   
    # docs2 = db.collection(u'chargers').document(u'頭前國中地下停車場').collection(u'neighbor').where(u'id', u'==', id2).stream()
    # for doc2 in docs2:
    #     lat2 = doc2.to_dict()['vlat']
    #     lng2 = doc2.to_dict()['vlng']
    #     b.append(lat2)
    #     b.append(lng2)
    # print(b)
    
    # c = []   
    # docs3 = db.collection(u'chargers').document(u'頭前國中地下停車場').collection(u'neighbor').where(u'id', u'==', id3).stream()
    # for doc3 in docs3:
    #     lat3 = doc3.to_dict()['vlat']
    #     lng3 = doc3.to_dict()['vlng']
    #     c.append(lat3)
    #     c.append(lng3)
    # print(c)
    
    # d = [] 
    # docs4 = db.collection(u'chargers').document(u'頭前國中地下停車場').collection(u'neighbor').where(u'id', u'==', id4).stream()
    # for doc4 in docs4:
    #     lat4 = doc4.to_dict()['vlat']
    #     lng4 = doc4.to_dict()['vlng']
    #     d.append(lat4)
    #     d.append(lng4)
    # print(d)
    
    iid1 = int(id1)
    # iid2 = int(id2)
    # iid3 = int(id3)
    # iid4 = int(id4)
    sources = [[25.054864, 121.458042]]
    sources.append(a)
    # sources.append(b)
    # sources.append(c)
    # sources.append(d)
    count[0] = iid1;
    # count[1] = iid2;
    # count[2] = iid3;
    # count[3] = iid4;
    distance_matrix = great_circle_distance_matrix(sources)
    permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
    itid1 = count[permutation[1]-1]
    # itid2 = count[permutation[2]-1]
    # itid3 = count[permutation[3]-1]
    # itid4 = count[permutation[4]-1]
    tid1 = str(itid1)
    # tid2 = str(itid2)
    # tid3 = str(itid3)
    # tid4 = str(itid4)
    
    dots = []
    
    docst1 = db.collection(u'chargers').document(u'頭前國中地下停車場').collection(u'neighbor').where(u'id', u'==', tid1).stream()
    for doct1 in docst1:
        latt1 = doct1.to_dict()['vlat']
        lngt1 = doct1.to_dict()['vlng']
        namet1 = doct1.to_dict()['name']
        addresst1 = doct1.to_dict()['viewaddress']
        t1 = {'pointaddress': addresst1, 'pointname': namet1 , 'pointlat': latt1, 'pointlng': lngt1}
    dots.append(t1)
    
    # docst2 = db.collection(u'chargers').document(u'頭前國中地下停車場').collection(u'neighbor').where(u'id', u'==', tid2).stream()
    # for doct2 in docst2:
    #     latt2 = doct2.to_dict()['vlat']
    #     lngt2 = doct2.to_dict()['vlng']
    #     namet2 = doct2.to_dict()['name']
    #     addresst2 = doct2.to_dict()['viewaddress']
    #     t2 = {'pointaddress': addresst2, 'pointname': namet2 , 'pointlat': latt2, 'pointlng': lngt2}
    # dots.append(t2)
    
    # docst3 = db.collection(u'chargers').document(u'頭前國中地下停車場').collection(u'neighbor').where(u'id', u'==', tid3).stream()
    # for doct3 in docst3:
    #     latt3 = doct3.to_dict()['vlat']
    #     lngt3 = doct3.to_dict()['vlng']
    #     namet3 = doct3.to_dict()['name']
    #     addresst3 = doct3.to_dict()['viewaddress']
    #     t3 = {'pointaddress': addresst3, 'pointname': namet3 , 'pointlat': latt3, 'pointlng': lngt3}
    # dots.append(t3)
    
    # docst4 = db.collection(u'chargers').document(u'頭前國中地下停車場').collection(u'neighbor').where(u'id', u'==', tid4).stream()
    # for doct4 in docst4:
    #     latt4 = doct4.to_dict()['vlat']
    #     lngt4 = doct4.to_dict()['vlng']
    #     namet4 = doct4.to_dict()['name']
    #     addresst4 = doct4.to_dict()['viewaddress']
    #     t4 = {'pointaddress': addresst4, 'pointname': namet4 , 'pointlat': latt4, 'pointlng': lngt4}
    # dots.append(t4)
    realdis = round(distance/1000,2)
    # id1+'-'+id2+'-'+id3+'-'+id4
    rid = id1
    doc = {
              u'id': rid,
              u'route': dots,
              u'count': j+1,
              u'distance': realdis
              
         }
        #欲存入路徑
    db.collection(u'routes').document(u'頭前國中地下停車場').collection(u'plan').add(doc)