import os

from flask import Flask, request
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler

from models import db, Video
from utils import youtube_search

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db.init_app(app)
migrate = Migrate(app, db)


def refresh_data(query: str, do_refresh: bool):
    with app.app_context():
        if do_refresh:
            youtube_search(query)


scheduler = BackgroundScheduler()
scheduler.add_job(refresh_data, trigger='interval',
                  hours=float(os.environ.get('REFRESH_INTERVAL')),
                  args=[os.environ.get('SEARCH_QUERY'),
                        bool(os.environ.get('REFRESH_ENABLED', False))])
scheduler.start()


@app.route('/refresh')
def refresh():
    query = request.args.get('query', os.environ.get('SEARCH_QUERY'))
    refresh_data(query, True)
    return '', 200


@app.route('/videos')
def get_videos():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    results = Video.query.order_by(Video.published_at.desc()).paginate(page=page, per_page=limit)
    videos = [{
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'published_at': video.published_at,
        'thumbnail': video.thumbnail
    } for video in results.items]

    return {
        'data': videos,
        'metadata': {
            'pages': results.pages,
            'limit': results.per_page,
            'count': results.total,
        }
    }


@app.route('/videos/search')
def search_videos():
    query = request.args.get('query', '')
    results = Video.query.filter(Video.__ts_vector__.match(query))
    return [{
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'published_at': video.published_at,
        'thumbnail': video.thumbnail
    } for video in results]


if __name__ == '__main__':
    app.run()
