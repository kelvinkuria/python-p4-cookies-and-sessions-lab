#!/usr/bin/env python3
from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    pass

@app.route('/articles/<int:id>')
def show_article(id):
    # Check if 'page_views' is set in the session or initialize it to 0
    session['page_views'] = session.get('page_views', 0)

    # Increment the page_views count
    session['page_views'] += 1

    # Check if the user has viewed more than 3 pages
    if session['page_views'] > 3:
        # Return a JSON response with an error message and a 401 status code
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    # If the user hasn't reached the limit, fetch and return the article data
    article = Article.query.get(id)
    return jsonify(article.to_dict())

if __name__ == '__main__':
    app.run(port=5555)
