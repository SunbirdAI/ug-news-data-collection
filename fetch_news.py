from news.new_vision import NewVision
from news.daily_monitor import DailyMonitor
from news.observer import Observer
import pymongo

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

# Insert into MongoDB database
news_col.insert_many(nv_news)
news_col.insert_many(dm_news)
news_col.insert_many(ob_news)
