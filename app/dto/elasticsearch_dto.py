from flask_restx import Namespace


class ElasticsearchDto:
    api = Namespace('Elasticsearch', description="Elasticsearch")
