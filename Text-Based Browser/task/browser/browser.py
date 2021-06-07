# Squirrel-Navigator
# Author: squirrelcom (https://github.com/squirrelcom)
# Python Version: 3.8


# BEGINNING OF PROGRAM


# import statements
import re
import os
import argparse
import requests
import colorama
from collections import deque
from bs4 import BeautifulSoup


def browse(tab_directory):  # contains all functions of the browser
    history = deque()
    while True:
        url = re.sub("^http[s]?[:]//", "", input("\nWelcome to Squirrel-Navigator!! Enter a URL to browse, 'back' to go back, or 'exit' to exit:\n"))

        if url == "exit":
            exit()
        elif url == "back":
            try:
                history[-2]
            except IndexError:
                url = None  # if there isn't, the url is set to None
            else:  # if there is, the url is set to penultimate value in history
                history.pop()
                url = history.pop()

        if url:  # will not run if url is None, i.e. if the user tried to back but there wasn't a page to go back to
            try:
                site = requests.get(f"https://{url}")
                soup = BeautifulSoup(site.content, "lxml")
                with open(f"{tab_directory}/{re.sub('.[a-z]+$', '', url)}", "w+") as site_file:
                    for element in soup.find_all(re.compile("p|a|ul|ol|li|^h[1-6]$")):
                        if element.name == "a":  # makes hyperlink text blue
                            print(colorama.Fore.BLUE + element.get_text())
                            print(colorama.Style.RESET_ALL)
                            site_file.write(f"{colorama.Fore.BLUE + element.get_text()}\n")
                            site_file.write(f"{colorama.Style.RESET_ALL}\n")
                        else:
                            print(element.get_text())
                            site_file.write(f"{element.get_text()}\n")
                history.append(re.sub('.[a-z]+$', '', url))  # appends site name to history
            except BaseException:
                try:
                    with open(f"{tab_directory}/{url}", "r") as site_file:
                        print(site_file.read())
                    history.append(url)
                except BaseException:  # if no existing tab can be found the user input an error message is printed
                    print("Error: No website with that URL")


# command line argument parsing

parser = argparse.ArgumentParser()
cli_args = ["tabdir"]

for argument in cli_args:
    parser.add_argument(argument)

args = parser.parse_args()


# if nonexistent, creates a folder with a user-specified name in which to save tabs
if not os.path.exists(args.tabdir):
    os.mkdir(args.tabdir)

browse(args.tabdir)  # runs the browser
