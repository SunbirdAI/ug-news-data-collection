import logging
import pymongo
from news import (
    NewVision, DailyMonitor, Observer
)

# Prepare the database client
client = pymongo.MongoClient()
news_db = client["ug_news"]
news_col = news_db["news"]
news_db.news.create_index([('slug', pymongo.ASCENDING)], unique=True)

new_vision = NewVision()
daily_monitor = DailyMonitor()
observer = Observer()

nv_news = new_vision.fetch_news()
dm_news = daily_monitor.fetch_news()
ob_news = observer.fetch_news()

# Print - temporary
print(nv_news)
print(dm_news)
print(ob_news)

# Set up logger in case of database insertion errors
logging.basicConfig(filename='example.log', level=logging.ERROR)

# Insert into MongoDB database
try:
    news_col.insert_many(nv_news)
    news_col.insert_many(dm_news)
    news_col.insert_many(ob_news)
except pymongo.bulk.BulkWriteError as bwe:
    for err in bwe.details['writeErrors']:
        if int(err['code']) == 11000:
            pass
        else:
            logging.error(err['errmsg'])
