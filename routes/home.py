from flask import Blueprint
from flask import render_template

from services.home_service import (
    HomeService
)

home_bp = Blueprint(
    "home",
    __name__
)

service = HomeService()


@home_bp.route("/")
def home():

    latest_products = (
        service.get_latest_products()
    )

    total_products = (
        service.get_total_products()
    )

    total_vendors = (
        service.get_total_vendors()
    )

    return render_template(

        "home.html",

        latest_products=latest_products,

        total_products=total_products,

        total_vendors=total_vendors
    )