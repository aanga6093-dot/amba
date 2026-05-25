import math
import cmath
def warna(nama_warna):
    kode_warna = {
        "hitam": "\033[30m",
        "merah": "\033[31m",
        "hijau": "\033[32m",
        "kuning": "\033[33m",
        "biru": "\033[34m",
        "ungu": "\033[35m",
        "cyan": "\033[36m",
        "putih": "\033[37m",
        "reset": "\033[0m"
    }
    if nama_warna.lower() in kode_warna:
        print(kode_warna[nama_warna.lower()], end="")
    else:
        print("\033[0m", end="")  # default jika nama warna tidak dikenal

# Contoh penggunaan:
warna("hijau")
print("Ini teks berwarna hijau")
warna("putih")
print("Ini teks kembali putih")
def calculator():
    CONSTANTS = {
        "π": math.pi,
        "pi": math.pi,
        "e": math.e,
        "g": 9.80665,
        "phi": (1 + math.sqrt(5))/2,
        "c": 299792458
    }

    def input_number(prompt):
        """Input angka atau konstanta, aman dari error"""
        while True:
            inp = input(prompt).strip().lower()
            if inp in CONSTANTS:
                return CONSTANTS[inp]
            try:
                return float(inp)
            except ValueError:
                warna("merah")
                print("Input salah, masukkan angka atau konstanta yang valid.")
                warna("hijau")

    def show_box(a):
        """Tampilkan nilai saat ini dalam kotak ASCII yang aman"""
        val_str = str(a)
        width = max(len(val_str), 17)
        line = "_" * (width + 2)
        print("\033[36m")  # warna cyan
        print(line)
        print(f"| Nilai sekarang: {val_str}".ljust(width + 2) + "|")
        print(line)
        print("\033[32m")  # warna hijau

    # Judul dan hiasan Pi tetap tampil sekali
    print("\033[36m \033[O")
    print("========== Mini Advanced Calculator ==========")
    print()
    print("             3,1415926535897932384626433")
    print("           83279502884197169399375105820")
    print("          97494459230781640628620899862")
    print("         8034      224      27")
    print("        825        877      99")
    print("        32         79      807")
    print("                  296      774")
    print("                  511      092")
    print("                 799      9624")
    print("                 609      6415")
    print("                833       0098")
    print("               0087       1127")
    print("              91378       9883")
    print("              2541        8621")
    print("             09733        21091")
    print("             12338        12577")
    print("            54480          6552")
    print("            3891           7827")
    print("\033[32m \033[O")

    a = input_number("Masukkan angka pertama (atau konstanta π/e/g/phi/c): ")
    history = []  # catatan riwayat

    while True:
        print("\n===== Menu Operasi =====")
        print("1.(+),2.(-), 3.(*) ,4.(/)")
        print("5.(√), 6.(^), 7. Cos(), 8. Sin()")
        print("9.Tan ,10. Acos,11. Asin,12.Atan")
        print("13. Exp,14. (i),15.(=)")
        print("16. exit 17.hapus")

        pilihan = input("Pilih operasi: ").strip().lower()

        if pilihan in ["1", "+"]:
            b = input_number("Angka yang ditambah: ")
            history.append(f"{a} + {b} = {a+b}")
            a += b
        elif pilihan in ["2", "-"]:
            b = input_number("Angka yang dikurangi: ")
            history.append(f"{a} - {b} = {a-b}")
            a -= b
        elif pilihan in ["3", "*", "x"]:
            b = input_number("Angka yang dikali: ")
            history.append(f"{a} * {b} = {a*b}")
            a *= b
        elif pilihan in ["4", "/"]:
            b = input_number("Angka yang dibagi: ")
            if b == 0:
                print("Error: Tidak bisa dibagi 0")
            else:
                history.append(f"{a} / {b} = {a/b}")
                a /= b
        elif pilihan in ["5", "√"]:
            if a < 0:
                result = cmath.sqrt(a)
                history.append(f"√({a}) = {result}")
                a = result
            else:
                result = math.sqrt(a)
                history.append(f"√({a}) = {result}")
                a = result
        elif pilihan in ["6", "^"]:
            b = input_number("Pangkat: ")
            history.append(f"{a} ^ {b} = {a**b}")
            a = a ** b
        elif pilihan in ["7", "cos"]:
            result = math.cos(a)
            history.append(f"cos({a}) = {result}")
            a = result
        elif pilihan  == "17":
            a = 0   
        elif pilihan in ["8", "sin"]:
            result = math.sin(a)
            history.append(f"sin({a}) = {result}")
            a = result
        elif pilihan in ["9", "tan"]:
            result = math.tan(a)
            history.append(f"tan({a}) = {result}")
            a = result
        elif pilihan in ["10", "arccos", "acos"]:
            result = math.acos(a)
            history.append(f"acos({a}) = {result}")
            a = result
        elif pilihan in ["11", "arcsin", "asin"]:
            result = math.asin(a)
            history.append(f"asin({a}) = {result}")
            a = result
        elif pilihan in ["12", "arctan", "atan"]:
            result = math.atan(a)
            history.append(f"atan({a}) = {result}")
            a = result
        elif pilihan in ["13", "exp"]:
            result = math.exp(a)
            history.append(f"exp({a}) = {result}")
            a = result
        elif pilihan in ["14", "imajiner", "i"]:
            result = complex(0, a)
            history.append(f"{a}i = {result}")
            a = result
        elif pilihan in ["15", "="]:
            warna("cyan")
            print("\n===== Riwayat Pengerjaan =====")
            for step in history:
                print(step)
            warna("biru")    
            print(f"\nHasil Akhir: {a}")
            warna("hijau")
            with open("Todosearh.txt", "w") as file:
                file.write("===== Riwayat Pengerjaan =====\n")
                for step in history:
                    file.write(step + "\n")
                file.write(f"\nHasil Akhir: {a}\n")
        elif pilihan in ["16", "exit", "keluar"]:
            print("Keluar dari kalkulator")
            break
        else:
        
            print("\033[31mPilihan tidak valid, coba lagi.\033[32m \033[O")

calculator()











