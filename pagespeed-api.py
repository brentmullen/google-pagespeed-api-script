#!/usr/bin/env python3
import requests, os, csv

# Documentation: https://developers.google.com/speed/docs/insights/v5/get-started

# JSON paths: https://developers.google.com/speed/docs/insights/v4/reference/pagespeedapi/runpagespeed
googleApiKey = os.getenv('GOOGLE_API_KEY')

if googleApiKey is None:
    googleApiKey = input('Google API Key (can be empty for single run): ')

# Populate 'pagespeed.txt' file with URLs to query against API.
with open('pagespeed.csv') as pagespeedurls:
    download_dir = 'pagespeed-results.csv'
    file = open(download_dir, 'w')
    file.write("Description, URL, V6 Score, FCP, SI, LCP, TTI, TBT, CLS\n")

    content = csv.reader(pagespeedurls, delimiter=',')

    # This is the google pagespeed api url structure, using for loop to insert each url in .txt file
    for row in content:
        if row[0] == 'Description':
            continue

        # If no "strategy" parameter is included, the query by default returns desktop data.
        analyzeUrl = row[1].replace('&', '%26').strip(' ')
        x = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={analyzeUrl}&strategy=mobile'
        print(f'Requesting {x}...')
        r = requests.get(f'{x}&key={googleApiKey}')
        final = r.json()
        
        try:
            url = str(final['id'])

            fcp = str(final['lighthouseResult']['audits']['first-contentful-paint']['displayValue'])
            fcpScore = final['lighthouseResult']['audits']['first-contentful-paint']['score']

            si = str(final['lighthouseResult']['audits']['speed-index']['displayValue'])
            siScore = final['lighthouseResult']['audits']['speed-index']['score']

            lcp = str(final['lighthouseResult']['audits']['largest-contentful-paint']['displayValue'])
            lcpScore = final['lighthouseResult']['audits']['largest-contentful-paint']['score']

            tti = str(final['lighthouseResult']['audits']['interactive']['displayValue'])
            ttiScore = final['lighthouseResult']['audits']['interactive']['score']

            tbt = str(final['lighthouseResult']['audits']['total-blocking-time']['displayValue'])
            tbtScore = final['lighthouseResult']['audits']['total-blocking-time']['score']

            cls = str(final['lighthouseResult']['audits']['cumulative-layout-shift']['displayValue'])
            clsScore = final['lighthouseResult']['audits']['cumulative-layout-shift']['score']

            v6score = round(final['lighthouseResult']['categories']['performance']['score'] * 100)
        except KeyError:
            print(f'<KeyError> One or more keys not found {analyzeUrl}.')
        
        try:
            file.write(f'{row[0]}, {url}, {str(v6score)}, {fcp}, {si}, {lcp}, {tti}, "{tbt}", {cls}\n'.replace(' ', ' '))
        except NameError:
            print(f'<NameError> Failing because of KeyError {analyzeUrl}.')
            file.write(f'<KeyError> & <NameError> Failing because of nonexistant Key ~ {analyzeUrl}.' + '\n')
        
        try:
            print(f'Description: {row[0]}')
            print(f'URL: {url}')
            print(f'Mobile Score (V6): {str(v6score)}')
            print(f'First Contentful Paint: {fcp} ({str(fcpScore)})')
            print(f'Speed Index: {si} ({str(siScore)})')
            print(f'Largest Contentful Paint: {lcp} ({str(lcpScore)})')
            print(f'Time to Interactive: {tti} ({str(ttiScore)})')
            print(f'Total Block Time: {tbt} ({str(tbtScore)})')
            print(f'Cumulative Layout Shift: {cls} ({str(clsScore)})')
        except NameError:
            print(f'<NameError> Failing because of KeyError {analyzeUrl}.')

    file.close()
