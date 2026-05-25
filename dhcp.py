"""
DHCP simpel gueh 
"""
list_ip_hp = ["154.869.75.0","154.869.75.0","154.869.75.0","154.869.75.0"]

def pilah(ip_hp):
    list_digit = ip_hp.split(".")
    return ".".join(list_digit[:3])
    
for i,ip_hp in enumerate(list_ip_hp):
    list_ip_hp[i] = pilah(ip_hp) + "." + str(i)
print(list_ip_hp)    
    
    
    
    
    
    