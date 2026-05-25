from datetime import datetime
import json

now = datetime.now()
kata = "mas dendra"
user = input("input",kata)


if user == "tahun":
 print("sekarang tahun ",now.year,kata)
elif userr == "bulan":
 print("sekarang",user,now.month,kata)
elif user == "hari":
 print("sekarang",user,now.day,kata)
elif user == "mingu":
 print(now.hour)
elif user == "menit":
 print(now.minute)
else:
 print("waduh input salah bang den")
