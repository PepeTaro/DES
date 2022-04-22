import sys
sys.path.insert(1,'../rsa')
sys.path.insert(1,'../des')

import number_theory
import rsa
import des
import random

from PyQt5 import QtWidgets,uic
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget,QMessageBox

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('app.ui', self)
        self.init_buttons()
        self.init_flags()
        self.init_error_popup()
        self.show() 

    def popup_error(self,message):
        self.error.setText(message)
        self.error.exec_()

    def init_error_popup(self):
        self.error = QMessageBox()
        self.error.setIcon(QMessageBox.Critical)
        self.error.setWindowTitle("エラー")
        
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

    def init_flags(self):        
        self.is_asymkey_generated = False
        self.is_asymkey_sent = False
        self.is_symkey_generated = False
        self.is_symkey_sent = False        
        self.is_symkey_encrypted = False
        self.is_symkey_decrypted = False
        self.is_message_encrypted = False
        self.is_message_sent = False
        
    def gen_asymkey(self):
        """
        公開鍵と秘密鍵を生成。
        """
        self.generate_asym_keys() # 多少時間がかかるため、スレッドを使用して鍵生成。
        
    def pubkey_send(self):
        """
        公開鍵を送信。
        """
        
        if(not self.is_asymkey_generated):
            self.popup_error("公開鍵が生成されていません。")
            return
        
        pubkey_str = "("+hex(self.n)+","+hex(self.e)+")"
        self.pubkey_right_lineEdit.setText(pubkey_str)

        # 公開鍵が送信されたことを示すフラグをオン。
        self.is_asymkey_sent = True

    def gen_symkey(self):
        """
        共通鍵を生成。
        """

        # HACK:共通鍵の乱数は高速に生成できると仮定してスレッドを使用しない。
        self.key = random.randrange(0,2**64)
        self.IV = random.randrange(0,2**64)        
        self.symkey_right_lineEdit.setText(hex(self.key))

        # 対称鍵が生成されたことを示すフラグをオン。
        self.is_symkey_generated = True
        
    def enc_symkey(self):
        """
        共通鍵を公開鍵で暗号化。
        """
        
        if(not self.is_asymkey_sent):
            self.popup_error("公開鍵が送信されていません。")
            return        
        elif(not self.is_symkey_generated):
            self.popup_error("共通鍵が生成されていません。")
            return

        self.enc_key = rsa.encrypt(self.key,self.n,self.e)# IVは暗号化しない。
        self.enc_symkey_right_lineEdit.setText(hex(self.enc_key))

        # 共通鍵が暗号化されたことを示すフラグをオン。
        self.is_symkey_encrypted = True
        
    def dec_symkey(self):
        """
        共通鍵を秘密鍵で復号化。
        """
        
        if(not self.is_symkey_sent):
            self.popup_error("共通鍵が送信されていません。")
            return        

        dec_key = rsa.decrypt(self.enc_key,self.n,self.d)
        self.dec_symkey_left_lineEdit.setText(hex(dec_key))

        # 共通鍵が復号化されたことを示すフラグをオン。
        self.is_symkey_decrypted = True
        
    def symkey_send(self):
        """
        暗号化された共通鍵を送信。
        """
        
        if(not self.is_symkey_encrypted):
            self.popup_error("共通鍵が暗号化されていません。")
            return
        
        self.symkey_left_lineEdit.setText(hex(self.enc_key))
        
        # 共通鍵が送信されたことを示すフラグをオン。
        self.is_symkey_sent = True
        
    def enc(self):
        """
        メッセージを共通鍵を使用して暗号化。
        """
                
        if(not self.is_symkey_decrypted):
            self.popup_error("共通鍵が復号化されていません。")
            return        
        
        b_key = "{:064b}".format(self.key)
        b_IV = "{:064b}".format(self.IV)
        
        plaintext = self.plain_left_plainTextEdit.toPlainText()
        self.ciphertext = des.enc(plaintext,b_key,b_IV)        
        self.cipher_left_plainTextEdit.setPlainText(des.ascii_decode(self.ciphertext))
        
        # メッセージが暗号化されたことを示すフラグをオン。
        self.is_message_encrypted = True
        
    def dec(self):
        """
        メッセージを共通鍵を使用して復号化。
        """
        
        if(not self.is_message_sent):
            self.popup_error("メッセージが送信されていません。")
            return

        b_key = "{:064b}".format(self.key)
        b_IV = "{:064b}".format(self.IV)

        ciphertext = self.cipher_right_plainTextEdit.toPlainText()
        plaintext = des.dec(self.ciphertext,b_key,b_IV)
        self.plain_right_plainTextEdit.setPlainText(plaintext)
    
    def message_send(self):
        """
        メッセージを送信。
        """
        
        if(not self.is_message_encrypted):
            self.popup_error("メッセージが暗号化されていません。")
            return

        ciphertext = self.cipher_left_plainTextEdit.toPlainText()
        self.cipher_right_plainTextEdit.setPlainText(ciphertext)

        # メッセージが送信されたことを示すフラグをオン。
        self.is_message_sent = True

    ### 以下スレッド関連のメソッド ###
        
    def signal_rsa_keys(self,keys):
        [(n,e),(d,p,q)] = keys
        self.n = n
        self.e = e
        self.d = d
        self.p = p
        self.q = q
        
        # lineEditに表示するために鍵を文字列に変換
        pubkey_str = "("+hex(self.n)+","+hex(self.e)+")"
        privkey_str = "("+hex(self.d)+","+hex(self.p)+","+hex(self.q)+")"

        # 上記の文字列を表示。
        self.pubkey_left_lineEdit.setText(pubkey_str)
        self.privkey_left_lineEdit.setText(privkey_str)

        # 非対称鍵が生成されたことを示すフラグをオン。
        self.is_asymkey_generated = True

    def generate_asym_keys(self):
        self.thread = QThread()
        self.worker = GenAsymkeysWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(self.signal_rsa_keys)

        self.thread.start()
        self.gen_asymkey_pushButton.setEnabled(False) # 生成ボタンを押せないようにする。
        self.thread.finished.connect(
            lambda: self.gen_asymkey_pushButton.setEnabled(True) # 終わったら生成ボタンを押せるようにする。
        ) 

class GenAsymkeysWorker(QObject):
    finished = pyqtSignal(list)
    def run(self):
        [(n,e),(d,p,q)] = rsa.generate_keys1024()
        self.finished.emit([(n,e),(d,p,q)])

def main():    
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()

if __name__ == '__main__':
    main()
