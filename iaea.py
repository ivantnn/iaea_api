import pandas as pd
import urllib.request

class Api:
	def path():
		path = "https://nds.iaea.org/relnsd/v0/data?"
		return path

	def lc_df(url):
		req=urllib.request.Request(url)
		req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
		return pd.read_csv(urllib.request.urlopen(req))

	def Import_Cases(mode,isotope,param):
		path=Api.path()
		match mode:
			case 'ground_states':
				return Api.lc_df(path+'fields='+mode+'&nuclides='+isotope)
			case 'levels':
				return Api.lc_df(path+'fields='+mode+'&nuclides='+isotope)
			case 'gammas':
				return Api.lc_df(path+'fields='+mode+'&nuclides='+isotope)
			case 'cummulative':
				return Api.lc_df(path+'fields=cumulative_fy&'+param+'='+isotope)
			case 'decay_rads':
				return Api.lc_df(path+'fields=decay_rads&nuclides='+isotope+'&rad_types='+param)

	def Import(mode,isotope,param=None): #Only one that can have all isotopes. Param changes for the decay_rads or te cummulatice cases
		if type(isotope)==list:
			ret=list()
			for i in range(0,len(isotope)):
				ret.append(Api.Import_Cases(mode,isotope[i],param))
			return ret
		else:
			return Api.Import_Cases(mode,isotope,param)

	def Export(data,name):
		data_typ=type(data)
		data_len=len(data)
		if data_typ==list:
			if data_len==len(name):
				[data[i].to_excel(name[i]+'.xlsx') for i in range(0,data_len)]
			return
		else:
			data.to_excel(name+'.xlsx')
			return

	def Call(mode,isotope,name,param=None):
		if (((mode=='cummulative')|(mode=='decay_rads')) and (param==None)):
			return
		Api.Export(Api.Import(mode,isotope,param),name)
		return

