#БЛОК ИМПОРТОВ
import socket, os
import datetime

#БЛОК ФУНКЦИЙ


#БЛОК САМОЙ ПРОГРАММЫ
sock = socket.socket()

try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen(5)

workdir = os.getcwd()




while True:
	conn, addr = sock.accept()
	print("Connected", addr)

	#получаем запрос
	data = conn.recv(8192)
	msg = data.decode()

	print(msg)

	#-dirname
	dirname = os.getcwd()
	request = msg.split()[1][1:] #запрос начинается с get далее следует путь к нужному файлу, начинающийся с /
	resp_file = ""
	text_types = ['html', 'css', 'txt']
	image_types =  ['png', 'jpeg','gif']

	if (msg.split()[1] == '/'):
		with open(os.path.join(dirname,'index.html'),'r', encoding='UTF-8') as f:
			resp_file = f.read()
		code = "200 OK"
		c_type = "text/html"
		c_len = len(resp_file)
	else:
		if os.path.exists(os.path.join(dirname, request)):
			tp = request.split('.')[1]
			if tp in text_types or tp in image_types:
				with open(os.path.join(dirname,request),'r', encoding='UTF-8') as f: #NE TAK KAK U IGORYA
					resp_file = f.read()
				code = "200 OK"
				c_len = len(resp_file)
				if tp in text_types:
					c_type = 'text/'+tp
				else:
					c_type = 'image/'+tp
			else:
				code = "403 Forbidden"

	#формируем заголовки
	date = str(datetime.datetime.now())

	if code = "200 OK":
		header = """HTTP/1.1 {0}
		Server: SelfMadeServer v0.0.1
		Date: {1}
		Content-type: {2}
		Content-length: {3}
		Connection: close
		""".format(code, date, c_type, c_len)
	else:
		header = """HTTP/1.1 {0}
		Server:
		Date: {1}""".format(code, date)

	responce = header + resp_file

	conn.send(responce.encode())

conn.close()