from abc import ABCMeta
import json
import csv


class AbstractOutput(metaclass=ABCMeta):
    def __init__(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def output(self, statistics, settings):
        raise NotImplementedError()


class JSONOutput(AbstractOutput):
    def __init__(self, path):
        super(JSONOutput, self).__init__(path)

    def output(self, statistics, settings):
        output_dict = {
            'project_url': settings['url'],
            'part_of_code': settings['part_of_code'],
            'part_of_speech': settings['part_of_speech'],
            'statistics': {el[0]: el[1] for el in statistics}
        }
        with open(self.path + '/statistics_report.json', 'w') as json_file:
            json.dump(output_dict, json_file)
        json_file.close()


class CSVOutput(AbstractOutput):
    def __init__(self, path):
        super(CSVOutput, self).__init__(path)

    def output(self, statistics, settings):
        fields = [[el[0], el[1]] for el in statistics]
        with open(self.path + '/statistics_report.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(fields)
        csv_file.close()
