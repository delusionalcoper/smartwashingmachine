import time
import sys

KAPASITAS_TABUNG = 55
BATAS_BERAT_PAKAIAN = 8
DEBIT_AIR = 6  # Liter/Menit

JENIS_PUTARAN = [
    "Regular", "Delicates", "Mixed", "Wool",
    "Heavy Duty", "Bedding", "Quick Wash"
]

# Durasi standar pengeringan (detik) dan kekuatan putaran
PENGERINGAN_STANDAR = {
    1: (7 * 60, "cepat"),
    2: (5 * 60, "lambat"),
    3: (7 * 60, "sedang"),
    4: (3 * 60, "lambat"),
    5: (9 * 60, "cepat"),
    6: (9 * 60, "sangat cepat"),
    7: (3 * 60, "cepat"),
}


def input_int(prompt, minimum=None, maximum=None):
    """Meminta bilangan bulat dan memvalidasi rentangnya."""
    while True:
        try:
            nilai = int(input(prompt))
            if minimum is not None and nilai < minimum:
                print(f"Masukkan angka minimal {minimum}.")
                continue
            if maximum is not None and nilai > maximum:
                print(f"Masukkan angka maksimal {maximum}.")
                continue
            return nilai
        except ValueError:
            print("Masukkan bilangan bulat yang valid.")


def input_ya_tidak(prompt):
    while True:
        jawaban = input(prompt).strip().lower()
        if jawaban in ("yes", "no"):
            return jawaban
        print("Masukkan yes atau no.")


def hitung_mundur(total_detik, pesan="Sisa waktu"):
    """Simulasi penghitung waktu; jeda 0.01 detik mempercepat demonstrasi."""
    while total_detik > 0:
        menit, detik = divmod(total_detik, 60)
        print(f"\r{pesan}: {menit:02d}:{detik:02d}", end="", flush=True)
        time.sleep(0.01)
        total_detik -= 1
    print()


def proses_pencucian():
    """Menjalankan pengaturan dan simulasi pencucian; mengembalikan jenis program."""
    while True:
        try:
            berat_pakaian = float(input("Berat pakaian (kg): "))
            if 0 < berat_pakaian <= BATAS_BERAT_PAKAIAN:
                break
            print(f"Berat harus lebih dari 0 dan maksimal {BATAS_BERAT_PAKAIAN} kg.")
        except ValueError:
            print("Masukkan angka yang valid.")

    volume_pakaian = berat_pakaian * 2.5
    print(f"Perkiraan volume pakaian: {volume_pakaian:.1f} liter")

    level_air = [0.25, 0.5, 0.75, 1]
    while True:
        pilihan_air = input_int(
            "Pilih water level: 1) 1/4  2) 1/2  3) 3/4  4) Penuh: ", 1, 4
        )
        target_volume = KAPASITAS_TABUNG * level_air[pilihan_air - 1]
        if target_volume > volume_pakaian:
            break
        print("Water level terlalu rendah. Pilih yang lebih tinggi.")

    rinse_hold = input("Aktifkan Rinse Hold? (iya/tidak): ").strip().lower()
    while rinse_hold not in ("iya", "tidak"):
        print("Ketik iya atau tidak.")
        rinse_hold = input("Aktifkan Rinse Hold? (iya/tidak): ").strip().lower()

    if rinse_hold == "iya":
        waktu_rendam = input_int("Waktu rendam (menit): ", 1)
        print(f"Rinse Hold aktif selama {waktu_rendam} menit.")
        hitung_mundur(waktu_rendam * 60, "Sisa waktu rendam")
    else:
        print("Rinse Hold tidak aktif.")

    jumlah_bilasan = input_int("Jumlah bilasan (1-3): ", 1, 3)
    durasi_cuci = input_int("Durasi tiap proses (15-40 menit): ", 15, 40)

    print("\nPilih jenis putaran:")
    for nomor, nama in enumerate(JENIS_PUTARAN, start=1):
        print(f"{nomor}. {nama}")
    pilihan_putaran = input_int("Pilih jenis putaran (1-7): ", 1, 7)

    # Pengaturan Putaran dan RPM
    pengaturan_putaran = {
        1: ("Sedang", 800),
        2: ("Pelan", 400),
        3: ("Sedang", 800),
        4: ("Sangat pelan", 400),
        5: ("Kuat", 1200),
        6: ("Kuat", 1200),
        7: ("Cepat", 1000),
    }
    kekuatan_putaran, rpm_putaran = pengaturan_putaran[pilihan_putaran]
    print("Jenis putaran:", JENIS_PUTARAN[pilihan_putaran - 1])
    print("Kekuatan putaran:", kekuatan_putaran)
    print("Kecepatan putaran:", rpm_putaran, "RPM")

    volume_air_target = target_volume - volume_pakaian
    volume_air = 0.0
    print("\nMengisi air...")
    while volume_air < volume_air_target:
        volume_air = min(volume_air + DEBIT_AIR / 60, volume_air_target)
        print(f"\rVolume air: {volume_air:.1f} liter", end="", flush=True)
        time.sleep(0.01)
    print("\nPengisian air selesai.")

    takaran_detergen = berat_pakaian * 5
    print(f"Takaran detergen: {takaran_detergen:.1f} ml")

    total_detik = jumlah_bilasan * durasi_cuci * 60
    print("Proses pencucian dimulai...")
    hitung_mundur(total_detik)
    print("Proses pencucian selesai.")

    return pilihan_putaran


def proses_pengeringan(pilihan_putaran=None):
    """Fungsi pengeringan yang dipakai mode 2 maupun mode 3."""
    if pilihan_putaran is None:
        print("\nPilih program pengeringan:")
        for nomor, nama in enumerate(JENIS_PUTARAN, start=1):
            print(f"{nomor}. {nama}")
        pilihan_putaran = input_int("Pilih program (1-7): ", 1, 7)

    durasi_standar, kekuatan_standar = PENGERINGAN_STANDAR[pilihan_putaran]
    durasi_detik = durasi_standar
    kekuatan = kekuatan_standar

    print(f"Program: {JENIS_PUTARAN[pilihan_putaran - 1]}")
    print(f"Pengaturan awal: {durasi_detik // 60} menit, putaran {kekuatan}")

    if input_ya_tidak("Apakah ingin mengubah waktu pengeringan? (yes/no): ") == "yes":
        while True:
            menit_baru = input_int(
                "Berapa lama waktu pengeringan? (1-15 menit, 0 untuk tetap standar): ",
                0, 15
            )
            if menit_baru == 0:
                print("Durasi tetap menggunakan pengaturan awal.")
                break
            durasi_detik = menit_baru * 60
            break

    if input_ya_tidak("Apakah ingin mengubah kekuatan pemerasan? (yes/no): ") == "yes":
        pilihan_kekuatan = [
            "lambat", "sedang", "cepat", "sangat cepat"
        ]
        print("1. Lambat\n2. Sedang\n3. Cepat\n4. Sangat cepat")
        nomor_kekuatan = input_int(
            "Pilih kekuatan (1-4, 0 untuk tetap standar): ", 0, 4
        )
        if nomor_kekuatan != 0:
            kekuatan = pilihan_kekuatan[nomor_kekuatan - 1]
        else:
            print("Kekuatan tetap menggunakan pengaturan awal.")

    print(f"Pengeringan berjalan dengan putaran {kekuatan}.")
    hitung_mundur(durasi_detik, "Pengeringan selesai dalam")
    print("Proses pengeringan selesai. Pakaian siap disimpan.")


def proses_clean_tub():
    while True:
        isi_mesin = input("Apakah mesin cuci sedang ada isinya? (yes/no): ").strip().lower()
        if isi_mesin == "yes":
            print("Program Clean Tub tidak bisa digunakan jika mesin berisi pakaian.")
            return
        if isi_mesin == "no":
            print("Proses Clean Tub dimulai.")
            hitung_mundur(8 * 60, "Pembersihan selesai dalam")
            print("Proses Clean Tub selesai. Mesin cuci siap digunakan kembali.")
            return
        print("Input tidak valid, masukkan yes atau no.")


def main():
    print("PROGRAM MESIN CUCI")
    print("1. Pencucian saja")
    print("2. Pencucian dan pengeringan")
    print("3. Pengeringan saja")
    print("4. Clean Tub")

    mode = input_int("Pilih mode (1-4): ", 1, 4)

    if mode == 1:
        proses_pencucian()
    elif mode == 2:
        pilihan_putaran = proses_pencucian()
        # Memanggil fungsi pengeringan
        proses_pengeringan(pilihan_putaran)
    elif mode == 3:
        proses_pengeringan()
    elif mode == 4:
        proses_clean_tub()


if __name__ == "__main__":
    main()