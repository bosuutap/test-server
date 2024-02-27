import socket, time, os, json

nodes = []
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
PORT = os.getenv("PORT", 6060)
server.bind("0.0.0.0", PORT)
print("Server is running\n")

while True:
    conn, client = server.accept()
    data = conn.recv(10*1024*1024)
    text = data.decode('utf-8', errors="replace")
    if text.startswith("//node//"):
        info = json.loads(text.replace("//node//", ""))
        prefix = info["prefix"]
        name = info["name"]
        node = {"name": name, "prefix": prefix, "ip": client}
        nodes.append(node)
        server.sendto(b'ACCEPTED', client)
        print(f"Máy chủ test {name}({prefix}) IP: {client} vừa kết nối\n")
    
    if text.startswith("//writer//"):
        writer = client
        os.environ["writer"] = writer
        info = json.loads(text.split("//writer//", ""))
        req = info["request"]
        if req == "nodes":
            if nodes:
                data = str(nodes).encode('utf-8', errors="replace")
            else:
                data = b'NO TEST SERVER'
            server.sendto(data, writer)
            print(f"Đã gửi danh sách máy chủ test cho Writer({writer})\n")
        
        if req == "speedtest":
            url = info["url"].encode('utf-8', errors="replace")
            req_node = info["node"]
            for node in nodes:
                if req_node == node["prefix"]:
                    server.sendto(url, node["ip"])
                    print(f"Đã gửi yêu cầu speedtest đến máy chủ test {node['name']}\n")
    
    if text.startswith("//result//"):
        print("Nhận được kết quả\n")
        writer = os.getenv("writer")
        data = text.replace("//result//", "").encode('utf-8', errors="replace")
        server.sendto(data, writer)
        print("Đã gửi kết quả\n")
        