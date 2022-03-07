def main():
    # 引用必要套件
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore
    
    # 引用私密金鑰
    cred = credentials.Certificate('serviceAccount.json')
    
    # 初始化firebase，注意不能重複初始化
    firebase_admin.initialize_app(cred)
    
    # 初始化firestore
    db = firestore.client()

    # setcenter
    import requests, bs4, json, googlemaps, xlwt, csv
    api_key = 'AIzaSyDzJ7f7PEVtP3WRXYJJoXAEnMcjpf5strU'
    gmap_obj = googlemaps.Client(key=api_key)
    
    # read_chargingpile_file
    readfile = 'SelectChargingPileLL.csv'
    with open(readfile) as csvFile:
        csvReader = csv.reader(csvFile)
        listReport = list(csvReader)
        for row in listReport:
            name = row[0]
            # setsearch
            slat = row[2]
            slng = row[1]
            doc1 = {
                u'name': name,
                u'lat': slat,
                u'lng': slng,
            }
                    #欲存入路徑
            db.collection("charger").document('name').set(doc1)
            
                    
    
main()