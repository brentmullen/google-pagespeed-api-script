*SYNOPSIS*
1. This script reads urls from 'pagespeed.txt' file. Load this file with full URLS.
2. Queries each url with the google pagespeed api.
3. Filters JSON results to only include desired metrics.
4. Metrics are saved to local .csv spreadsheet for analysis.

### Reqs
Python3

### Google API Key
Create API Key: https://console.developers.google.com/apis/credentials (Create Credentials)

Enable PageSpeed Insights API: https://console.developers.google.com/apis/api/pagespeedonline.googleapis.com/overview

```bash
export GOOGLE_API_KEY={YOUR_KEY}
```
