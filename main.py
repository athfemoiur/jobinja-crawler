import sys
from crawler import LinkCrawl, MongoDataCrawl, MysqlDataCrawler

if __name__ == "__main__":
    switch = sys.argv[1]
    if switch == "link":
        LinkCrawl().start()
    elif switch == "datamongo":
        MongoDataCrawl().start()
    elif switch == "datamysql":
        MysqlDataCrawler().start()
    else:
        print("Invalid switch")
