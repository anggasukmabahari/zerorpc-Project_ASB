import zerorpc
import socket
import threading

# Inisiasi socket TCP/IPv4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Kelas sebagai rujukan Server
class Payment(object):
    saldo = 100000 #Deklarasi Saldo sebagai object
    
    #Deklarasi fungsi untuk transaksi
    def pembelian(self, nominalBeli):
        #Jika True, melanjutkan pembayaran dan uang admin Rp2000
        if Payment.saldo >= nominalBeli:
            Payment.saldo = Payment.saldo - (nominalBeli + 2000)
            return True
        #Jika False, Tidak melanjutkan pembayaran
        elif nominalBeli > Payment.saldo:
           return False

    #Dekrlarasi fungsi mengecek Saldo
    def checkSaldo(self) :
        return Payment.saldo

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
    s = zerorpc.Server(Payment())
    s.bind("tcp://0.0.0.0:2000")
    s.run()
    # Terima permintaan koneksi
    conn, client_addr = sock.accept()
    # Buat thread baru setiap ada permintaan koneksi dari client
    clientThread = threading.Thread(target=handle_thread, args=(conn,))
    clientThread.start()
except KeyboardInterrupt:
    print("Keluar")