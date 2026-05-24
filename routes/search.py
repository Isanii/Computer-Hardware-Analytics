from flask import Blueprint
from flask import render_template
from flask import request

from services.search_service import (
    SearchService
)

search_bp = Blueprint(
    "search",
    __name__
)

service = SearchService()


@search_bp.route(
    "/search"
)
def search():

    keyword = request.args.get(
        "q",
        ""
    )

    products = []

    if keyword:

        products = (
            service.search_products(
                keyword
            )
        )

    return render_template(

        "products/search.html",

        products=products,

        keyword=keyword
    )