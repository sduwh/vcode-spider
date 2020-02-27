import re
import requests
from bs4 import BeautifulSoup
from models import Problem
from exceptions import CrawlerException


class Crawler:
    NAMESPACE = ""

    def crawl(self, key: str) -> Problem:
        raise NotImplementedError


class POJCrawler(Crawler):
    NAMESPACE = "POJ"

    def crawl(self, key: str) -> Problem:
        r = requests.get(f"http://poj.org/problem?id={key}")
        bs = BeautifulSoup(r.content, "html.parser")

        problem = Problem(POJCrawler.NAMESPACE, key)
        problem.title = bs.select(".ptt")[0].get_text()

        meta_nodes = bs.select(".plm")[0].select("td")

        time_limit_raw = meta_nodes[0].get_text()
        matches = re.findall(r"Time Limit: (\d+)MS", time_limit_raw)
        if len(matches) != 1:
            raise CrawlerException(f"no time limit found, raw: '{time_limit_raw}'")
        problem.time_limit = int(matches[0])

        memory_limit_raw = meta_nodes[2].get_text()
        matches = re.findall(r"Memory Limit: (\d+)K", memory_limit_raw)
        if len(matches) != 1:
            raise CrawlerException(f"no memory limit found, raw: '{memory_limit_raw}'")
        problem.memory_limit = int(matches[0])

        desc_nodes = bs.select(".ptx")
        try:
            problem.description = desc_nodes[0].prettify()
            problem.input = desc_nodes[1].prettify()
            problem.output = desc_nodes[2].prettify()
            problem.hint = desc_nodes[3].prettify()
            problem.source = desc_nodes[4].prettify()
        except IndexError:
            pass

        sample_nodes = bs.select(".sio")
        try:
            problem.sample_input = sample_nodes[0].prettify()
            problem.sample_output = sample_nodes[1].prettify()
        except IndexError:
            pass

        # print(problem.title)
        # print(problem.time_limit)
        # print(problem.memory_limit)
        # print(problem.description)
        # print(problem.input)
        # print(problem.output)
        # print(problem.sample_input)
        # print(problem.sample_output)
        # print(problem.hint)
        # print(problem.source)
        return problem


class HDUCrawler(Crawler):
    NAMESPACE = "HDU"

    def crawl(self, key: str) -> Problem:
        pass


class SDUTCrawler(Crawler):
    NAMESPACE = "SDUT"

    def crawl(self, key: str) -> Problem:
        pass


class Crawlers:
    _crawlers = {
        POJCrawler.NAMESPACE: POJCrawler(),
    }

    @staticmethod
    def crawl(namespace: str, key: str) -> Problem:
        return Crawlers._crawlers[namespace].crawl(key)
