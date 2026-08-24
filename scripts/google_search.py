#!/usr/bin/env python3
import argparse
from personal_assistant.browser_search import search

ap=argparse.ArgumentParser(); ap.add_argument('query'); args=ap.parse_args()
print(search(args.query))
