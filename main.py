import sys
from crawler import LinkCrawl, DataCrawl

if __name__ == "__main__":
    switch = sys.argv[1]
    if switch == "link":
        LinkCrawl().start()
    elif switch == "data":
        DataCrawl().start()
    else:
        print("Invalid switch")
