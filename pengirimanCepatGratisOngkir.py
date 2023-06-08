import PySimpleGUI as sg
from Queue import Queue
from Stack import Stack
import csv


def insertionSort(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1

        while j >= 0 and key[1] < data[j][1]:
            data[j+1] = data[j]
            j = j - 1

        data[j+1] = key

    return data


kota_tujuan = []
with open('kota_tujuan.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        kota = row[0]
        tujuan = int(row[1])
        pesanan = [kota, tujuan]
        kota_tujuan.append(pesanan)

kota_tujuan_sorted = insertionSort(kota_tujuan)
print(kota_tujuan_sorted)

urutan_tujuan = []
for i in kota_tujuan_sorted:
    urutan_tujuan.append(i[0])

print(urutan_tujuan)


class Kota:
    def __init__(self):
        self.order = urutan_tujuan


# Inisialisasi
kota = Kota()
Pesanan = Queue()
Pengemasan = Queue()
Pengiriman = Stack()


class Barang:
    def __init__(self, nama, tujuan):
        self.nama = nama
        self.tujuan = tujuan

    def info(self):
        print(f"Barang: {self.nama}")
        print(f"Kota Tujuan: {self.tujuan}")


def antrian_pesanan():
    if not Pesanan.is_empty():
        return [[barang.nama, barang.tujuan] for barang in Pesanan.get_values()]
    else:
        return []


def antrian_pengemasan():
    if not Pengemasan.is_empty():
        return [[barang.nama, barang.tujuan] for barang in Pengemasan.get_values()]
    else:
        return []


def antrian_pengiriman():
    if not Pengiriman.is_empty():
        return [[barang.nama, barang.tujuan] for barang in Pengiriman.get_values()]
    else:
        return []

# pesanan masuk (enqueue pesanan)


def pesanan_masuk(barang):
    Pesanan.enqueue(barang)
    print(
        f"Pesanan {barang.nama} telah ditambahkan ke dalam antrian pesanan.")

# pesanan pindah ke pengemasan (dequeue pesanan, enqueue pengemasan)


def kemas_pesanan():
    for barang in Pesanan.get_values():
        if barang.tujuan in kota.order:
            index = next((i for i, x in enumerate(Pengemasan.get_values()) if x.tujuan in kota.order and kota.order.index(
                x.tujuan) < kota.order.index(barang.tujuan)), None)
            if index is not None:
                Pengemasan.data.insert(index, barang)
            else:
                Pengemasan.enqueue(barang)
    Pesanan.data.clear()


# barang dikirim/dimasukkan ke dalam mobil (dequeue pengemasan, push barang dikirim)
kapasitas_pengiriman = 10


def kirim_pesanan(jumlah=1, kapasitas=10):
    global kapasitas_pengiriman
    if len(Pengiriman.get_values()) + jumlah <= kapasitas:
        for i in range(jumlah):
            pesanan = Pengemasan.dequeue()
            Pengiriman.push(pesanan)
        print(f"{jumlah} pesanan berhasil dikirim.")
    else:
        print("Jumlah pesanan melebihi kapasitas pengiriman.")

# barang sampai ke tujuan (pop stack barang dikirim)


def atur_kapasitas():
    global kapasitas_pengiriman
    input_kapasitas = sg.popup_get_text("Masukkan kapasitas pengiriman:")
    try:
        kapasitas_pengiriman = int(input_kapasitas)
        print("Kapasitas pengiriman berhasil diatur.")
    except ValueError:
        print("Kapasitas pengiriman tidak valid. Silakan masukkan angka.")


def pesanan_terkirim():
    if not Pengiriman.is_empty():
        tujuan_pertama = Pengiriman.peek().tujuan
        for barang in Pengiriman.get_values():
            if barang.tujuan == tujuan_pertama:
                barang_terkirim(barang)
        Pengiriman.data = [
            barang for barang in Pengiriman.get_values() if barang.tujuan != tujuan_pertama]

# clear barang pada stack dikirim dan masukkan ke dalam queue pesanan.


def batalkan_pengiriman():
    if not Pengiriman.is_empty():
        Pesanan.data.extend(Pengiriman.get_values())
        Pengiriman.data.clear()

# pencatatan barang yang telah terkirim


def barang_terkirim(barang):
    with open('barang_terkirim.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([barang.nama, barang.tujuan])


def main():
    # sorting
    def insertionSort3(data):
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1

            while j >= 0 and key < data[j]:
                data[j+1] = data[j]
                j = j - 1

            data[j+1] = key

        return data

    data = kota_tujuan_sorted
    listbaru = insertionSort3([item[0] for item in data])

    dropdown = listbaru

    # Layout GUI
    layout = [
        [sg.Text("Nama Barang"), sg.InputText(key="-NAMA-")],
        [sg.Text("Tujuan"), sg.DropDown(dropdown, key="-TUJUAN-")],
        [sg.Button("Pesanan Masuk"), sg.Button("Kemas Pesanan"),
         sg.Button("Kirim Pesanan"), sg.Button("Pesanan Terkirim")],
        [sg.Text("Daftar Pesanan")],
        [sg.Table(values=[], headings=["Nama Barang", "Tujuan"], key="-TABLE-PESANAN-",
                  justification="left", enable_events=True, num_rows=10, size=(60, 10))],
        [sg.Text("Daftar Barang Dikemas")],
        [sg.Table(values=[], headings=["Nama Barang", "Tujuan"], key="-TABLE-PENGEMASAN-",
                  justification="left", enable_events=True, num_rows=10, size=(60, 10))],
        [sg.Text("Daftar Barang Dikirim")],
        [sg.Table(values=[], headings=["Nama Barang", "Tujuan"], key="-TABLE-PENGIRIMAN-",
                  justification="left", enable_events=True, num_rows=10, size=(60, 10))],
        [sg.Button("Antrian Pesanan"), sg.Button("Atur Kapasitas"),
         sg.Button("Batalkan Pengiriman")],
        [sg.Output(size=(60, 10))],
        [sg.Button("Keluar")]
    ]

    # Membuat window GUI
    window = sg.Window("Aplikasi Gudang", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Keluar":
            break

        if event == "Pesanan Masuk":
            nama = values["-NAMA-"]
            tujuan = values["-TUJUAN-"]
            barang = Barang(nama, tujuan)
            pesanan_masuk(barang)

        if event == "Kemas Pesanan":
            kemas_pesanan()
            print("Pesanan berhasil dikemas.")

        if event == "Kirim Pesanan":
            try:
                jumlah_pesanan = int(sg.popup_get_text(
                    "Masukkan jumlah pesanan yang akan dikirim:"))
                kirim_pesanan(jumlah_pesanan, kapasitas_pengiriman)
            except ValueError:
                print("Jumlah pesanan tidak valid. Silakan masukkan angka.")

        if event == "Atur Kapasitas":
            atur_kapasitas()

        if event == "Pesanan Terkirim":
            pesanan_terkirim()
            print("Pesanan telah terkirim.")

        if event == "Antrian Pesanan":
            window["-TABLE-PESANAN-"].update(values=antrian_pesanan())
            window["-TABLE-PENGEMASAN-"].update(values=antrian_pengemasan())
            window["-TABLE-PENGIRIMAN-"].update(values=antrian_pengiriman())

        if event == "Batalkan Pengiriman":
            batalkan_pengiriman()
            print("Pengiriman dibatalkan.")
            window["-TABLE-PESANAN-"].update(values=antrian_pesanan())
            window["-TABLE-PENGEMASAN-"].update(values=antrian_pengemasan())
            window["-TABLE-PENGIRIMAN-"].update(values=antrian_pengiriman())

    window.close()


if __name__ == "__main__":
    main()
