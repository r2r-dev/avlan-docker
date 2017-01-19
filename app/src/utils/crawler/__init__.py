from click import (
    group,
    option,
)

from src.utils.crawler.AvlanCrawler import AvlanCrawler


@group()
def cli():
    pass


@cli.command()
@option(
    '--input_file',
    help='Input JSON file used to query nodes and construct effective output'
         'containing vlan data',
    type=unicode,
    required=True,
)
@option(
    '--output_file',
    help='Output file containing vlan related data',
    type=unicode,
    required=True,
)
@option(
    '--schema_file',
    help='Schema file for input data validation',
    type=unicode,
    required=True,
)
def crawl(**options):
    crawler = AvlanCrawler(
        input_file=options['input_file'],
        schema_file=options['schema_file'],
    )
    crawler.crawl()
    crawler.write_config(options['output_file'])
