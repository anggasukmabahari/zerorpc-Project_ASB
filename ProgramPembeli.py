import zerorpc
import socket
import threading

#Deklarasi client RPC
c = zerorpc.Client()
c.connect("tcp://127.0.0.1:2001")

while True: #Infinite Loop
    print ("===== SUNDA EMPIRE CELL =====\n")
    print ("1. Beli Pulsa")
    print ("2. Cek Pulsa")
    print ("3. Cek Saldo\n")
    opsiMenu = input("Pilih Opsi Menu Kamu (Angka) : ")
    nominalPembelian = 0
    #Pemilihan Menu Beli Pulsa
    if opsiMenu == str(1):
        nominalPembelian = int(input("\nMasukkan Nominal Pembelian : Rp"))    
        print(c.quotaAvailable(nominalPembelian))
    #Pemilihan Menu Cek Pulsa
    elif opsiMenu == str(2):
        print(c.cekPulsa())
    #Pemilihan Menu Cek Saldo
    elif opsiMenu == str(3):
        print(c.cekSaldo(nominalPembelian))
    
    else :
       print ("Harap Masukkan Opsi dengan Benar!")

