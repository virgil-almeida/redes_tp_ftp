from ftplib import FTP

host = 'localhost'
port = 2121
usr = 'user_30_30_65536_65536'
pwd = '12345'
ftp = FTP()

ftp.connect(host, port)

ftp.login(usr, pwd)

ftp.nlst()

print(ftp.getwelcome())

with open('ti.png', 'wb') as fp:
    ftp.retrbinary('RETR i.png', fp.write)

ftp.quit()