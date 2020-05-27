from news.new_vision import NewVision
from news.daily_monitor import DailyMonitor
# import pymongo

# client = pymongo.MongoClient()
# news_db = client["ug_news"]
# news_col = news_db["news"]
# news_db.news.create_index([('slug', pymongo.ASCENDING)], unique=True)

new_vision = NewVision()
daily_monitor = DailyMonitor()

print(new_vision.fetch_news())
print(daily_monitor.fetch_news())

# news_col.insert_many(nv_news_data)
