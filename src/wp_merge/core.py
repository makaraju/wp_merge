import csv
#import pip._vendor.requests as requests
import requests
import logging
import os
import argparse
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError

class MergeCsvRecords(object):
    def __init__(self, url='http://interview.wpengine.io/v1/accounts'):
        self.url = url
        self.session = requests.Session()
    
    def url_ok(self):
        try:
            r = requests.head(self.url)
            r.raise_for_status()
        except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
            raise ValueError('Api Server is not available, please retry after some time....')

    def readcsv(self, inputfile):
        if not os.path.exists(inputfile):
            raise FileNotFoundError
        with open(inputfile, 'r') as fd:
            reader = csv.DictReader(fd)
            print(reader.fieldnames)
            if 'Account ID' not in reader.fieldnames:
                #raise ValueError('No Account Id found')
                print(f'Account ID missing... {reader.fieldnames}')
            for row in reader:
                yield row
    
    def fetchaccountinfo(self, accountid):
        try:
            resp = self.session.get(f'{self.url}/{accountid}')
            resp.raise_for_status()
            return resp.json()
        except Exception as ex:
            logging.error(f'unable to process account id {accountid}. error: {ex}')
    
    def generateoutput(self, inputfile, outputfile):
        with open(outputfile, 'w', newline='') as csvfile:
            fieldnames = ['Account ID', 'First Name', 'Created On', 'Status', 'Status Set On']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.readcsv(inputfile):
                del row['Account Name']
                accountinfo = self.fetchaccountinfo(row['Account ID'])
                print(f'Account info...{accountinfo}')
                if not accountinfo:
                    continue

                row['Status'] = accountinfo['status']
                row['Status Set On'] = accountinfo['created_on']
                writer.writerow(row)

def parse_arguments() -> object:
    parser = argparse.ArgumentParser(description="Convert Json")

    # Positional mandatory arguments
    parser.add_argument("-i","--inputfile", help="Input CSV data file", type=str)
    parser.add_argument("-o","--output", help="Output CSV file", type=str)
    parser.add_argument("-v", "--verbose", help="Increase output verbose, more v more output.", action="count", default=0)

    return parser.parse_args()


def main():

    logging.basicConfig(level=logging.INFO)
    args = parse_arguments()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    mergecsv = MergeCsvRecords()
    mergecsv.url_ok()
    mergecsv.generateoutput(args.inputfile, args.output)

if __name__ == "__main__":
    main()

