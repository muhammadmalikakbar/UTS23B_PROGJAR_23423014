import socket

def konek_ke_server(ip, port, timeout_connect):
    """Mencoba connect ke server dengan timeout tertentu."""
    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli.settimeout(timeout_connect)

    try:
        cli.connect((ip, port))
        print(f"[INFO] Terhubung ke server {ip}:{port}")
        return cli
    except socket.timeout:
        print("Koneksi timeout! (saat mencoba connect)")
        return None
    except Exception as e:
        print(f"[ERROR] Gagal connect: {e}")
        return None


def baca_data(sock, timeout_read):
    """Membaca data dari server dengan timeout."""
    sock.settimeout(timeout_read)

    try:
        data = sock.recv(1024)
        if data:
            print("[DATA DITERIMA]", data.decode())
    except socket.timeout:
        print("Koneksi timeout! (saat membaca data)")
    except Exception as e:
        print(f"[ERROR] Gagal membaca data: {e}")


def main():
    IP = "127.0.0.1"
    PORT = 5050

    # 1. Timeout saat connect = 3 detik
    client_socket = konek_ke_server(IP, PORT, 3)

    if client_socket is None:
        return  # berhenti kalau gagal connect

    # Kirim pesan ke server (opsional)
    try:
        client_socket.sendall(b"Tes Koneksi dari client timeout v2")
    except:
        print("[ERROR] Gagal mengirim pesan")
        return

    # 2. Timeout saat membaca data = 2 detik
    baca_data(client_socket, 2)

    # Tutup koneksi
    try:
        client_socket.close()
    except:
        pass


if __name__ == "__main__":
    main()