# WEB应用程序：遵循HTTP协议

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 5173))  # 正确写法
server_socket.listen(5)
print("服务器已启动，监听端口 5173...")


try:
    while True:
        conn, addr = server_socket.accept()  # 阻塞等待客户端连接
        data = conn.recv(1024)
        print(f"客户端发送的请求信息：\n{data}")
        conn.send(
            b'HTTP/1.1 200 ok\r\nserver:lee\r\ncontent-type:application/json\r\n\r\n{"user_id": 1001}'
        )
        conn.close()
except Exception as e:
    print(e)
finally:
    server_socket.close()
