import socket

def main(server_ip="127.0.0.1", port=5050):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
        cli.connect((server_ip, port))
        print("[INFO] Terhubung ke server")

        pesan = "Tes Koneksi"
        cli.sendall(pesan.encode())
        print(f"[SEND] {pesan}")

        balikan = cli.recv(1024).decode()
        print(f"[ECHO] {balikan}")


if __name__ == "__main__":
    main()