import socket
import threading


class ChatServer:
    def __init__(self, host="0.0.0.0", port=5050):
        self.host = host
        self.port = port
        self.server_socket = None

        # list berisi dict: {"sock": socket, "addr": addr, "name": name}
        self.clients = []
        self.lock = threading.Lock()

    def start(self):
        """Mulai server dan listen koneksi."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bisa reuse port kalau server restart cepat
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print(f"[SERVER] Chat server aktif di {self.host}:{self.port}")
        print("[SERVER] Menunggu client terhubung...\n")

        try:
            while True:
                conn, addr = self.server_socket.accept()
                print(f"[SERVER] Koneksi baru dari {addr}")

                # Buat thread untuk client baru
                t = threading.Thread(target=self.handle_client, args=(conn, addr))
                t.daemon = True
                t.start()
        except KeyboardInterrupt:
            print("\n[SERVER] Dimatikan oleh user.")
        finally:
            self.shutdown()

    def handle_client(self, conn, addr):
        """Menangani 1 client (dijalankan di thread terpisah)."""
        try:
            conn.sendall(b"Masukkan nickname: ")
            nickname_data = conn.recv(1024)
            if not nickname_data:
                conn.close()
                return

            nickname = nickname_data.decode().strip()
            if nickname == "":
                nickname = f"user_{addr[1]}"

            # Simpan client
            with self.lock:
                self.clients.append({"sock": conn, "addr": addr, "name": nickname})

            join_msg = f"[INFO] {nickname} bergabung ke chat.\n"
            print(join_msg.strip())
            self.broadcast(join_msg, sender=None)

            # Loop terima pesan
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                text = data.decode().strip()
                if text == "":
                    continue

                # Pesan keluar di server
                print(f"[CHAT] {nickname}: {text}")

                # Broadcast ke client lain
                kirim = f"[{nickname}] {text}\n"
                self.broadcast(kirim, sender=conn)

        except ConnectionResetError:
            print(f"[SERVER] Koneksi terputus tiba-tiba dari {addr}")
        finally:
            # Hapus client dari list
            self.remove_client(conn)

    def broadcast(self, message, sender=None):
        """Kirim pesan ke semua client, kecuali pengirim (sender)."""
        with self.lock:
            dead_clients = []
            for c in self.clients:
                sock = c["sock"]
                if sock is sender:
                    continue
                try:
                    sock.sendall(message.encode() if isinstance(message, str) else message)
                except:
                    # kalau gagal kirim, tandai untuk dihapus
                    dead_clients.append(sock)

            # hapus client yang sudah mati koneksinya
            for dc in dead_clients:
                self.remove_client(dc)

    def remove_client(self, conn):
        """Menghapus client dari list jika disconnect."""
        with self.lock:
            target = None
            for c in self.clients:
                if c["sock"] is conn:
                    target = c
                    break

            if target:
                self.clients.remove(target)
                nama = target["name"]
                addr = target["addr"]
                print(f"[SERVER] {nama} ({addr}) keluar dari chat.")
                leave_msg = f"[INFO] {nama} meninggalkan chat.\n"
                self.broadcast(leave_msg, sender=None)

        try:
            conn.close()
        except:
            pass

    def shutdown(self):
        """Matikan server dan tutup semua koneksi."""
        with self.lock:
            for c in self.clients:
                try:
                    c["sock"].close()
                except:
                    pass
            self.clients.clear()

        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        print("[SERVER] Shutdown selesai.")


if __name__ == "__main__":
    server = ChatServer(port=5050)
    server.start()