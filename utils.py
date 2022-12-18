import os

from googleapiclient.discovery import build

from models import Video, db
from datetime import datetime, date

DEVELOPER_KEY = os.environ.get('DEVELOPER_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

YOUTUBE = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)


def __get_start_timestamp():
    dt = datetime.combine(date(date.today().year, date.today().month, 1), datetime.min.time())
    return dt.isoformat('T') + 'Z'


def youtube_search(query: str, page_token: str = None):
    print(f"Querying YouTube Search\tQuery:{query}\tToken:{page_token}")
    try:
        search_response = YOUTUBE.search().list(
            q=query,
            part='id,snippet',
            order='date',
            pageToken=page_token,
            maxResults=50,
            type='video',
            publishedAfter=__get_start_timestamp()
        ).execute()
    except Exception as e:
        print("YouTube API Error", e)
        return

    for search_result in search_response.get('items', []):
        video = convert_to_object(search_result)
        try:
            db.session.add(video)
        except Exception as e:
            print("Database Insert Error", e)
            return
    db.session.commit()
    if search_response.get('nextPageToken') is not None:
        return youtube_search(query, search_response.get('nextPageToken'))


def convert_to_object(item: dict) -> Video:
    return Video(id=item['id']['videoId'],
                 title=item['snippet']['title'],
                 description=item['snippet']['description'],
                 published_at=item['snippet']['publishTime'],
                 thumbnail=item['snippet']['thumbnails']['default']['url'])
