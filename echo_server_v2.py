import socket

def start_server(host="0.0.0.0", port=5050):
    print(f"[INFO] Server berjalan di port {port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.bind((host, port))
        srv.listen()

        print("[INFO] Menunggu koneksi client...")

        conn, addr = srv.accept()
        with conn:
            print(f"[CONNECTED] Client dari {addr}")

            while True:
                data = conn.recv(1024)
                if not data:
                    print("[INFO] Client terputus")
                    break

                pesan = data.decode()
                print(f"[RECV] {pesan}")

                # Kirim kembali (echo)
                conn.sendall(data)


if __name__ == "__main__":
    start_server()