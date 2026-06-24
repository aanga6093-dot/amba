import string
key = 20

text = ""

kata_baru = ""

#esi na abcdefgh.. terus 
kata = string.ascii_lowercase + " " + string.ascii_lowercase + " "

for chat in text:
    if chat in kata:
        
        indet = kata.index(2,chat) + key
        kata_baru += kata[indet]
    
print(kata_baru)    
