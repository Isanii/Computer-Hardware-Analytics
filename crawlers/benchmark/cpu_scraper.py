from crawlers.benchmark.scraper import Scraper


class CPUScraper:

    def get_all_cpus(self):

        scraper = Scraper(
            "www.cpubenchmark.net"
        )

        return scraper.items