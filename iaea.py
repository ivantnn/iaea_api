import numpy as np
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
		if mode == 'ground_states':
			return Api.lc_df(path+'fields='+mode+'&nuclides='+isotope)
		elif mode =='levels':
			return Api.lc_df(path+'fields='+mode+'&nuclides='+isotope)
		elif mode == 'gammas':
			return Api.lc_df(path+'fields='+mode+'&nuclides='+isotope)
		elif mode == 'cummulative':
			return Api.lc_df(path+'fields=cumulative_fy&'+param+'='+isotope)
		elif 'decay_rads':
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

class chain_finder:
	def __init__(self):
		#Using iaea script to download the data from IAEA
		df = Api.Import('ground_states','all')
		self.df = df
		#A dictionary of names for the symbols
		self.isotopes_dic = {0:'Nn',1:'H',2:'He',3:'Li',4:'Be',5:'B',6:'C',7:'N',8:'O',9:'F',10:'Ne',11:'Na',12:'Mg',13:'Al',14:'Si',15:'P',16:'S',17:'Cl',18:'Ar',19:'K',20:'Ca',21:'Sc',22:'Ti',23:'V',24:'Cr',25:'Mn',26:'Fe',27:'Co',28:'Ni',29:'Cu',30:'Zn',31:'Ga',32:'Ge',33:'As',34:'Se',35:'Br',36:'Kr',37:'Rb',38:'Sr',39:'Y',40:'Zr',41:'Nb',42:'Mo',43:'Tc',44:'Ru',45:'Rh',46:'Pd',47:'Ag',48:'Cd',49:'In',50:'Sn',51:'Sb',52:'Te',53:'I',54:'Xe',55:'Cs',56:'Ba',57:'La',58:'Ce',59:'Pr',60:'Nd',61:'Pm',62:'Sm',63:'Eu',64:'Gd',65:'Tb',66:'Dy',67:'Ho',68:'Er',69:'Tm',70:'Yb',71:'Lu',72:'Hf',73:'Ta',74:'W',75:'Re',76:'Os',77:'Ir',78:'Pt',79:'Au',80:'Hg',81:'Tl',82:'Pb',83:'Bi',84:'Po',85:'At',86:'Rn',87:'Fr',88:'Ra',89:'Ac',90:'Th',91:'Pa',92:'U',93:'Np',94:'Pu',95:'Am',96:'Cm',97:'Bk',98:'Cf',99:'Es',100:'Fm',101:'Md',102:'No',103:'Lr',104:'Rf',105:'Db',106:'Sg',107:'Bh',108:'Hs',109:'Mt',110:'Ds',111:'Rg',112:'Cn',113:'Nh',114:'Fl',115:'Mc',116:'Lv',117:'Ts',118:'Og'}

		self.decays = {
        ' ':np.array([0,0]),
        '14C':np.array([-6,-8]),
        '24NE':np.array([-10,-14]),
        '2B+':2*np.array([-1,+1]),
        '2B-':2*np.array([+1,-1]),
        '2EC':2*np.array([-1,+1]),
        '2N':2*np.array([0,-1]),
        '2P':2*np.array([-1,0]),
        '34SI':np.array([-14,-20]),
        'A':np.array([-2,-2]),
        'B+':np.array([-1,+1]),
        'B++EC':np.array([0,0]),
        'B+2P':np.array([-1,+1])+2*np.array([-1,0]),
        'B+A':np.array([-1,+1])+np.array([-2,-2]),
        'B+F':np.array([0,0]),
        'B+P':np.array([-1,+1])+np.array([-1,0]),
        'B-':np.array([+1,-1]),
        'B-2N':np.array([+1,-1])+2*np.array([0,-1]),
        'B-3N':np.array([+1,-1])+3*np.array([0,-1]),
        'B-4N':np.array([+1,-1])+4*np.array([0,-1]),
        'B-5N':np.array([+1,-1])+5*np.array([0,-1]),
        'B-6N':np.array([+1,-1])+6*np.array([0,-1]),
        'B-7N':np.array([+1,-1])+7*np.array([0,-1]),
        'B-A':np.array([+1,-1])+np.array([-2,-2]),
        'B-F':np.array([0,0]),
        'B-N':np.array([+1,-1])+np.array([0,-1]),
        'B-P':np.array([+1,-1])+np.array([-1,0]),
        'EC':np.array([-1,+1]),
        'EC+B+':np.array([0,0]),
        'EC2P':np.array([-1,+1])+2*np.array([-1,0]),
        'ECA':np.array([-1,+1])+2*np.array([-2,-2]),
        'ECF':np.array([0,0]),
        'ECP':np.array([-1,+1])+np.array([-1,0]),
        'ECP+EC2P':np.array([0,0]),
        'ECSF':np.array([0,0]),
        'IT':np.array([0,0]),
        'Mg':np.array([0,0]),
        'N':np.array([0,-1]),
        'P':np.array([-1,0]),
        'SF':np.array([0,0]),
        'SF+EC+B+':np.array([0,0]),
        'SF+EC+B-':np.array([0,0]),
        '{+22}Ne':np.array([0,0]),
        '{+24}Ne':np.array([0,0]),
        '{+25}Ne':np.array([0,0]),
        '{+34}Si':np.array([0,0]),
        '|b{+-}fission':np.array([0,0])
        }

	def find_daughters(self):
		df = self.df
		isotopes_dic = self.isotopes_dic
		decays = self.decays
		#Putting the decay modes in a vector
		x_1 = df['decay_1'].values
		x_2 = df['decay_2'].values
		x_3 = df['decay_3'].values
		#Size of the dataframe
		l = len(df)
		#Translating each decay mode vector with the decay dictionary, putting them into a list, then transforming into numpy 2D array and operating it with the dataframe z and n columns to find the new z and n values after decay
		y_1 = df[['z','n']].values + np.array([decays[x_1[i]] for i in range(0,l)])
		y_2 = df[['z','n']].values + np.array([decays[x_2[i]] for i in range(0,l)])
		y_3 = df[['z','n']].values + np.array([decays[x_3[i]] for i in range(0,l)])
		#Now discovering the new symbol of the daughter isotope with the same method
		s_1 = np.array([isotopes_dic[y_1[i,0]] for i in range(0,l)])
		s_2 = np.array([isotopes_dic[y_2[i,0]] for i in range(0,l)])
		s_3 = np.array([isotopes_dic[y_3[i,0]] for i in range(0,l)])
		#Now creating a new column with the (Z+N)Symbol notation
		a_1 = np.char.add(y_1.sum(axis=1).astype(str),s_1)
		a_2 = np.char.add(y_2.sum(axis=1).astype(str),s_2)
		a_3 = np.char.add(y_3.sum(axis=1).astype(str),s_3)
		#Now putting them in the dataframe
		df['decay_daughter_1'] = a_1
		df['decay_daughter_2'] = a_2
		df['decay_daughter_3'] = a_3
		#Doing the same with the parent isotope
		df['A']=(df['z']+df['n']).astype(str) + df['symbol']
		#Pointing the half_life_sec as 0 for all the stable isotopes
		df.loc[df['half_life']=='STABLE','half_life_sec']=0
		#Putting only the relevant columns in a new dataframe
		df2 = df[['A','half_life_sec','decay_daughter_1','decay_1','decay_1_%','decay_daughter_2','decay_2','decay_2_%','decay_daughter_3','decay_3','decay_3_%']]
		df2['half_life_sec'] = pd.to_numeric(df2['half_life_sec'],errors='coerce').fillna(0)
		#Making all the decay %s numeric
		nams = ['decay_1_%','decay_2_%','decay_3_%']
		for i in nams:
			#If the field is empty, then we coerce it to be Nan
			df2[i]=pd.to_numeric(df2[i],errors='coerce')/100
		#We make the (Z+N)Sy notation the index
		df2 = df2.set_index('A')
		#Transposing it for simplicity
		df2 = df2.T
		self.df_daughters = df2
		return df2

	def chain(iso,decay_list,df2):#iso has to follow the notation, with uppercase
		#decay_list = list()#This is the list of the isotopes in the chain
		decay_list.append(iso)#First we append the mother isotope
		#Iso - A + Symbol  (Uppercase)
		daug_1 = df2[iso].decay_daughter_1#Getting the daughter isotopes listed
		daug_2 = df2[iso].decay_daughter_2
		daug_3 = df2[iso].decay_daughter_3
		if daug_1!=iso:#If the isotope repeat -> No decay
			decay_list.append(daug_1)#We append this isotope
			chain_finder.chain(daug_1,decay_list,df2)#We do recursion here
		if daug_2!=iso:
			decay_list.append(daug_2)
			chain_finder.chain(daug_2,decay_list,df2)
		if daug_3!=iso:
			decay_list.append(daug_3)
			chain_finder.chain(daug_3,decay_list,df2)
		return np.unique(np.array(decay_list))#Returning all the isotopes

	def parents(iso,df2):
		df2 = df2.T
		decay_list = list()#This is the list of the isotopes in the chain
		#Iso - A + Symbol  (Uppercase)
		fat_1 = list(df2.loc[df2['decay_daughter_1']==iso,'decay_daughter_1'].index)
		# per_1 = list(df2.loc[df2['decay_daughter_1']==iso,'decay_1_%'])
		fat_2 = list(df2.loc[df2['decay_daughter_2']==iso,'decay_daughter_2'].index)
		fat_3 = list(df2.loc[df2['decay_daughter_3']==iso,'decay_daughter_3'].index)
		fin = np.unique(np.array(fat_1+fat_2+fat_3))#Returning all the isotopes
		return np.delete(fin,np.where(fin==iso)[0])

	def daughters(iso,df2):
		decay_list = []
				#Iso - A + Symbol  (Uppercase)
		daug_1 = df2[iso].decay_daughter_1#Getting the daughter isotopes listed
		daug_2 = df2[iso].decay_daughter_2
		daug_3 = df2[iso].decay_daughter_3
		if daug_1!=iso:#If the isotope repeat -> No decay
			decay_list.append(daug_1)#We append this isotope
		if daug_2!=iso:
			decay_list.append(daug_2)
		if daug_3!=iso:
			decay_list.append(daug_3)
		return np.unique(np.array(decay_list))#Returning all the isotopes

	def plot_chain(iso):
		import networkx as nx
		import matplotlib.pyplot as plt
		fig,ax=plt.subplots()
		g = nx.DiGraph()
		#g.add_nodes_from([1,2,3,4,5,6,7])
		f = chain_finder()
		df2 = f.find_daughters()
		iso_list = chain_finder.chain(iso,[],df2)
		# color_map=[]
		for i in iso_list:
			daug_list = chain_finder.daughters(i,df2)
			if len(daug_list)!=0:
				for j in daug_list:
					g.add_edge(i, j)
					# color_map.append('white')
		# nx.draw(g,pos,with_labels=True)
		# nx.draw_circular(g,with_labels=True)
		# nx.draw_planar(g,with_labels=True)
		# nx.draw_random(g,with_labels=True)
		# nx.draw_spectral(g,with_labels=True)
		# nx.draw_spring(g,with_labels=True)
		ax = nx.draw_shell(g,with_labels=True,node_size=0.1, font_size=5, node_color="skyblue", node_shape="s", alpha=0.9, width=0.5, linewidths=40, edge_color="skyblue", style="solid")
		#plt.draw()
		#plt.show()
		return fig


def bateman_matrix(iso,export_csv=False):
	f = chain_finder()
	df2 = f.find_daughters()
	decay_list = chain_finder.chain(iso,[],df2)
	if decay_list[0]==iso:
		print('No decay chain for this isotope')
		return
	l = len(decay_list)
	df3 = pd.DataFrame(np.zeros((l,l)),index=decay_list,columns=decay_list)
	for i in decay_list:
		t_1_2 = df2[i]['half_life_sec']
		if t_1_2!=0:
			#Self decay
			df3[i][i]=-1*np.log(2)/t_1_2
		#Parents isotopes
		pt = chain_finder.parents(i,df2)
		if len(pt)!=0:
			for j in pt:
				if j in decay_list:
					t_1_2 = df2[j]['half_life_sec']
					spawn = 0
					if df2[j]['decay_daughter_1']==i:
						spawn = df2[j]['decay_1_%']
					elif df2[j]['decay_daughter_2']==i:
						spawn = df2[j]['decay_2_%']
					elif df2[j]['decay_daughter_3']==i:
						spawn = df2[j]['decay_3_%']
					df3[i][j]=spawn*np.log(2)/t_1_2

	if export_csv==True:
		#self.bateman_matrix = df3.T
		df3.T.to_excel(iso+'-bateman.xlsx')
	return df3.T
