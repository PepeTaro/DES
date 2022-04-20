import sys
sys.path.insert(1,'../rsa')
sys.path.insert(1,'../des')

import number_theory
import rsa
import des
import random

from PyQt5 import QtWidgets, uic

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('app.ui', self)
        self.init_buttons()
        self.show() 
        
    def init_buttons(self):        
        self.gen_asymkey_pushButton = self.findChild(QtWidgets.QPushButton,'gen_asymkey_pushButton')
        self.gen_asymkey_pushButton.clicked.connect(self.gen_asymkey)

        
        self.pubkey_send_pushButton = self.findChild(QtWidgets.QPushButton,'pubkey_send_pushButton')
        self.pubkey_send_pushButton.clicked.connect(self.pubkey_send)
        
        self.dec_symkey_pushButton = self.findChild(QtWidgets.QPushButton,'dec_symkey_pushButton')
        self.dec_symkey_pushButton.clicked.connect(self.dec_symkey)
        
        self.symkey_send_pushButton = self.findChild(QtWidgets.QPushButton,'symkey_send_pushButton')
        self.symkey_send_pushButton.clicked.connect(self.symkey_send)
        
        self.gen_symkey_pushButton = self.findChild(QtWidgets.QPushButton,'gen_symkey_pushButton')
        self.gen_symkey_pushButton.clicked.connect(self.gen_symkey)
        
        self.enc_symkey_pushButton = self.findChild(QtWidgets.QPushButton,'enc_symkey_pushButton')
        self.enc_symkey_pushButton.clicked.connect(self.enc_symkey)
        
        self.enc_pushButton = self.findChild(QtWidgets.QPushButton,'enc_pushButton')
        self.enc_pushButton.clicked.connect(self.enc)
        
        self.message_send_pushButton = self.findChild(QtWidgets.QPushButton,'message_send_pushButton')
        self.message_send_pushButton.clicked.connect(self.message_send)
        
        self.dec_pushButton = self.findChild(QtWidgets.QPushButton,'dec_pushButton')
        self.dec_pushButton.clicked.connect(self.dec)
        
        
    def gen_asymkey(self):
        [(n,e),(d,p,q)] = rsa.generate_keys256()        
        self.n = n
        self.e = e
        self.d = d
        self.p = p
        self.q = q
        
        pubkey_str = "("+hex(self.n)+","+hex(self.e)+")"
        privkey_str = "("+hex(self.d)+","+hex(self.p)+","+hex(self.q)+")"

        self.pubkey_left_lineEdit.setText(pubkey_str)
        self.privkey_left_lineEdit.setText(privkey_str)

    def pubkey_send(self):
        pubkey_str = "("+hex(self.n)+","+hex(self.e)+")"
        self.pubkey_right_lineEdit.setText(pubkey_str)

    def gen_symkey(self):
        self.key = random.randrange(0,2**64)
        self.IV = random.randrange(0,2**64)        
        self.symkey_right_lineEdit.setText(hex(self.key))
        
    def enc_symkey(self):                
        self.enc_key = rsa.encrypt(self.key,self.n,self.e)# IVは暗号化しない。
        self.enc_symkey_right_lineEdit.setText(hex(self.enc_key))
        
    def dec_symkey(self):
        dec_key = rsa.decrypt(self.enc_key,self.n,self.d)
        self.dec_symkey_left_lineEdit.setText(hex(dec_key))

    def symkey_send(self):
        self.symkey_left_lineEdit.setText(hex(self.enc_key))

    def enc(self):
        b_key = "{:064b}".format(self.key)
        b_IV = "{:064b}".format(self.IV)
        
        plaintext = self.plain_left_plainTextEdit.toPlainText()
        self.ciphertext = des.enc(plaintext,b_key,b_IV)        
        self.cipher_left_plainTextEdit.setPlainText(des.ascii_decode(self.ciphertext))
        
    def dec(self):
        b_key = "{:064b}".format(self.key)
        b_IV = "{:064b}".format(self.IV)

        ciphertext = self.cipher_right_plainTextEdit.toPlainText()
        plaintext = des.dec(self.ciphertext,b_key,b_IV)
        self.plain_right_plainTextEdit.setPlainText(plaintext)
    
    def message_send(self):
        ciphertext = self.cipher_left_plainTextEdit.toPlainText()
        self.cipher_right_plainTextEdit.setPlainText(ciphertext)

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
