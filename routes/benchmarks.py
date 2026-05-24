from flask import Blueprint
from flask import render_template
from flask import request

from services.benchmark_service import (
    BenchmarkService
)

benchmark_bp = Blueprint(
    "benchmark",
    __name__
)

service = BenchmarkService()


@benchmark_bp.route(
    "/benchmarks/cpu"
)
def cpu_benchmark():

    page = int(
        request.args.get(
            "page",
            1
        )
    )

    keyword = request.args.get(
        "q"
    )

    page_size = 50

    cpus = service.get_cpu_benchmarks(

        page=page,

        page_size=page_size,

        keyword=keyword

    )

    total = service.get_cpu_count(
        keyword
    )

    total_pages = (

        total
        + page_size
        - 1

    ) // page_size

    start_page = max(
        page - 2,
        1
    )

    end_page = min(
        page + 2,
        total_pages
    )

    return render_template(

        "benchmarks/cpu_list.html",

        cpus=cpus,

        page=page,

        total_pages=total_pages,

        start_page=start_page,

        end_page=end_page,

        keyword=keyword
    )


@benchmark_bp.route(
    "/benchmarks/gpu"
)
def gpu_benchmark():

    page = int(
        request.args.get(
            "page",
            1
        )
    )

    keyword = request.args.get(
        "q"
    )

    page_size = 50
    start_rank = (
        (page - 1)
        * page_size
    )

    gpus = service.get_gpu_benchmarks(

        page=page,

        page_size=page_size,

        keyword=keyword

    )

    total = service.get_gpu_count(
        keyword
    )

    total_pages = (

        total
        + page_size
        - 1

    ) // page_size

    start_page = max(
        page - 2,
        1
    )

    end_page = min(
        page + 2,
        total_pages
    )

    return render_template(

        "benchmarks/gpu_list.html",

        gpus=gpus,

        page=page,

        total_pages=total_pages,

        start_page=start_page,

        end_page=end_page,

        start_rank=start_rank,

        keyword=keyword
    )

@benchmark_bp.route(
    "/compare/cpu"
)
def compare_cpu():

    cpu1_id = request.args.get(
        "cpu1"
    )

    cpu2_id = request.args.get(
        "cpu2"
    )

    cpu1 = None
    cpu2 = None

    if cpu1_id:

        cpu1 = service.get_cpu_by_id(
            cpu1_id
        )

    if cpu2_id:

        cpu2 = service.get_cpu_by_id(
            cpu2_id
        )

    cpu_list = (
        service.get_top_cpus(
            200
        )
    )

    return render_template(

        "benchmarks/cpu_compare.html",

        cpu1=cpu1,

        cpu2=cpu2,

        cpu_list=cpu_list,

        chart_labels=[

            cpu1.name if cpu1 else "",

            cpu2.name if cpu2 else ""

        ],

        cpu_mark_values=[

            cpu1.cpumark if cpu1 else 0,

            cpu2.cpumark if cpu2 else 0

        ],

        thread_values=[

            cpu1.thread_mark if cpu1 else 0,

            cpu2.thread_mark if cpu2 else 0

        ],

        core_values=[

            cpu1.cores if cpu1 else 0,

            cpu2.cores if cpu2 else 0

        ],

        thread_count_values=[

            cpu1.threads if cpu1 else 0,

            cpu2.threads if cpu2 else 0

        ]

    )

@benchmark_bp.route(
    "/compare/gpu"
)
def compare_gpu():

    gpu1_id = request.args.get(
        "gpu1"
    )

    gpu2_id = request.args.get(
        "gpu2"
    )

    gpu1 = None
    gpu2 = None

    if gpu1_id:

        gpu1 = service.get_gpu_by_id(
            gpu1_id
        )

    if gpu2_id:

        gpu2 = service.get_gpu_by_id(
            gpu2_id
        )

    gpu_list = (
        service.get_top_gpus(
            200
        )
    )

    return render_template(

        "benchmarks/gpu_compare.html",

        gpu1=gpu1,

        gpu2=gpu2,

        gpu_list=gpu_list,

        chart_labels=[

            gpu1.name if gpu1 else "",

            gpu2.name if gpu2 else ""

        ],

        g3d_values=[

            gpu1.g3d_mark if gpu1 else 0,

            gpu2.g3d_mark if gpu2 else 0

        ],

        g2d_values=[

            gpu1.g2d_mark if gpu1 else 0,

            gpu2.g2d_mark if gpu2 else 0

        ],

        tdp_values=[

            gpu1.tdp if gpu1 else 0,

            gpu2.tdp if gpu2 else 0

        ]

    )



@benchmark_bp.route(
    "/benchmarks/cpu/<cpu_id>"
)
def cpu_detail(
    cpu_id
):

    cpu = (
        service.get_cpu_by_id(
            cpu_id
        )
    )

    if not cpu:

        return "Không tìm thấy CPU", 404

    return render_template(

        "benchmarks/cpu_detail.html",

        cpu=cpu

    )

@benchmark_bp.route(
    "/benchmarks/gpu/<gpu_id>"
)
def gpu_detail(
    gpu_id
):

    gpu = (
        service.get_gpu_by_id(
            gpu_id
        )
    )

    if not gpu:

        return "Không tìm thấy GPU", 404

    return render_template(

        "benchmarks/gpu_detail.html",

        gpu=gpu

    )
