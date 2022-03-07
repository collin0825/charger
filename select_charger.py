# import count distance
from math import radians, cos, sin, asin, sqrt
def countdistance(lata, lnga, latb, lngb):
    mlata = float(lata)
    mlnga = float(lnga)
    mlatb = float(latb)
    mlngb = float(lngb)
    # 將十進位制度數轉化為弧度
    lat1, lng1, lat2, lng2 = map(radians, [mlata, mlnga, mlatb, mlngb])
    # haversine公式
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 地球平均半徑，單位為公里
    return round(c * r * 1000,2)
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
    api_key = 'AIzaSyBPu_5Fi8_Ouvq88730tMcVbKe2v4wwvRg'
    gmap_obj = googlemaps.Client(key=api_key)
    
    # read_chargingpile_file
    readfile = 'SelectChargingPileLL.csv'
    with open(readfile) as csvFile:
        csvReader = csv.reader(csvFile)
        listReport = list(csvReader)
        for row in listReport:
            name = row[0]
            #setfile
            file = name+'.xls'
            wb = xlwt.Workbook()
            datahead = ['名稱', '地址', '電話', '評價', '緯度', '經度',  '距離(m)', '預估時間(男)(mins)', '預估時間(女)(mins)', '消費水平', '營業時間']
            
            # setsearch
            slat = row[2]
            slng = row[1]
            address = row[3]
            # doc1 = {
            #     u'name': name,
            #     u'lat': slat,
            #     u'lng': slng,
            #     u'address': address
            # }
            #         #欲存入路徑
            # db.collection("chargers").document(name).set(doc1)
            # slat = '25.031924'
            # slng = '121.431691'
            radius = '500' 
            searchdata = ['convenience_store', 'cafe',\
                          'park', 'restaurant'
                         ]
            for s in range(len(searchdata)):
                print(searchdata[s]+": ")
                sh = wb.add_sheet(searchdata[s], cell_overwrite_ok=True)
                for i in range(len(datahead)):
                    sh.write(0, i, datahead[i])
                searchtype = searchdata[s]
                # url1 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=24.99862,121.4877&radius=850&type=restaurant&key=AIzaSyDHvu3CYK8QurHnBM2f6qVPba7Dknl5fL0&language=zh-TW'
                url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='\
                +slat+','+slng+'&radius='+radius+'&type='+searchtype+'&key='+api_key+\
                '&language=zh-TW'
                gmap = requests.get(url)
                gsoup = bs4.BeautifulSoup(gmap.text, 'html.parser')
                g_info = json.loads(gsoup.text)
                results = g_info['results']
                print('列出搜尋到結果的資料長度 : ', len(results))
                doc2 = {
                    searchtype: len(results)
                }
                db.collection("chargers").document(name).update(doc2)
                # for data in results:
                #     placeId = data['place_id']
                #     view_info = gmap_obj.place(place_id=placeId, language='zh_TW')['result']
                #     viewaddress = view_info['formatted_address']
                #     if ('formatted_phone_number' in view_info.keys()):
                #         viewphone = view_info['formatted_phone_number']
                #     else:
                #         viewphone = 'NA'
                #     vlat = view_info['geometry']['location']['lat']
                #     vlng = view_info['geometry']['location']['lng']
                #     # 抓取評價
                #     if ('rating' in view_info.keys()):
                #         rating = view_info['rating']
                #     else:
                #         rating = 'NA'
                #     # 抓取評論
                #     # if ('reviews' in view_info.keys()):
                #     #     contents = view_info['reviews']
                #     # else:
                #     #     contents = [{'author_name':'NA', 'relative_time_description': 'NA', 'text': 'NA'}]
                #     distance = countdistance(slat, slng, vlat, vlng)
                #     # 抓取消費水平
                #     if ('price_level' in view_info.keys()):
                #         price_level = view_info['price_level']
                #     else:
                #         price_level = 'NA'
                #     # 抓取營業時間
                #     if ('opening_hours' in view_info.keys()):
                #         workdays  = view_info['opening_hours']['weekday_text']
                #     else:
                #         workdays  = 'NA'
                #     #計算預估時間 男:1.23 m/s
                #     mantime = round(distance/1.23/60,2)
                #     #計算預估時間 女:1.18 m/s
                #     womantime = round(distance/1.18/60,2)
                #     print(results.index(data)+1)
                #     print("名稱: ", data['name'])
                #     print("地址: ", viewaddress)
                #     print("電話: ", viewphone)
                #     print("評價: ", rating)
                #     print("緯度: ", vlat)
                #     print("經度: ", vlng)
                #     print("距離: ", distance)
                #     print("預估時間(男): ", mantime)
                #     print("預估時間(女): ", womantime)
                #     print("消費水平: ", price_level)
                #     print("營業時間: ", workdays)
                #     rdata=[]
                #     rdata.append(data['name'])
                #     rdata.append(viewaddress)
                #     rdata.append(viewphone)
                #     rdata.append(rating)
                #     rdata.append(vlat)
                #     rdata.append(vlng)
                #     rdata.append(distance)
                #     rdata.append(mantime)
                #     rdata.append(womantime)
                #     rdata.append(price_level)
                #     rdata.append(workdays)
                # #     # 加入評論
                # #     # for i in range(len(contents)):
                # #     #     item = []
                # #     #     author = contents[i]['author_name']
                # #     #     relative_time = contents[i]['relative_time_description']
                # #     #     text = contents[i]['text']
                # #     #     item.append(author)
                # #     #     item.append(relative_time)
                # #     #     item.append(text)
                # #     #     rdata.append(item)
                # #     # 寫進excel
                # #     for j in range(len(rdata)):
                # #         sh.write(results.index(data)+1, j, rdata[j])
                        
                # #     #欲寫入firebase之資料格式
                #     doc = {
                #       u'name': data['name'],
                #       u'viewaddress': viewaddress,
                #       u'viewphone': viewphone,
                #       u'rating': rating,
                #       u'vlat': vlat,
                #       u'vlng': vlng,
                #       u'distance': distance,
                #       u'mantime': mantime,
                #       u'womantime': womantime,
                #       u'price_level': price_level,
                #       u'workdays': workdays,
                #       u'type': searchtype
                #     }
                #     #欲存入路徑
                #     db.collection('chargers').document(name).collection('neighbor').add(doc)
                    
                # wb.save(file)
                print('*'*70)
main()



    