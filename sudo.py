import random
import copy
import os
import sys

class PapanSudoku:
    """
    Kelas untuk merepresentasikan papan Sudoku dengan berbagai ukuran
    """
    
    def __init__(self, ukuran=9):
        """
        Inisialisasi papan Sudoku
        
        Args:
            ukuran (int): Ukuran papan (4, 6, atau 9)
        """
        self.ukuran = ukuran
        
        # Tentukan ukuran kotak sub-grid (box)
        if ukuran == 4:
            self.ukuran_kotak = 2  # 2x2
        elif ukuran == 6:
            self.ukuran_kotak_baris = 2  # 2x3
            self.ukuran_kotak_kolom = 3
        elif ukuran == 9:
            self.ukuran_kotak = 3  # 3x3
        else:
            raise ValueError("Ukuran hanya boleh 4, 6, atau 9")
        
        # Inisialisasi papan kosong
        self.papan = [[0 for _ in range(ukuran)] for _ in range(ukuran)]
        self.papan_solusi = [[0 for _ in range(ukuran)] for _ in range(ukuran)]
        self.papan_awal = [[0 for _ in range(ukuran)] for _ in range(ukuran)]
    
    def apakah_aman(self, baris, kolom, angka):
        """
        Cek apakah angka aman ditempatkan di posisi tertentu
        
        Args:
            baris (int): Indeks baris
            kolom (int): Indeks kolom
            angka (int): Angka yang akan ditempatkan
            
        Returns:
            bool: True jika aman, False jika tidak
        """
        # Cek baris
        if angka in self.papan[baris]:
            return False
        
        # Cek kolom
        for i in range(self.ukuran):
            if self.papan[i][kolom] == angka:
                return False
        
        # Cek kotak sub-grid
        if self.ukuran == 6:
            # Untuk 6x6, kotak berbentuk 2x3
            kotak_baris_awal = (baris // self.ukuran_kotak_baris) * self.ukuran_kotak_baris
            kotak_kolom_awal = (kolom // self.ukuran_kotak_kolom) * self.ukuran_kotak_kolom
            
            for i in range(kotak_baris_awal, kotak_baris_awal + self.ukuran_kotak_baris):
                for j in range(kotak_kolom_awal, kotak_kolom_awal + self.ukuran_kotak_kolom):
                    if self.papan[i][j] == angka:
                        return False
        else:
            # Untuk 4x4 dan 9x9
            kotak_baris_awal = (baris // self.ukuran_kotak) * self.ukuran_kotak
            kotak_kolom_awal = (kolom // self.ukuran_kotak) * self.ukuran_kotak
            
            for i in range(kotak_baris_awal, kotak_baris_awal + self.ukuran_kotak):
                for j in range(kotak_kolom_awal, kotak_kolom_awal + self.ukuran_kotak):
                    if self.papan[i][j] == angka:
                        return False
        
        return True
    
    def selesaikan_sudoku(self):
        """
        Selesaikan Sudoku menggunakan algoritma backtracking
        
        Returns:
            bool: True jika berhasil diselesaikan
        """
        # Cari sel kosong
        for baris in range(self.ukuran):
            for kolom in range(self.ukuran):
                if self.papan[baris][kolom] == 0:
                    # Coba angka 1 sampai ukuran
                    angka_list = list(range(1, self.ukuran + 1))
                    random.shuffle(angka_list)  # Randomize untuk variasi
                    
                    for angka in angka_list:
                        if self.apakah_aman(baris, kolom, angka):
                            self.papan[baris][kolom] = angka
                            
                            # Rekursif untuk sel berikutnya
                            if self.selesaikan_sudoku():
                                return True
                            
                            # Backtrack
                            self.papan[baris][kolom] = 0
                    
                    return False
        
        return True
    
    def generate_papan_lengkap(self):
        """
        Generate papan Sudoku yang sudah terisi lengkap (solusi)
        """
        self.papan = [[0 for _ in range(self.ukuran)] for _ in range(self.ukuran)]
        self.selesaikan_sudoku()
        self.papan_solusi = copy.deepcopy(self.papan)
    
    def hapus_angka(self, kesulitan):
        """
        Hapus beberapa angka dari papan berdasarkan tingkat kesulitan
        
        Args:
            kesulitan (str): 'mudah', 'sedang', atau 'sulit'
        """
        # Tentukan jumlah angka yang akan dihapus
        if kesulitan == 'mudah':
            jumlah_hapus = int(self.ukuran * self.ukuran * 0.3)  # 30%
        elif kesulitan == 'sedang':
            jumlah_hapus = int(self.ukuran * self.ukuran * 0.5)  # 50%
        elif kesulitan == 'sulit':
            jumlah_hapus = int(self.ukuran * self.ukuran * 0.65)  # 65%
        else:
            jumlah_hapus = int(self.ukuran * self.ukuran * 0.4)
        
        # List semua posisi
        posisi_list = [(i, j) for i in range(self.ukuran) for j in range(self.ukuran)]
        random.shuffle(posisi_list)
        
        # Hapus angka
        for i in range(jumlah_hapus):
            baris, kolom = posisi_list[i]
            self.papan[baris][kolom] = 0
        
        self.papan_awal = copy.deepcopy(self.papan)
    
    def reset_papan(self):
        """
        Reset papan ke kondisi awal (setelah generate)
        """
        self.papan = copy.deepcopy(self.papan_awal)


class TampilanSudoku:
    """
    Kelas untuk menangani tampilan Sudoku di terminal
    """
    
    def __init__(self, papan_sudoku):
        """
        Inisialisasi tampilan
        
        Args:
            papan_sudoku (PapanSudoku): Objek papan Sudoku
        """
        self.papan = papan_sudoku
    
    def bersihkan_layar(self):
        """
        Bersihkan layar terminal
        """
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def tampilkan_papan(self, highlight_posisi=None):
        """
        Tampilkan papan Sudoku dengan format yang rapi
        
        Args:
            highlight_posisi (tuple): Posisi (baris, kolom) yang akan di-highlight
        """
        self.bersihkan_layar()
        ukuran = self.papan.ukuran
        
        print("\n╔═══ SUDOKU GAME ═══╗\n")
        
        # Header kolom
        print("    ", end="")
        for j in range(ukuran):
            print(f" {j+1} ", end="")
        print()
        
        # Garis atas
        print("   ┌" + "─" * (ukuran * 3 + (ukuran // self.papan.ukuran_kotak if ukuran != 6 else ukuran // 3) - 1) + "┐")
        
        for i in range(ukuran):
            print(f" {i+1} │", end="")
            
            for j in range(ukuran):
                nilai = self.papan.papan[i][j]
                
                # Highlight posisi yang dipilih
                if highlight_posisi and highlight_posisi == (i, j):
                    if nilai == 0:
                        print(" _ ", end="")
                    else:
                        print(f"[{nilai}]", end="")
                else:
                    # Tampilkan angka atau titik kosong
                    if nilai == 0:
                        print(" . ", end="")
                    elif self.papan.papan_awal[i][j] != 0:
                        # Angka awal (dari soal) - bold
                        print(f" {nilai} ", end="")
                    else:
                        # Angka yang diisi pemain
                        print(f" {nilai} ", end="")
                
                # Garis vertikal untuk pemisah kotak
                if ukuran == 6:
                    if (j + 1) % 3 == 0 and j < ukuran - 1:
                        print("│", end="")
                else:
                    if (j + 1) % self.papan.ukuran_kotak == 0 and j < ukuran - 1:
                        print("│", end="")
            
            print("│")
            
            # Garis horizontal untuk pemisah kotak
            if ukuran == 6:
                if (i + 1) % 2 == 0 and i < ukuran - 1:
                    print("   ├" + "─" * (ukuran * 3 + 1) + "┤")
            else:
                if (i + 1) % self.papan.ukuran_kotak == 0 and i < ukuran - 1:
                    print("   ├" + "─" * (ukuran * 3 + (ukuran // self.papan.ukuran_kotak) - 1) + "┤")
        
        # Garis bawah
        print("   └" + "─" * (ukuran * 3 + (ukuran // self.papan.ukuran_kotak if ukuran != 6 else ukuran // 3) - 1) + "┘")
        print()


class PermainanSudoku:
    """
    Kelas utama untuk menjalankan permainan Sudoku
    """
    
    def __init__(self):
        """
        Inisialisasi permainan
        """
        self.papan = None
        self.tampilan = None
        self.ukuran = 9
        self.kesulitan = 'sedang'
    
    def menu_utama(self):
        """
        Tampilkan menu utama dan tangani pilihan
        """
        while True:
            os.system('clear' if os.name != 'nt' else 'cls')
            print("\n╔═════════════════════════════╗")
            print("║     SUDOKU GAME PYTHON      ║")
            print("╚═════════════════════════════╝\n")
            print("1. Main Game Baru")
            print("2. Atur Ukuran Papan")
            print("3. Atur Tingkat Kesulitan")
            print("4. Keluar")
            print("\n" + "─" * 31)
            
            pilihan = input("\nPilih menu (1-4): ").strip()
            
            if pilihan == '1':
                self.mulai_game_baru()
            elif pilihan == '2':
                self.atur_ukuran()
            elif pilihan == '3':
                self.atur_kesulitan()
            elif pilihan == '4':
                print("\nTerima kasih sudah bermain!")
                sys.exit(0)
            else:
                print("\nPilihan tidak valid!")
                input("Tekan Enter untuk melanjutkan...")
    
    def atur_ukuran(self):
        """
        Menu untuk mengatur ukuran papan
        """
        os.system('clear' if os.name != 'nt' else 'cls')
        print("\n╔═══ PILIH UKURAN PAPAN ═══╗\n")
        print("1. 4x4 (Pemula)")
        print("2. 6x6 (Menengah)")
        print("3. 9x9 (Klasik)")
        print("\n" + "─" * 27)
        
        pilihan = input("\nPilih ukuran (1-3): ").strip()
        
        if pilihan == '1':
            self.ukuran = 4
            print("\n✓ Ukuran papan: 4x4")
        elif pilihan == '2':
            self.ukuran = 6
            print("\n✓ Ukuran papan: 6x6")
        elif pilihan == '3':
            self.ukuran = 9
            print("\n✓ Ukuran papan: 9x9")
        else:
            print("\n✗ Pilihan tidak valid! Tetap menggunakan ukuran sebelumnya.")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    def atur_kesulitan(self):
        """
        Menu untuk mengatur tingkat kesulitan
        """
        os.system('clear' if os.name != 'nt' else 'cls')
        print("\n╔═══ PILIH TINGKAT KESULITAN ═══╗\n")
        print("1. Mudah (30% kosong)")
        print("2. Sedang (50% kosong)")
        print("3. Sulit (65% kosong)")
        print("\n" + "─" * 35)
        
        pilihan = input("\nPilih kesulitan (1-3): ").strip()
        
        if pilihan == '1':
            self.kesulitan = 'mudah'
            print("\n✓ Tingkat kesulitan: Mudah")
        elif pilihan == '2':
            self.kesulitan = 'sedang'
            print("\n✓ Tingkat kesulitan: Sedang")
        elif pilihan == '3':
            self.kesulitan = 'sulit'
            print("\n✓ Tingkat kesulitan: Sulit")
        else:
            print("\n✗ Pilihan tidak valid! Tetap menggunakan kesulitan sebelumnya.")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    def mulai_game_baru(self):
        """
        Mulai permainan baru
        """
        print("\n⏳ Membuat papan Sudoku...")
        
        # Generate papan baru
        self.papan = PapanSudoku(self.ukuran)
        self.papan.generate_papan_lengkap()
        self.papan.hapus_angka(self.kesulitan)
        
        self.tampilan = TampilanSudoku(self.papan)
        
        print("✓ Papan berhasil dibuat!")
        input("\nTekan Enter untuk mulai bermain...")
        
        self.loop_permainan()
    
    def cek_kemenangan(self):
        """
        Cek apakah pemain sudah menang
        
        Returns:
            bool: True jika menang
        """
        for i in range(self.ukuran):
            for j in range(self.ukuran):
                if self.papan.papan[i][j] != self.papan.papan_solusi[i][j]:
                    return False
        return True
    
    def loop_permainan(self):
        """
        Loop utama permainan
        """
        posisi_terpilih = None
        
        while True:
            self.tampilan.tampilkan_papan(posisi_terpilih)
            
            print("Perintah:")
            print("  [baris kolom angka] - Isi sel (contoh: 1 2 5)")
            print("  [baris kolom 0]     - Hapus angka di sel")
            print("  'cek'   - Cek jawaban")
            print("  'hint'  - Lihat solusi satu sel")
            print("  'reset' - Reset papan")
            print("  'menu'  - Kembali ke menu")
            print()
            
            perintah = input("Input: ").strip().lower()
            
            if perintah == 'menu':
                konfirmasi = input("\nYakin mau keluar? (y/n): ").strip().lower()
                if konfirmasi == 'y':
                    break
            
            elif perintah == 'reset':
                self.papan.reset_papan()
                print("\n✓ Papan di-reset ke kondisi awal!")
                input("Tekan Enter untuk melanjutkan...")
            
            elif perintah == 'cek':
                if self.cek_kemenangan():
                    self.tampilan.tampilkan_papan()
                    print("\n" + "═" * 40)
                    print("🎉 SELAMAT! KAMU MENANG! 🎉")
                    print("═" * 40)
                    input("\nTekan Enter untuk kembali ke menu...")
                    break
                else:
                    print("\n✗ Masih ada yang salah, coba lagi!")
                    input("Tekan Enter untuk melanjutkan...")
            
            elif perintah == 'hint':
                # Cari sel kosong dan isi dengan jawaban
                for i in range(self.ukuran):
                    for j in range(self.ukuran):
                        if self.papan.papan[i][j] == 0:
                            self.papan.papan[i][j] = self.papan.papan_solusi[i][j]
                            print(f"\n💡 Hint: Baris {i+1}, Kolom {j+1} = {self.papan.papan_solusi[i][j]}")
                            input("Tekan Enter untuk melanjutkan...")
                            break
                    else:
                        continue
                    break
            
            else:
                # Parse input baris kolom angka
                try:
                    parts = perintah.split()
                    if len(parts) != 3:
                        raise ValueError
                    
                    baris = int(parts[0]) - 1
                    kolom = int(parts[1]) - 1
                    angka = int(parts[2])
                    
                    # Validasi input
                    if not (0 <= baris < self.ukuran and 0 <= kolom < self.ukuran):
                        print("\n✗ Baris/kolom di luar jangkauan!")
                        input("Tekan Enter untuk melanjutkan...")
                        continue
                    
                    if not (0 <= angka <= self.ukuran):
                        print(f"\n✗ Angka harus 0-{self.ukuran}!")
                        input("Tekan Enter untuk melanjutkan...")
                        continue
                    
                    # Cek apakah sel bisa diubah
                    if self.papan.papan_awal[baris][kolom] != 0:
                        print("\n✗ Sel ini tidak bisa diubah (angka awal)!")
                        input("Tekan Enter untuk melanjutkan...")
                        continue
                    
                    # Isi atau hapus angka
                    self.papan.papan[baris][kolom] = angka
                    posisi_terpilih = (baris, kolom)
                    
                except ValueError:
                    print("\n✗ Format salah! Gunakan: baris kolom angka")
                    input("Tekan Enter untuk melanjutkan...")


def main():
    """
    Fungsi utama untuk menjalankan game
    """
    try:
        game = PermainanSudoku()
        game.menu_utama()
    except KeyboardInterrupt:
        print("\n\nGame dihentikan. Sampai jumpa!")
        sys.exit(0)


if __name__ == "__main__":
    main()