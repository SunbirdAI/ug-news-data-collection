from news.new_vision import NewVision
from news.daily_monitor import DailyMonitor
# import pymongo

# client = pymongo.MongoClient()
# news_db = client["ug_news"]
# news_col = news_db["news"]
# news_db.news.create_index([('slug', pymongo.ASCENDING)], unique=True)

new_vision = NewVision()
daily_monitor = DailyMonitor()

# nv_news = new_vision.fetch_news()
dm_news = daily_monitor.fetch_news()

# print(nv_news)
print(dm_news)

# news_col.insert_many(nv_news)
# news_col.insert_many(dm_news)
