import zerorpc
import socket
import threading

# Inisiasi socket TCP/IPv4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Kelas sebagai rujukan Serve
class InternetServiceProvider(object):
    myPulsa = 5500          #Deklarasi myPulsa sebagai object
    quotaPulse = 1000000    #Deklarasi penyedia pulsa (ISP) sebagai object
    def quotaAvailable(self, nominalBeliISP):
        c = zerorpc.Client()
        c.connect("tcp://127.0.0.1:2000")
        #Jika sisa pulsa pada ISP kurang dari permintaan, maka batalkan layanan
        if InternetServiceProvider.quotaPulse < nominalBeliISP :
            return "Layanan sedang bermasalah, silahkan coba beberapa saat lagi."
        #Jika sisa pulsa mencukupi dari penawaran, lanjutkan transaksi
        else :
            #Jika sisa saldo tersedia, lanjutkan transaksi
            if c.pembelian(nominalBeliISP) == True :
                InternetServiceProvider.myPulsa = nominalBeliISP + InternetServiceProvider.myPulsa
                InternetServiceProvider.quotaPulse = InternetServiceProvider.quotaPulse - nominalBeliISP
                print("Sisa stok pulsa ISP : Rp{}".format(InternetServiceProvider.quotaPulse))
                return "\nPembelian Pulsa Anda Sejumlah Rp%d Telah Berhasil.\n\n" % nominalBeliISP
            #Jika sisa saldo kurang, batalkan transaksi
            elif c.pembelian(nominalBeliISP) == False : 
                return "\nSaldo Anda Tidak Cukup\n\n"

    #Deklarasi fungsi cek pulsa
    def cekPulsa(self) :
        return "\nSisa Pulsa Anda Sekarang Sejumlah Rp%d\n\n" % InternetServiceProvider.myPulsa

    #Deklarasi fungsi cek saldo (client)
    def cekSaldo(self, nominalBeliISP) :
        c = zerorpc.Client()
        c.connect("tcp://127.0.0.1:2000")
        saldo = c.checkSaldo()
        return "\nSisa Saldo E-Money Anda Sekarang Sejumlah Rp%d\n\n" % saldo

#Deklarasi handle_thread
def handle_thread(conn):
    try :
        while True :
            # Receive data dari client
            data = conn.recv(100)
            data = data.decode('ascii')
            data = "OK "+data
            # Kirim balik ke client
            conn.send(data.encode('ascii'))
    except (socket.error, KeyboardInterrupt):
        conn.close()
        print("Client menutup koneksi")

#Deklarasi program sebagai server
try :
    s = zerorpc.Server(InternetServiceProvider())
    s.bind("tcp://0.0.0.0:2001")
    s.run()
    # Terima permintaan koneksi
    conn, client_addr = sock.accept()
    # Buat thread baru setiap ada permintaan koneksi dari client
    clientThread = threading.Thread(target=handle_thread, args=(conn,))
    clientThread.start()
except KeyboardInterrupt:
    print("Keluar")