import re
import argparse
import sys
import urllib.request
from html.parser import HTMLParser

__author__ = "Yaseen Al-Salamy"


search_text = ""


class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        global search_text
        search_text += data


def find_urls(text):
    url_pattern = re.compile(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|/[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    return url_pattern.findall(text)


def find_emails(text):
    email_pattern = re.compile(
        r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    return email_pattern.findall(text)


def find_numbers(text):
    num_pattern = re.compile(
        r"1?[^\w\t]?[2-9][0-8][0-9]\W?[2-9][0-9]{2}\W?[0-9]{4}")
    return num_pattern.findall(text)


def create_parser(args):
    parser = argparse.ArgumentParser(description="Input a url to scrape")
    parser.add_argument("url", help="website url you want to scrape")
    parser.add_argument(
        "-u", "--urls", action="store_true", help="scrape urls")

    parser.add_argument(
        "-e", "--emails", action="store_true", help="scrape emails")

    parser.add_argument("-n", "--numbers", action="store_true",
                        help="scrape US phone numbers")

    return parser.parse_args(args)


def print_scrapes(results, description=None):
    if description:
        print(description, end="\n\n")
    if not results:
        print("None")
    for value in results:
        print(value)
    print()


def main(args):
    ns = create_parser(args)
    req = urllib.request.Request(ns.url,
                                 headers={
                                     'User-Agent': 'Mozilla/5.0'
                                 })
    response = urllib.request.urlopen(req).read().decode("utf-8")
    MyHTMLParser().feed(response)
    if not ns.urls and not ns.emails and not ns.numbers:
        print("Default: Scraps All")
        print_scrapes(find_urls(search_text), description="URLS:")
        print_scrapes(find_emails(search_text), description="EMAILS:")
        print_scrapes(find_numbers(search_text), description="NUMBERS:")
    if ns.urls:
        print_scrapes(find_urls(search_text), description="URLS:")
    if ns.emails:
        print_scrapes(find_emails(search_text), description="EMAILS:")
    if ns.numbers:
        print_scrapes(find_numbers(search_text), description="NUMBERS:")

    pass


if __name__ == "__main__":
    main(sys.argv[1:])
