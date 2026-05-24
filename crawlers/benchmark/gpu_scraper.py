from crawlers.benchmark.scraper import Scraper


class GPUScraper:

    def get_all_gpus(self):

        scraper = Scraper(
            "www.videocardbenchmark.net"
        )

        return scraper.items