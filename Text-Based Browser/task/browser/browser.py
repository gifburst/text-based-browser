# Text-Based Browser
# Author: Jason Tolbert (https://github.com/jasonalantolbert)
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
    history = deque()  # creates a deque to hold the browser history
    while True:
        # gets a url from the user, stripping the protocol identifier if present
        url = re.sub("^http[s]?[:]//", "", input("\nEnter a URL to browse, 'back' to go back, or 'exit' to exit:\n"))

        if url == "exit":
            exit()
        elif url == "back":  # goes back to the previous page
            try:
                history[-2]  # checks if there's a previous page to go back to
            except IndexError:
                url = None  # if there isn't, the url is set to None
            else:  # if there is, the url is set to penultimate value in history
                history.pop()
                url = history.pop()

        if url:  # will not run if url is None, i.e. if the user tried to back but there wasn't a page to go back to
            try:
                site = requests.get(f"https://{url}")
                soup = BeautifulSoup(site.content, "lxml")
                # opens (or creates if nonexistent) a new file in the tabs folder with the same name as the url minus
                # the protocol identifier and top-level-domain (e.g. for the url https://google.com, the file name
                # would be "google")
                #
                # these files function as the browser's tabs and can be opened by simply typing the site name
                # instead of the url (e.g. once https://google.com has been saved in a tab, it can be loaded again
                # by typing only "google")
                with open(f"{tab_directory}/{re.sub('.[a-z]+$', '', url)}", "w+") as site_file:
                    for element in soup.find_all(re.compile("p|a|ul|ol|li|^h[1-6]$")):
                        # this for loop finds all elements in the page with any of a limited range of HTML tags
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
                # trying to open an existing tab will cause an exception
                # with requests.get(), so if one occurs the program check to see if
                # there's an existing tab with a name that matches the user input
                try:
                    with open(f"{tab_directory}/{url}", "r") as site_file:
                        print(site_file.read())
                    history.append(url)
                except BaseException:  # if no existing tab can be found the user input an error message is printed
                    print("Error: Incorrect URL")


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
