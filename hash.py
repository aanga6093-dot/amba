from hashlib import sha256  # nyokot algoritma sha256 jeng hessing pasword Tina hashlib
from os import path  # pake path Tina os make data base Jason jadi kudu cek file nya Aya teu
from random import choice
from string import digits, ascii_letters  # eta ascietesn nyokot Kabeh hurup
from json import dump, load

DB_FILE = "users.json"  # eta ungu variabel penting nama file amih wawuh jelas


def get_salt():
    panjang = 5
    asci = digits + ascii_letters
    return "".join([
        choice(asci)
        for _ in range(panjang)
    ])


def sha_hash(password, salt):  # fungi hash NU make salt jeng cegah lamun sandi srua
    opjek = sha256((password + salt).encode())  # en code ubah string jadi hex biner
    return opjek.hexdigest()  # eta ubah hex jadi digit str


def load_users():  # nyokot di data base json
    if not path.exists(DB_FILE):  # tina liblayt OS teang BISI can Aya file nya
        with open(DB_FILE, "w") as f:
            dump({}, f)

    with open(DB_FILE, "r") as f:
        return load(f)


def save_users(users):  # asup data base json
    with open(DB_FILE, "w") as f:
        dump(users, f, indent=4)


def register():
    users = load_users()

    salt = get_salt()
    username = input("Buat username: ")
    password = sha_hash(input("Buat password: "), salt)

    if username in users:
        print("Username sudah ada.")
        return

    users[username] = {
        "password": password,
        "salt": salt
    }
    save_users(users)
    print("Berhasil daftar.")


def login():
    
    users = load_users()
    try:
        username = input("Username: ")
        password = sha_hash(input("Password: "), users[username]["salt"])
    except KeyError:
        print("user name gak ada")
        return 

    if username in users and users[username]["password"] == password:
        print("Login berhasil.")
    else:
        print("Username lu salah ngebtot")


def main():
    # tah ie beunget fitur na
    while True:
        print("\n1. Daftar")
        print("2. Login")
        print("3. Keluar")

        choice = input("Pilih: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()