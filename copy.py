from datetime import datetime
import json

now = datetime.now()


print(now.year)
print(now.month)
print(now.day)
print(now.hour)
print(now.minute)
templat = {
    now.year:{
        now.month:{
            now.day:{}
        },
        "tootal_1moth":0
    },
    "total_1year":0
}
with  open("money.json","w") as var:
    {} 
def set():
    sruct = {now.minute:[int(input("uang:")),input("keperluan:")]}

    with  open("money.json","r") as nor:
        data = json.load(nor)
    data[now.year][now.month][now.day] = sruct
    data[now.year][now.moth] = sum(list(map(lambda  ls : x[1],list(data[now.year][now.month][now.day].values()))))
    print(data)
    with  open("money.json","w") as var:
        json.dump(data,var,indent = 4)
set()        
        
        
        
