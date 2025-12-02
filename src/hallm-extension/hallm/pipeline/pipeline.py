import logging

from .extraction.extractor import Extractor
from halucinator import hal_log, hal_config

log = logging.getLogger(__name__)
hal_log.setLogConfig()

class Pipeline:
    def __init__(self, config: hal_config.HalucinatorConfig):
        self.extractor = Extractor(config)

    def run(self):
        self.extractor.extract()