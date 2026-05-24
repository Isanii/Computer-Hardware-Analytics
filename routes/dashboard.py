from flask import Blueprint
from flask import render_template
from services.dashboard_service import DashboardService

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

service = DashboardService()

@dashboard_bp.route(
    "/dashboard"
)
def dashboard():

    stats = (
        service.get_statistics()
    )

    cpu_chart = (
        service.get_top_cpu_chart()
    )

    gpu_chart = (
        service.get_top_gpu_chart()
    )

    vendor_chart = (
        service.get_vendor_chart()
    )

    type_chart = (
        service.get_product_type_chart()
    )

    price_chart = (
        service.get_avg_price_chart()
    )

    print(cpu_chart)

    return render_template(

        "dashboard.html",

        stats=stats,

        labels=cpu_chart["labels"],

        values=cpu_chart["values"],

        gpu_labels=gpu_chart["labels"],

        gpu_values=gpu_chart["values"],

        type_labels=type_chart["labels"],

        type_values=type_chart["values"],

        price_labels=price_chart["labels"],

        price_values=price_chart["values"],

    )