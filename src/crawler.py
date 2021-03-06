import re
import requests
from bs4 import BeautifulSoup
from models import Problem
from exceptions import CrawlerException
from logger import logger
from common import IMAGE_TAG_REGULAR


def replace_image_src(regular, target, add_origin) -> str:
    changed_str = target
    matched_list = re.findall(regular, changed_str)
    for item in matched_list:
        changed_str = re.sub(item, add_origin + item, changed_str)
    return changed_str


class Crawler:
    NAMESPACE = ""

    def crawl(self, key: str) -> Problem:
        raise NotImplementedError


class POJCrawler(Crawler):
    NAMESPACE = 'POJ'
    OJ_ORIGIN = 'http://poj.org/'

    def crawl(self, key: str) -> Problem:
        logger.info("[*] start crawl problem POJ-{}".format(key))
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
            problem.source = desc_nodes[4].get_text()
        except IndexError:
            pass
        problem.description = replace_image_src(IMAGE_TAG_REGULAR, problem.description, self.OJ_ORIGIN)
        sample_nodes = bs.select(".sio")
        try:
            problem.sample_input = sample_nodes[0].get_text()
            problem.sample_output = sample_nodes[1].get_text()
        except IndexError:
            pass
        problem.language = ['C++', "JAVA", "C"]
        return problem


class HDUCrawler(Crawler):
    NAMESPACE = "HDU"
    ORIGIN = 'http://acm.hdu.edu.cn/'

    def crawl(self, key: str) -> Problem:
        logger.info("[*] start crawl problem HDU-{}".format(key))
        r = requests.get(f"http://acm.hdu.edu.cn/showproblem.php?pid={key}")
        bs = BeautifulSoup(r.content, "html.parser")

        problem = Problem(HDUCrawler.NAMESPACE, key)
        problem.title = bs.find('h1').get_text()

        meta_nodes = bs.find('span').get_text()
        time_limit_raw = re.findall(r"Time Limit: \d+/(\d+) MS \(Java/Others\)", meta_nodes)
        if len(time_limit_raw) != 1:
            raise CrawlerException(
                f"no time limit found, HDU problem: '{key}'")
        problem.time_limit = time_limit_raw[0]

        memory_limit_raw = re.findall(r"Memory Limit: \d+/(\d+) K \(Java/Others\)", meta_nodes)
        if len(memory_limit_raw) != 1:
            raise CrawlerException(
                f"no memory limit found, raw: '{memory_limit_raw}'")
        problem.memory_limit = memory_limit_raw[0]

        desc_nodes = bs.select(".panel_content")
        try:
            problem.description = desc_nodes[0].prettify()
            problem.input = desc_nodes[1].prettify()
            problem.output = desc_nodes[2].prettify()
            problem.sample_input = desc_nodes[3].get_text()
            problem.sample_output = desc_nodes[4].get_text()
            problem.source = desc_nodes[5].get_text()
            problem.hint = desc_nodes[6].get_text()
        except IndexError:
            pass
        problem.description = replace_image_src(IMAGE_TAG_REGULAR, problem.description, self.ORIGIN)
        problem.language = ['C++', "JAVA", "C"]
        return problem


class SDUTCrawler(Crawler):
    NAMESPACE = "SDUT"
    ORIGIN = 'https://acm.sdut.edu.cn/'

    def crawl(self, key: str) -> Problem:
        logger.info("[*] start crawl problem SDUT-{}".format(key))
        r = requests.get(f"https://acm.sdut.edu.cn/onlinejudge2/index.php/API_ng/problems/{key}")

        problem = Problem(SDUTCrawler.NAMESPACE, key)

        meta_nodes = r.json().get('data')
        if meta_nodes is None or len(meta_nodes) is 0:
            raise CrawlerException(f"SDUT problem-{key} is not found")

        problem.title = meta_nodes.get('title')
        problem.description = meta_nodes.get('description')
        problem.description = replace_image_src(IMAGE_TAG_REGULAR, problem.description, self.ORIGIN)
        problem.input = meta_nodes.get('input')
        problem.output = meta_nodes.get('output')
        problem.hint = meta_nodes.get('hint')
        problem.source = meta_nodes.get('source')
        problem.sample_input = meta_nodes.get('sampleInput')
        problem.sample_output = meta_nodes.get('sampleOutput')
        problem.memory_limit = meta_nodes.get('memoryLimit')
        problem.time_limit = meta_nodes.get('timeLimit')
        problem.language = ['C++', "JAVA", "C"]
        return problem


class Crawlers:
    _crawlers = {
        POJCrawler.NAMESPACE: POJCrawler(),
        HDUCrawler.NAMESPACE: HDUCrawler(),
        SDUTCrawler.NAMESPACE: SDUTCrawler(),
    }

    @staticmethod
    def crawl(namespace: str, key: str) -> Problem:
        try:
            return Crawlers._crawlers[namespace].crawl(key)
        except Exception as e:
            raise e
