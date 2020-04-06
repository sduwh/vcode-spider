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
        return problem


class HDUCrawler(Crawler):
    NAMESPACE = "HDU"

    def crawl(self, key: str) -> Problem:
        r = requests.get(f"http://acm.hdu.edu.cn/showproblem.php?pid={key}")
        bs = BeautifulSoup(r.content, "html.parser")

        problem = Problem(HDUCrawler.NAMESPACE, key)
        problem.title = bs.find('h1').get_text()

        meta_nodes = bs.find('span').get_text()
        time_limit_raw = re.findall(r"Time Limit: (\d+/\d+ MS \(Java/Others\))", meta_nodes)
        if len(time_limit_raw) != 1:
            raise CrawlerException(
                f"no time limit found, HDU problem: '{key}'")
        problem.time_limit = time_limit_raw[0]

        memory_limit_raw = re.findall(r"Memory Limit: (\d+/\d+ K \(Java/Others\))", meta_nodes)
        if len(memory_limit_raw) != 1:
            raise CrawlerException(
                f"no memory limit found, raw: '{memory_limit_raw}'")
        problem.memory_limit = memory_limit_raw[0]

        desc_nodes = bs.select(".panel_content")
        try:
            problem.description = desc_nodes[0].prettify()
            problem.input = desc_nodes[1].prettify()
            problem.output = desc_nodes[2].prettify()
            problem.sample_input = desc_nodes[3].prettify()
            problem.sample_output = desc_nodes[4].prettify()
            problem.source = desc_nodes[5].prettify()
            problem.hint = desc_nodes[6].prettify()
        except IndexError:
            pass
        print(dict(problem))
        return problem


class SDUTCrawler(Crawler):
    NAMESPACE = "SDUT"

    def crawl(self, key: str) -> Problem:
        r = requests.get(
            f"https://acm.sdut.edu.cn/onlinejudge2/index.php/API_ng/problems/{key}")

        problem = Problem(SDUTCrawler.NAMESPACE, key)

        meta_nodes = r.json().get('data')
        if meta_nodes is None or len(meta_nodes) is 0:
            raise CrawlerException(f"SDUT problem-{key} is not found")

        problem.title = meta_nodes.get('title')
        problem.description = meta_nodes.get('description')
        problem.input = meta_nodes.get('input')
        problem.output = meta_nodes.get('output')
        problem.hint = meta_nodes.get('hint')
        problem.source = meta_nodes.get('source')
        problem.sample_input = meta_nodes.get('sampleInput')
        problem.sample_output = meta_nodes.get('sampleOutput')
        problem.memory_limit = meta_nodes.get('memoryLimit')
        problem.time_limit = meta_nodes.get('timeLimit')

        return problem


class Crawlers:
    _crawlers = {
        POJCrawler.NAMESPACE: POJCrawler(),
        HDUCrawler.NAMESPACE: HDUCrawler(),
        SDUTCrawler.NAMESPACE: SDUTCrawler(),
    }

    @staticmethod
    def crawl(namespace: str, key: str) -> Problem:
        return Crawlers._crawlers[namespace].crawl(key)
