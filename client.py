import socket
import threading
import os
import sys

# --- Platform Specific Key Reading ---
if os.name == 'nt': # Windows
    import msvcrt
    def get_char():
        # Read a wide character (Unicode)
        return msvcrt.getwch()
else: # Linux/Mac
    import tty, termios
    def get_char():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# --- Colors Class ---
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    CLEAR_LINE = "\033[K" # ANSI code to clear text from cursor to end of line

class ClientProgram:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.input_buffer = "" # Stores what you are currently typing
        self.prompt_text = f"{Colors.BLUE}{self.username}{Colors.RESET}: "
        
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print(f"{Colors.GREEN}[CLIENT] Connected to {self.host}:{self.port}{Colors.RESET}")
            
            # Send Handshake
            self.sock.sendall(f"{self.username}:joined".encode())

            # Start listening thread
            threading.Thread(target=self.listen_for_messages, daemon=True).start()
            
            # Start sending loop (Main Thread)
            self.send_messages()
            
        except ConnectionRefusedError:
            print(f"{Colors.RED}Could not connect to server.{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Exiting...{Colors.RESET}")
            sys.exit()

    def listen_for_messages(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    print(f"\n{Colors.RED}[SERVER] Disconnected unexpectedly.{Colors.RESET}")
                    os._exit(0)
                
                message = data.decode(errors="ignore")
                
                # Handle Shutdown
                if "[Server] Shutting Down!" in message:
                    print(f"\r{Colors.CLEAR_LINE}", end="") # Clear line
                    print(f"{Colors.RED}{Colors.BOLD}{message}{Colors.RESET}")
                    print(f"{Colors.YELLOW}Press Enter to exit...{Colors.RESET}")
                    os._exit(0)
                
                # --- THE FIX IS HERE ---
                # 1. \r moves cursor to start of line
                # 2. Colors.CLEAR_LINE wipes everything on that line (your partial input)
                # 3. Print the incoming message
                # 4. Reprint your prompt AND the buffer you were typing
                if message.count(":") == 0 and message.endswith("has left the chat."):
                    print(f"\r{Colors.CLEAR_LINE}{Colors.YELLOW}{message}{Colors.RESET}")
                else:
                    print(f"\r{Colors.CLEAR_LINE}{Colors.CYAN}{message}{Colors.RESET}")
                print(f"{self.prompt_text}{self.input_buffer}", end="", flush=True)
                
            except Exception:
                break

    def send_messages(self):
        while True:
            # We use a custom input function instead of built-in input()
            msg = self.custom_input(self.prompt_text)
            
            if msg is not None: # Ensure msg isn't empty/None
                try:
                    full_msg = f"{self.username}: {msg}"
                    self.sock.sendall(full_msg.encode())
                except:
                    self.sock.close()
                    break

    def custom_input(self, prompt):
        """
        A custom replacement for input() that updates self.input_buffer
        so the listening thread knows what to re-print.
        """
        print(prompt, end="", flush=True)
        self.input_buffer = "" # Reset buffer
        
        while True:
            ch = get_char()
            
            # 1. Handle Enter (Return)
            if ch == '\r' or ch == '\n':
                print() # Move to new line
                return self.input_buffer
            
            # 2. Handle Backspace (Windows='\x08', Unix='\x7f')
            elif ch == '\x08' or ch == '\x7f':
                if len(self.input_buffer) > 0:
                    # Remove last char from buffer
                    self.input_buffer = self.input_buffer[:-1]
                    # Visually delete: Move back, print space, move back
                    print("\b \b", end="", flush=True)
            
            # 3. Handle Ctrl+C (End of Text)
            elif ch == '\x03': 
                raise KeyboardInterrupt
            
            # 4. Handle Normal Characters
            else:
                # Only accept printable characters
                if ch.isprintable():
                    self.input_buffer += ch
                    print(ch, end="", flush=True)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    IP = input("Enter server IP: ") or "localhost"
    PORT = int(input("Enter server port: ") or 23901)
    Username = input("Enter your username: ")
    os.system('cls' if os.name == 'nt' else 'clear')

    ClientProgram(IP, PORT, Username)