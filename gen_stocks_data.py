#!/usr/bin/env python2

# usage: python HistoricalDataRequest.py <host-ip>

import argparse
import json
import ssl
import sys
import urllib2
import requests
import pandas as pd


def request(args):


	""" 1. Read the input csv table """ 

	company_table = pd.read_csv('{}'.format(args.filein))
	companies = company_table['Ticker symbol']
	n_companies = len(companies)
	""" 2. Process each company in companies and save out. """

	for company_id in range(n_companies):
		# companyname, _ = '{}'.format(args.fileout).split('.')
		companyname = companies[company_id]

		print companyname

		data = {
			"securities": [companyname+" US Equity"],
			"fields": ["PX_LAST"],
			# "eventTypes": ["TRADE"],
			"startDate": "20120101",
			"endDate": "20150101",
			"periodicitySelection": "DAILY"
			# "eventTypes": ["AT_TRADE"]
		}

		print data

		req = urllib2.Request('https://{}/request?ns=blp&service=refdata&type=HistoricalDataRequest'.format(args.host))
		# req = urllib2.Request('https://{}/request?ns=blp&service=refdata&type=IntradayTickRequest'.format(args.host))
		req.add_header('Content-Type', 'application/json')

		ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
		ctx.load_verify_locations('bloomberg.crt')
		ctx.load_cert_chain('warwickhack_spring_2015_014.crt', 'warwickhack_spring_2015_014.key')

		try:

			res = urllib2.urlopen(req, data=json.dumps(data), context=ctx)

			# this parses out the html string request.
			dat = res.read()
			dat1 = json.loads(dat)

			# this is a super useful module for pretty printing aligned. so gonna use it.
			import pprint 
			# pprint.pprint(dat1)
			security = dat1['data'][0]['securityData']['fieldData']
			points = [(r['date'], r['PX_LAST']) for r in security]

			# pprint.pprint(points)
			# pprint.pprint(security)

			table = pd.DataFrame.from_dict(points)

			table.to_csv('Equity_Data/'+companyname+'.csv', header=['Date','Price'], index=False)


		# data1 = dat['data']
		# print data1['fieldData']
		# data2 = json.loads(data1)
		# data2 = json.loads(data2)

		# print type(dat1)

		# print data1

		# items = dat.split('}')

		# for item in items:
			# print item

		# print dat["securityData"]
		# print type(dat[0]['data'])

		except Exception as e:
			e
			print e
			return 1
		# return 0


# def main():
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('host', type=str)
	parser.add_argument('filein', type=str)
	# print companyname, _ = '{}'.format(args.fileout).split('.')

	request(parser.parse_args())

# if __name__ == "__main__":
	# main()
	# sys.exit(main())
