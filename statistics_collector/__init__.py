import sys
import os
from argparse import ArgumentParser

from statistics_collector.collector import StatisticsCollector


def main():
    return_code = 0
    try:
        parser = ArgumentParser(description='Сбор статистики по наиболее часто встречающимся словам в исходном коде')
        parser.add_argument('url', type=str,
                            help='Ссылка на репозиторий с исходным кодом')
        parser.add_argument('-f', '--format', type=str, nargs='?',
                            choices=['console', 'json', 'csv'], default='console',
                            help='Формат вывода отчёта со статистикой: '
                                 'console - консоль; json - json-файл; csv - csv-файл')
        parser.add_argument('-p', '--part_of_speech', nargs='?', type=str,
                            choices=['verb', 'noun'], default='verb',
                            help='Части речи, по которым проводится сбор статистики: '
                                 'verb - глаголы; noun - существительные')
        parser.add_argument('-c', '--part_of_code', nargs='?', type=str,
                            choices=['func', 'var'], default='func',
                            help='Части кода, в которых производится сбор статистики: '
                                 'func - названия функций; var - названия локальных переменных внутри функций')
        parser.add_argument('-l', '--lang', nargs='?', default='py', type=str,
                            help='Язык программирования анализируемого кода'),
        parser.add_argument('-t', '--top_size', nargs='?', type=int, default='10',
                            help='Ограничение на количество выводимых в статистике слов')

        args = parser.parse_args(sys.argv[1:])

        current_settings = dict(url=args.url,
                                format=args.format,
                                part_of_speech=args.part_of_speech,
                                part_of_code=args.part_of_code,
                                lang=args.lang,
                                top_size=args.top_size)

        stat_collector = StatisticsCollector(current_settings)
        statistics = stat_collector.collect_statistics()
        stat_collector.statistics_output(statistics)

    except Exception as e:
        print(e)
        return_code = 1

    return return_code
