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

for i in range(212, 1044, 1):
    docs = db.collection(u'routes').document(u'後港新公園地下停車場').collection(u'plan').where(u'count', u'==', i).stream()
    for doc in docs:
        a = doc.id
        db.collection(u'routes').document(u'後港新公園地下停車場').collection(u'plan').document(a).delete()

