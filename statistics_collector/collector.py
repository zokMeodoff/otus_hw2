from statistics_collector.output import JSONOutput, CSVOutput
from statistics_collector.repository import GithubRepository
from statistics_collector.parser import PythonParser
import tempfile
import os


class StatisticsCollector:
    def __init__(self, settings):
        self._settings = settings
        self._parser = self._init_parser()
        self._output = self._init_output()
        self._repository = self._init_repository()

    def _init_parser(self):
        if self._settings['lang'] == 'py':
            return PythonParser()

    def _init_output(self):
        report_dir_path = os.path.dirname(os.getcwd()) + '/reports'
        if not os.path.exists(report_dir_path):
            os.mkdir(report_dir_path)
        if self._settings['format'] == 'json':
            return JSONOutput(report_dir_path)
        elif self._settings['format'] == 'csv':
            return CSVOutput(report_dir_path)

    def _init_repository(self):
        if 'https://github.com' in self._settings['url']:
            return GithubRepository(self._settings['url'])

    def collect_statistics(self):
        temp_path = tempfile.mkdtemp()
        self._repository.clone_repository(temp_path)
        self._parser.set_path(temp_path)
        return self._parser.get_words_count(self._settings['part_of_code'], self._settings['part_of_speech'],
                                            self._settings['top_size'])

    def statistics_output(self, statistics):
        if self._settings['format'] == 'console':
            for word, occurrence in statistics:
                print(word, occurrence)
        else:
            self._output.output(statistics, self._settings)
            report_path = os.path.dirname(os.getcwd()).replace('\\', '/')
            print('Сгенерирован файл со статистикой: {0}/reports/statistics_report.{1}'.format(report_path,
                                                                                              self._settings['format']))
