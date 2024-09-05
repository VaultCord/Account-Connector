# Copyright © Nelson Cybersecurity LLC
# Founder of VaultCord.com and KeyAuth.win

# VaultCord account connector is licensed under Elastic License 2.0
# - You may not provide the software to third parties as a hosted or managed service, where the service provides users with access to any substantial set of the features or functionality of the software.
# - You may not move, change, disable, or circumvent the license key functionality in the software, and you may not remove or obscure any functionality in the software that is protected by the license key.
# - You may not alter, remove, or obscure any licensing, copyright, or other notices of the licensor in the software. Any use of the licensor’s trademarks is subject to applicable law.
# Thank you for your compliance, we work hard on the development of VaultCord and do not appreciate our copyright being infringed.

# https://github.com/VaultCord/Account-Connector
# https://youtube.com/@VaultCord
# https://t.me/vaultcode

import time
import os
import subprocess
import sys
from sys import exit
import json
import ctypes
import requests
import http.server
import socketserver
from colorama import Fore, init
from client_info import request_client, discord_build, discord_build_failback

colors = {
    "main_colour": Fore.MAGENTA,
    "light_red": Fore.LIGHTRED_EX,
    "yellow": Fore.YELLOW,
    "light_blue": Fore.LIGHTBLUE_EX,
    "green": Fore.LIGHTGREEN_EX,
    "white": Fore.WHITE,
}

def cleanup():
        print(f"Closing in 3 seconds..")
        time.sleep(3)
        current_executable = sys.argv[0]
        delete_command = f"Start-Sleep -Seconds 1; Remove-Item -Force \"{current_executable}\""
        subprocess.Popen(["powershell", "-Command", delete_command])
        # Execute self-delete so people don't use outdated version of program (if we have to update)
        exit()

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def version_string(self):
        """Return the server software version string."""
        return "VaultCord account connector"

    def log_message(self, format, *args):
        # Disable server request list from showing
        return

    def do_OPTIONS(self):
        """Respond to an OPTIONS request."""
        self.send_response(200, "OK")
        self.send_header("Allow", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Origin", "https://dash.vaultcord.com")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        """Respond to a POST request."""
        # Setting the headers
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "https://dash.vaultcord.com")
        self.end_headers()
        
        # JSON response
        response_content = {
            "success": True,
            "message": "Responded to POST request"
        }
        
        # Write the JSON response
        self.wfile.write(json.dumps(response_content).encode('utf-8'))

    def do_GET(self):
        import console
        c = console.prnt()

        referer = self.headers.get('Origin')
        if not referer:
            print("No referer specified, please try again")

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "https://dash.vaultcord.com")
            self.end_headers()

            # JSON response
            response_content = {
                "success": False,
                "message": "No referer specified"
            }
        
            # Write the JSON response
            self.wfile.write(json.dumps(response_content).encode('utf-8'))

            cleanup()
            return

        if referer and 'https://dash.vaultcord.com' not in referer:
             print("Invalid referer:", referer)
             print("Please try again")

             self.send_response(200)
             self.send_header("Content-type", "application/json")
             self.send_header("Access-Control-Allow-Origin", "https://dash.vaultcord.com")
             self.end_headers()
 
             # JSON response
             response_content = {
                 "success": False,
                 "message": f"Invalid referer: {referer}"
             }
         
             # Write the JSON response
             self.wfile.write(json.dumps(response_content).encode('utf-8'))

             cleanup()
             return

        # This will list Discord accounts you can use with VaultCord
        # Only our client-side dashboard sees the details and it's NOT saved in database, do not worry.
        # we require 2FA so it's only temporary access to make a bot.
        # Most people use alt accounts for VaultCord anyways so their bot is safe if their account gets deleted..

        # You can always use the --Manual-- option on our dashboard if that makes you more comfortable
        import fetch_details
        c.info(f"Scanning for accounts... Please wait a moment")
        tokens = fetch_details.fetch()
        if len(tokens) != 0:
            print()
            while True:
                c.info(f"Select which account you want to use for VaultCord:")
                for tkn in tokens:
                    print(f"{colors['white']}{tokens.index(tkn)}: {colors['main_colour']}{tkn[1]}{colors['white']} from {colors['main_colour']}{tkn[3]}")
                print()
                c.inp(f"Choice {colors['main_colour']}(int) """, end=colors['white'])
                try: tknchoice = int(input())
                except ValueError: c.fail(f"Invalid Choice. Please try again")
                else:
                    try:
                        token_selected = tokens[tknchoice]
                    except:
                        c.fail(f"Invalid Choice. Please try again")
                    else:
                        break
            c.success(f"Selected {colors['main_colour']}{token_selected[1]}")
            token_info = token_selected
        else:
            c.fail(f"No accounts found Please login to Discord and try again.")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "https://dash.vaultcord.com")
            self.end_headers()

            # JSON response
            response_content = {
                "success": False,
                "message": "No accounts found"
            }
        
            # Write the JSON response
            self.wfile.write(json.dumps(response_content).encode('utf-8'))
            cleanup()
            return

        print("SUCCESS - Check the VaultCord dashboard")
        print(f"{colors['yellow']}Check the VaultCord dashboard!{colors['white']}")

        # Setting the headers
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "https://dash.vaultcord.com")
        self.end_headers()
        
        # JSON response
        response_content = {
            "success": True,
            "token": token_info[0]
        }
        
        # Write the JSON response
        self.wfile.write(json.dumps(response_content).encode('utf-8'))

        cleanup()

if __name__ == '__main__':
    with socketserver.TCPServer(("localhost", 53628), CustomHTTPRequestHandler) as httpd:
        print('Waiting for VaultCord dashboard to complete..')
        print('ONLY download this program from github.com/VaultCord')
        try: ctypes.windll.kernel32.SetConsoleTitleW(f"VaultCord automatic setup")
        except: pass
        init(autoreset=True)
        httpd.serve_forever()
