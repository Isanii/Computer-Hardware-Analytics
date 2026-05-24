from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from services.product_service import (
    ProductService
)

import csv
from flask import Response

product_bp = Blueprint(
    "products",
    __name__
)

service = ProductService()


@product_bp.route(
    "/products"
)
def get_products():

    products = (
        service.get_all_products()
    )

    result = []

    for product in products:

        result.append({

            "product_id":
                product.product_id,

            "title":
                product.title,

            "price":
                product.price,

            "vendor":
                product.vendor,

            "image":
                product.image_url
        })

    return jsonify(result)


@product_bp.route(
    "/products/<product_id>"
)
def get_product_detail(
    product_id
):

    product = (
        service.get_product_by_id(
            product_id
        )
    )

    if not product:

        return jsonify({

            "message":
                "Không tìm thấy sản phẩm"

        }), 404

    images = (
        service.get_product_images(
            product_id
        )
    )

    specs = (
        service.get_product_specs(
            product_id
        )
    )

    return jsonify({

        "product_id":
            product.product_id,

        "title":
            product.title,

        "vendor":
            product.vendor,

        "price":
            product.price,

        "description":
            product.description,

        "images": [

            image.image_url

            for image in images

        ],

        "specs": [

            {

                "name":
                    spec.spec_name,

                "value":
                    spec.spec_value

            }

            for spec in specs

        ]
    })

@product_bp.route(
    "/products/view"
)
def product_list():

    vendor = request.args.get(
        "vendor"
    )

    product_type = request.args.get(
        "type"
    )

    price_range = request.args.get(
        "price"
    )

    sort = request.args.get(
        "sort"
    )
    query_params = {}

    if vendor:
        query_params["vendor"] = vendor

    if product_type:
        query_params["type"] = product_type

    if price_range:
        query_params["price"] = price_range

    if sort:
        query_params["sort"] = sort
    page = int(
        request.args.get(
            "page",
            1
        )
    )
    # Chặn page âm hoặc bằng 0
    if page < 1:
        page = 1
    page_size = 21

    products = (

        service.get_filtered_products(

            page=page,

            page_size=page_size,

            vendor=vendor,

            product_type=product_type,

            price_range=price_range,

            sort=sort,

        )

    )

    total_products = (

        service.get_filtered_count(

            vendor=vendor,

            product_type=product_type,

            price_range=price_range

        )

    )
    total_pages = (

        total_products
        + page_size
        - 1

    ) // page_size

    # Nếu không có sản phẩm nào
    if total_pages == 0:
        total_pages = 1

    # Chống user nhập page quá lớn
    if page > total_pages:
        page = total_pages

    # Chống page âm hoặc bằng 0
    if page < 1:
        page = 1
    start_page = max(
        page - 2,
        1
    )

    end_page = min(
        page + 2,
        total_pages
    )
    vendors = (
        service.get_all_vendors()
    )

    types = (
        service.get_all_types()
    )

    category_counts = (
        service.get_category_counts()
    )

    return render_template(

        "products/list.html",

        products=products,

        page=page,

        total_pages=total_pages,

        start_page=start_page,

        end_page=end_page,

        vendors=vendors,

        types=types,

        selected_vendor=vendor,

        selected_type=product_type,

        query_params=query_params,

        selected_price=price_range,

        selected_sort=sort,

        total_products=total_products,

        category_counts=category_counts,
    )


@product_bp.route(
    "/products/view/<product_id>"
)
def product_detail(
    product_id
):

    product = (
        service.get_product_by_id(
            product_id
        )
    )

    images = (
        service.get_product_images(
            product_id
        )
    )

    specs = (
        service.get_product_specs(
            product_id
        )
    )

    return render_template(

        "products/detail.html",

        product=product,

        images=images,

        specs=specs
    )


@product_bp.route(
    "/api/search-suggest"
)
def search_suggest():

    keyword = request.args.get(
        "q",
        ""
    )

    products = (

        service.search_suggestions(
            keyword
        )

    )

    return jsonify([

        {

            "id":
            p.product_id,

            "title":
            p.title,

            "price":
            p.price,

            "image":
            p.image_url

        }

        for p in products

    ])

@product_bp.route(
    "/export/products"
)
def export_products():

    products = service.get_all_products()

    def generate():

        # UTF-8 BOM cho Excel
        yield '\ufeff'

        yield "Tên,Hãng,Giá\n"

        for p in products:

            yield (

                f'"{p.title}",'

                f'"{p.vendor}",'

                f'{p.price}\n'

            )

    return Response(

        generate(),

        mimetype="text/csv; charset=utf-8",

        headers={

            "Content-Disposition":
            "attachment; filename=products.csv"

        }

    )