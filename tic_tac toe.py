

import random

data = [
    [" "," "," "],
    [" "," "," "],
    [" "," "," "]
    ]
nama1 = input("nama1:")
nama2 = input("nama2:")
def vertikal(user):
    for i in range(len(data)):
        kondisi = []
        for j in range(len(data[0])):
            kondisi.append(data[j][i])
        if kondisi[0] == user and kondisi[1] == user and kondisi[2] == user:
            
            return True
    return False            
    
def silang(user): 
    if data[0][0] == user and data[1][1] == user and data[2][2] == user:
        data[0][0] = "✅"
        data[1][1] = "✅"
        data[2][2] = "✅"  
        return True
    if data[0][2] == user and data[1][1] == user and data[2][0] == user:
        data[0][2] = "✅"
        data[1][1] = "✅" 
        data[2][0] = "✅"
        return True
    return False 
                      
def horizon(user):
    for row in data:
        if row[0] == user and row[1] == user and row[2] == user:
            data[data.index(row)] = ["✅","✅","✅"]
            return True
    return False                

def keluar():
    for x in data:
        print(x) 
        print()          
penuh = lambda : " " not in sum(data,[]) 

tungul = ["o","x"]

user = random.choice(tungul)
print('pertama :',user)



while True:
    ram_tung = tungul.copy()
    try:
        
        if vertikal(tungul[0]) or horizon(tungul[0]) or silang(tungul[0]):
            keluar()
            print(tungul[0],"menang!")
            break
        if  vertikal(tungul[1]) or horizon(tungul[1]) or silang(tungul[1]):  
            keluar() 
            print(tungul[1],"menang!")
            break
        keluar()    
        if user == "o":
            print("giliran",user1)
        elif user == "x":
            print("giliran",user2)
        posisi = [int(input("y:"))-1,int(input("x:"))-1]    
        
        if data[posisi[0]][posisi[1]] == " ":
            data[posisi[0]][posisi[1]] = user 
            
            ram_tung.remove(user)
            if vertikal(user) or horizon(user) or silang(user):
                keluar()
                print(user,"menang!")
                break    
            elif penuh():
                print("seri")
            user = random.choice(ram_tung)    
        else:
            print("sudah di isi")    
            
             
    except NameError:
        print("<input you salah>")
    
    
        
        