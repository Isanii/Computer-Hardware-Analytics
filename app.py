from flask import Flask

from routes.home import home_bp
from routes.products import product_bp
from routes.search import search_bp
from routes.benchmarks import benchmark_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(product_bp)
app.register_blueprint(search_bp)
app.register_blueprint(benchmark_bp)
app.register_blueprint(dashboard_bp)
if __name__ == "__main__":
    app.run(debug=True)