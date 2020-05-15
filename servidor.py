"""Servidor FTP básico com um usuário virtual, com configuração de limite de conexões e portas.
"""

# Comando para instalação da biblioteca que utilizaremos para criar o servidor
# pip install pyftpdlib 
#Site da biblioteca
# https://pyftpdlib.readthedocs.io/en/latest/tutorial.html

#Limitador de taxa de leitura e escrita
LIMITE_LEITURA = 1*1024 # 30 Kb/sec (30 * 1024)
LIMITE_ESCRITA = 1*1024 # 30 Kb/sec (30 * 1024)

#limite para o tamanho do buffer
LIMITE_INBUFFER = 65536
LIMITE_OUTBUFFER = 65536

import logging

from pyftpdlib.handlers import FTPHandler,ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer


class MyHandler(FTPHandler):
    """Manipula os eventos para geração dos históricos e dados"""
    def log_transfer(self, cmd, filename, receive, completed, elapsed, bytes):
        # Registra estatisticas ao enviar um arquivo
        with open('resultados.txt', 'a') as f:
            f.write(str(cmd))
            f.write(",")
            f.write(str(LIMITE_LEITURA))
            f.write(",")
            f.write(str(LIMITE_ESCRITA))
            f.write(",")
            f.write(",")
            f.write(str(LIMITE_INBUFFER))
            f.write(",")
            f.write(str(LIMITE_OUTBUFFER))
            f.write(",")
            f.write(str(elapsed))
            f.write(",")
            f.write(str(bytes))
            f.write("\n")
        print("Log")
        pass
    def on_login(self,username):
        tx_l = int(username.split('_')[1])
        tx_e = int(username.split('_')[2])
        LIMITE_LEITURA = tx_l*1024
        LIMITE_ESCRITA = tx_e*1024 
        
        buf_in = int(username.split('_')[3])
        LIMITE_INBUFFER = buf_in
        buf_out = int(username.split('_')[4])
        LIMITE_OUTBUFFER = buf_out
        
        self.dtp_handler.ac_in_buffer_size = LIMITE_INBUFFER
        self.dtp_handler.ac_out_buffer_size = LIMITE_OUTBUFFER

        self.dtp_handler.read_limit = LIMITE_LEITURA
        self.dtp_handler.write_limit = LIMITE_ESCRITA
        pass

def main():
    """ Função principal"""

    authorizer = DummyAuthorizer()
    #Padrão para usuários
    #user_A_B_C_D
    #Onde
    # A -> Limite Leitura
    # B -> Limite Escrita
    # C -> Tamanho do buffer de Entrada
    # D -> Tamanho do buffer de Saida
    
    #Exemplo
    authorizer.add_user('user_30_30_65536_65536', '12345', homedir='.', perm='elradfmwMT')
    
    handler = MyHandler
    handler.authorizer = authorizer
    # Mensagem de boas vindas
    handler.banner = "##### Ola! Bem vindo ao Meu FTP.####"
    address = ('', 2121)
    
    dtp_handler = ThrottledDTPHandler
    dtp_handler.read_limit = LIMITE_LEITURA  
    dtp_handler.write_limit = LIMITE_ESCRITA 
    
    handler.dtp_handler = dtp_handler
    
    logging.basicConfig(level=logging.DEBUG)

    server = FTPServer(address, handler)
        
    # Limite de conexões
    server.max_cons = 50
    server.max_cons_per_ip = 5

    server.serve_forever()

if __name__ == "__main__":
    main()