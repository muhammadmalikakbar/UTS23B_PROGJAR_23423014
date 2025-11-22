import socket
import threading


class ChatClient:
    def __init__(self, host="127.0.0.1", port=5050):
        self.host = host
        self.port = port
        self.sock = None
        self.running = False

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.running = True

        # Terima prompt nickname dari server
        prompt = self.sock.recv(1024).decode()
        print(prompt, end="")

        nickname = input()
        if nickname.strip() == "":
            nickname = "Anon"

        self.sock.sendall(nickname.encode())

        print("\n[INFO] Terhubung ke chat. Ketik /quit untuk keluar.\n")

        # Thread untuk menerima pesan dari server
        t = threading.Thread(target=self.receive_loop)
        t.daemon = True
        t.start()

        # Loop kirim pesan
        while self.running:
            try:
                msg = input("> ")
                if msg.lower() == "/quit":
                    self.running = False
                    break
                if msg.strip() == "":
                    continue
                self.sock.sendall(msg.encode())
            except (KeyboardInterrupt, EOFError):
                self.running = False
                break

        try:
            self.sock.close()
        except:
            pass
        print("[INFO] Keluar dari chat.")

    def receive_loop(self):
        """Menerima pesan dari server terus-menerus."""
        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    print("\n[INFO] Koneksi ke server terputus.")
                    self.running = False
                    break
                print("\n" + data.decode(), end="")
                print("> ", end="", flush=True)
            except:
                self.running = False
                break


if __name__ == "__main__":
    client = ChatClient(host="127.0.0.1", port=5050)
    client.connect()