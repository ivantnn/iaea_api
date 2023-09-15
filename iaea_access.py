import pandas as pd
import urllib.request

path = "https://nds.iaea.org/relnsd/v0/data?"

def lc_df(url):
	req=urllib.request.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
	return pd.read_csv(urllib.request.urlopen(req))
