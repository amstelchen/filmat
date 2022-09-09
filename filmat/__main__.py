import os
import sys
import json
import requests
import argparse
from datetime import date

PROG = "filmat"
VERSION = "0.1.0"
AUTHOR = "Copyright (C) 2022, by Michael John"
DESC = "A cinema show times interface for the film.at API"


def main():

    parser = argparse.ArgumentParser(prog=PROG, description=DESC)
    parser.add_argument('cinema', metavar='cinema', type=str, nargs='?', default = "",
                        help='which cinema so show (or all, if missing)')
    parser.add_argument('when', metavar='when', type=str, nargs='?', default=str(date.today()),
                        help='date of screening (or today, if missing)')
    parser.add_argument('file', metavar='file', type=str, nargs='?', default="", #default=str(date.today()),
                        help='use local file instead of api')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + VERSION + ' ' + AUTHOR)

    args = parser.parse_args()
    #print(args.accumulate(args.integers))

    #date1 = str(date.today())
    #date = "2022-09-11"
    cinema = args.cinema # sys.argv[1]
    print(args.when)
    #print(len(args.file))

    if len(args.file) > 0:
        with open(args.file + ".json", "r") as read_file:
            data = json.load(read_file)
    else:
        response = requests.get("https://efs.film.at/api/v1/cfs/filmat/screenings/nested/cinema/" + args.when)
        data = json.loads(response.text)

    #print(os.listdir())

    #print(data)
    #list(filter(lambda x: x['type'] == 1, data))

    #for key in data:
        #if data[key] == "type":
    #    print(key)

    for result in data['result']:
        #print(type(result['parent']['title']))
        if cinema in result['parent']['title']:
            print(result['parent']['title'])
            for film in result['nestedResults']:
                print(f"  {film['parent']['title']}")
                for screening in film['screenings']:
                    print(f"    {screening['time'][11:16]}")

    #if 'cinema' in data['result']:
    #    print(data['result']['title'])

if __name__ == "__main__":
    main()
