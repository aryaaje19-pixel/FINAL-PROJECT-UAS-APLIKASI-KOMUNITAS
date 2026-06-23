import csv
import os

# Konfigurasi
FILE_NAME = 'komunitas ROG VORTEX.csv'
FIELDNAMES = ['id', 'nama', 'peran', 'tahun_gabung']

# 1. Hash Map (Dictionary): Untuk menyimpan data di memori dengan akses O(1) berdasarkan ID
members_db = {} 

# 2. Stack (List): Untuk menyimpan riwayat penghapusan (Fitur Undo)
undo_stack = [] 


def init_csv():
    """Membuat file CSV jika belum ada."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

def load_data():
    """Membaca data dari CSV ke Hash Map."""
    global members_db
    members_db.clear()
    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            members_db[row['id']] = row

def save_data():
    """Menyimpan seluruh isi Hash Map ke file CSV."""
    with open(FILE_NAME, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for member_id, data in members_db.items():
            writer.writerow(data)

def quick_sort(arr):
    """Mengurutkan list of dictionary berdasarkan 'nama' (Ascending)."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]['nama'].lower()
    left = [x for x in arr if x['nama'].lower() < pivot]
    middle = [x for x in arr if x['nama'].lower() == pivot]
    right = [x for x in arr if x['nama'].lower() > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def binary_search(arr, target_name):
    """Mencari anggota berdasarkan nama pada data yang sudah diurutkan."""
    low = 0
    high = len(arr) - 1
    target = target_name.lower()
    
    while low <= high:
        mid = (low + high) // 2
        mid_val = arr[mid]['nama'].lower()
        
        if mid_val == target:
            return arr[mid]
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return None

# OPERASI CRUD
def create_member():
    print("\n--- TAMBAH ANGGOTA ---")
    m_id = input("ID Anggota   : ")
    if m_id in members_db:
        print("Error: ID sudah terdaftar!")
        return
    
    nama = input("Nama         : ")
    peran = input("Peran        : ")
    tahun = input("Tahun Gabung : ")
    
    members_db[m_id] = {'id': m_id, 'nama': nama, 'peran': peran, 'tahun_gabung': tahun}
    save_data()
    print("Data berhasil ditambahkan.")

def read_members():
    print("\n--- DAFTAR ANGGOTA KOMUNITAS ---")
    if not members_db:
        print("Data masih kosong.")
        return
        
    print(f"{'ID':<15} | {'Nama':<20} | {'Peran':25} | {'Tahun'}")
    print("-" * 60)
    for data in members_db.values():
        print(f"{data['id']:<15} | {data['nama']:<20} | {data['peran']:<25} | {data['tahun_gabung']}")

def update_member():
    print("\n--- UPDATE DATA ANGGOTA ---")
    m_id = input("Masukkan ID yang akan diupdate: ")
    if m_id not in members_db:
        print("Error: ID tidak ditemukan.")
        return

    print("Kosongkan isian jika tidak ingin mengubah data.")
    nama = input(f"Nama baru ({members_db[m_id]['nama']}): ") or members_db[m_id]['nama']
    peran = input(f"Peran baru ({members_db[m_id]['peran']}): ") or members_db[m_id]['peran']
    tahun = input(f"Tahun baru ({members_db[m_id]['tahun_gabung']}): ") or members_db[m_id]['tahun_gabung']
    
    members_db[m_id] = {'id': m_id, 'nama': nama, 'peran': peran, 'tahun_gabung': tahun}
    save_data()
    print("Data berhasil diupdate.")

def delete_member():
    print("\n--- HAPUS DATA ANGGOTA ---")
    m_id = input("Masukkan ID yang akan dihapus: ")
    if m_id in members_db:
        undo_stack.append(members_db[m_id]) 
        
        del members_db[m_id]
        save_data()
        print("Data berhasil dihapus.")
    else:
        print("Error: ID tidak ditemukan.")

def undo_delete():
    print("\n--- UNDO HAPUS ---")
    if not undo_stack:
        print("Tidak ada riwayat penghapusan.")
        return
    
    restored_member = undo_stack.pop()
    members_db[restored_member['id']] = restored_member
    save_data()
    print(f"Data atas nama {restored_member['nama']} berhasil dikembalikan.")

def search_and_sort_menu():
    print("\n--- CARI ANGGOTA BERDASARKAN NAMA ---")
    target = input("Masukkan Nama yang dicari: ")
    
    # Ubah Hash Map menjadi List of Dictionary untuk diproses
    member_list = list(members_db.values())
    
    # 1. Sorting data menggunakan Quick Sort
    sorted_members = quick_sort(member_list)
    
    # 2. Searching menggunakan Binary Search
    result = binary_search(sorted_members, target)
    
    if result:
        print("\n[Data Ditemukan]")
        print(f"ID    : {result['id']}")
        print(f"Nama  : {result['nama']}")
        print(f"Peran : {result['peran']}")
        print(f"Tahun : {result['tahun_gabung']}")
    else:
        print("\nData tidak ditemukan.")


def main():
    init_csv()
    load_data()
    
    while True:
        print("\n=== APLIKASI SISTEM KOMUNITAS ROG VORTEX ===")
        print("1. Tambah Anggota")
        print("2. Lihat Anggota")
        print("3. Ubah Data")
        print("4. Hapus Anggota")
        print("5. Cari Anggota")
        print("6. Undo Hapus Anggota")
        print("0. Keluar")
        
        pilihan = input("Pilih menu (0-6): ")
        
        if pilihan == '1':
            create_member()
        elif pilihan == '2':
            read_members()
        elif pilihan == '3':
            update_member()
        elif pilihan == '4':
            delete_member()
        elif pilihan == '5':
            search_and_sort_menu()
        elif pilihan == '6':
            undo_delete()
        elif pilihan == '0':
            print("Keluar dari aplikasi. Data telah diamankan di komunitas.csv.")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()