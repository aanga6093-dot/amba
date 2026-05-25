from datetime import datetime
import json

now = datetime.now()
kata = "mas dend"
user = input("input mas den (hari,bulan,tahun) gitu lah")


if user == "tahun":
 print("sekarang tahun ",now.year,kata)
elif user == "bulan":
 print("sekarang",user,now.month,kata)
elif user == "hari":
 print("sekarang",user,now.day,kata)
elif user == "mingu":
 print("sekarang",user,now.hour,kata)
elif user == "menit":
 print("sekarang",user,now.minute,kata)
else:
 print("waduh input salah bang den")
