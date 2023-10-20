import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import plotly.figure_factory as ff
import plotly.graph_objs as go
import streamlit as st
import A_dic
import iaea

@st.cache_data
def convert_df_lvls(ref):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    df = iaea.Api.Import('levels',ref,param=None)
    return df.to_csv().encode('utf-8')

@st.cache_data
def convert_df_GS(ref):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    df = iaea.Api.Import('ground_states',ref,param=None)
    return df.to_csv().encode('utf-8')

@st.cache_data
def convert_df_gamma(ref):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    df = iaea.Api.Import('gammas',ref,param=None)
    return df.to_csv().encode('utf-8')

@st.cache_data
def convert_df_cum(ref,p):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    df = iaea.Api.Import('cummulative',ref,param=p)
    return df.to_csv().encode('utf-8')

@st.cache_data
def convert_df_dr(ref,rad):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    df = iaea.Api.Import('decay_rads',ref,param=rad)
    return df.to_csv().encode('utf-8')

st.set_page_config(
    page_title="IAEA Nuclear Database API frontend",
    page_icon="☢️",
    layout="wide",
)

st.title("I want to import some nuclear data")
st.write("Here one can find all the modes to import nuclear data from the IAEA (International Atomic Energy Agency's) database")
st.write("On each tab, one can find all the explanation and the modes for the data")
st.markdown("**Be aware**: Any input is allowed but it might not exist in the IAEA database. As an example, one can try to download a hidrogen isotope with 10 neutrons, but there is no recording of such in the database, thus rendering the downloaded file empty")

#Mode = st.selectbox("Select the data type to be imported", ('Ground States','Levels','Gammas','Cummulative','Decay Radiations'))

isotopes_dic={0:'Nn',1:'H',2:'He',3:'Li',4:'Be',5:'B',6:'C',7:'N',8:'O',9:'F',10:'Ne',11:'Na',12:'Mg',13:'Al',14:'Si',15:'P',16:'S',17:'Cl',18:'Ar',19:'K',20:'Ca',21:'Sc',22:'Ti',23:'V',24:'Cr',25:'Mn',26:'Fe',27:'Co',28:'Ni',29:'Cu',30:'Zn',31:'Ga',32:'Ge',33:'As',34:'Se',35:'Br',36:'Kr',37:'Rb',38:'Sr',39:'Y',40:'Zr',41:'Nb',42:'Mo',43:'Tc',44:'Ru',45:'Rh',46:'Pd',47:'Ag',48:'Cd',49:'In',50:'Sn',51:'Sb',52:'Te',53:'I',54:'Xe',55:'Cs',56:'Ba',57:'La',58:'Ce',59:'Pr',60:'Nd',61:'Pm',62:'Sm',63:'Eu',64:'Gd',65:'Tb',66:'Dy',67:'Ho',68:'Er',69:'Tm',70:'Yb',71:'Lu',72:'Hf',73:'Ta',74:'W',75:'Re',76:'Os',77:'Ir',78:'Pt',79:'Au',80:'Hg',81:'Tl',82:'Pb',83:'Bi',84:'Po',85:'At',86:'Rn',87:'Fr',88:'Ra',89:'Ac',90:'Th',91:'Pa',92:'U',93:'Np',94:'Pu',95:'Am',96:'Cm',97:'Bk',98:'Cf',99:'Es',100:'Fm',101:'Md',102:'No',103:'Lr',104:'Rf',105:'Db',106:'Sg',107:'Bh',108:'Hs',109:'Mt',110:'Ds',111:'Rg',112:'Cn',113:'Nh',114:'Fl',115:'Mc',116:'Lv',117:'Ts',118:'Og'}

api_dic={1:'h',2:'he',3:'li',4:'be',5:'b',6:'c',7:'n',8:'o',9:'f',10:'ne',11:'na',12:'mg',13:'al',14:'si',15:'p',16:'s',17:'cl',18:'ar',19:'k',20:'ca',21:'sc',22:'ti',23:'v',24:'cr',25:'mn',26:'fe',27:'co',28:'ni',29:'cu',30:'zn',31:'ga',32:'ge',33:'as',34:'se',35:'br',36:'kr',37:'rb',38:'sr',39:'y',40:'zr',41:'nb',42:'mo',43:'tc',44:'ru',45:'rh',46:'pd',47:'ag',48:'cd',49:'in',50:'sn',51:'sb',52:'te',53:'i',54:'xe',55:'cs',56:'ba',57:'la',58:'ce',59:'pr',60:'nd',61:'pm',62:'sm',63:'eu',64:'gd',65:'tb',66:'dy',67:'ho',68:'er',69:'tm',70:'yb',71:'lu',72:'hf',73:'ta',74:'w',75:'re',76:'os',77:'ir',78:'pt',79:'au',80:'hg',81:'tl',82:'pb',83:'bi',84:'po',85:'at',86:'rn',87:'fr',88:'ra',89:'ac',90:'th',91:'pa',92:'u',93:'np',94:'pu',95:'am',96:'cm',97:'bk',98:'cf',99:'es',100:'fm',101:'md',102:'no',103:'lr',104:'rf',105:'db',106:'sg',107:'bh',108:'hs',109:'mt',110:'ds',111:'rg',112:'cn',113:'nh',114:'fl',115:'mc',116:'lv',117:'ts',118:'og',}

A_dic = A_dic.A

tab00,tab11,tab22,tab33 = st.tabs(["General","Import Data","Decay Chains Generator","About"])


def hl_list(df):
    df['A']=(df['z']+df['n']).astype(str)+df['symbol']
    df.loc[df['half_life']=='','half_life_sec']=0
    df.loc[df['half_life']==' ','half_life_sec']=0
    df.loc[df['half_life_sec']=='','half_life_sec']=0
    df.loc[df['half_life_sec']==' ','half_life_sec']=0
    df.loc[df['half_life_sec']!=df['half_life_sec'].isna(),'half_life_sec']=pd.to_numeric(df.loc[df['half_life_sec']!=df['half_life_sec'].isna(),'half_life_sec'])
    #df['log_half_life_sec'] = np.log10(df['half_life_sec'],out=np.zeros_like(df['half_life_sec']),where=(df['half_life_sec']!=0))
    return df

with tab00:
    st.header("Half-Life and nuclear data")
    st.title("Half-what?")
    st.markdown("For people who were once chemists before any contact with the nuclear world - *such as myself* - it is difficult to wrap one's mind around this new worlds. For us, there is just one type of uranium, of hydrogen, of oxygen...")
    st.markdown("So when we raise one eyebrow after a nuclear scientist says **'Which isotope?'** is nothing but a natural reaction. It took me some time to remember that the protons orient the name of the element, as the number of neutrons adds to the mass")
    st.markdown("Now, how many protons or neutrons are in a nucleus says a lot about how much time said nucleus can exist - **by reasons intrinsic to the subparticle physics** - such as strong and weak force. As there is no intent on suffering by entering the wild domains of particle physics, one question remains: How much time can this nucleus be?")
    df = hl_list(iaea.Api.Import('ground_states','all'))
    df2 = pd.pivot_table(df,values='half_life_sec',index='z',columns='n',aggfunc="sum").fillna(0)
    log_vals = np.log10(df2,out=np.zeros_like(df2),where=(df2!=0))
    # HLs = 10**df2.values
    # names= np.repeat(list(isotopes_dic.values()), len(df2.columns)).reshape(len(df2.index), len(df2.columns))
    # nk = np.empty(shape=(len(df2.index)*len(df2.columns),2,1), dtype='object')
    # nk[:,0] = np.array(HLs).reshape(-1,1)
    # nk[:,1] = np.array(names).reshape(-1,1)
    graph = st.selectbox("Graph mode",("Half-Life","Decay Type"),key="general_ban")

    decays = {
        np.nan:np.nan,
        '2B+':1,
        '2B-':2,
        '2EC':3,
        '2N':4,
        '2P':5,
        'A':6,
        'B+':7,
        'B+P':8,
        'B-':9,
        'B-2N':10,
        'B-N':11,
        'EC':12,
        'EC+B+':13,
        'ECP':14,
        'ECP+EC2P':15,
        'ECSF':16,
        'IT':17,
        'N':18,
        'P':19,
        'SF':20,
        'B-A':21
        }

    vals = df['decay_1'].replace({' ':np.nan}).values
    df['decay_class'] = [decays[vals[i]] for i in range(0,len(vals))]
    piv=pd.pivot_table(df,values='decay_class',index='z',columns='n',aggfunc='sum')

    if graph == "Half-Life":

        fig1 = px.imshow(log_vals.replace({0:np.nan}),color_continuous_scale='jet',origin='lower')

        fig1.update(data=[{'customdata': np.repeat(list(isotopes_dic.values()), len(df2.columns)).reshape(len(df2.index), len(df2.columns)),'hovertemplate': 'Protons: %{y}<br>Neutrons: %{x}<br>Symbol: %{customdata}<extra></extra>'}])

        fig1.update_layout(coloraxis_colorbar=dict(
        title="Half-Life (s)",
        tickvals=[30,27,24,21,18,15,12,9,6,3,1,-3,-6,-9,-12,-15,-18,-21,-24,-27,-30],
        ticktext=["1e30","1e27","1e24","1e21","1e18","1e15","1e12","1e9","1e6","1e3","1","1e-3","1e-6","1e-9","1e-12","1e-15","1e-18","1e-21","1e-24","1e-27","1e-30"]
        ))

        fig1.update_layout(hovermode="y unified")
        st.plotly_chart(fig1, use_container_width=True)

    elif graph=="Decay Type":
        df.loc[df['half_life']=='STABLE','decay_1']='STABLE'
        df.loc[df['half_life']==' ','decay_1']='unknown'
        df.loc[df['half_life']=='','decay_1']='unknown'
        st.markdown("Hint: Click the legends icons to show/hide some of the decay types!")
        #fig = px.imshow(piv,origin='lower',color_continuous_scale='viridis')
        data = px.scatter(df,x='n',y='z',color='decay_1',
                         hover_data={'decay_1':False,
                                     'z':True,
                                     'n':True,
                                     'Symbol':df['symbol'],
                                     'Decay type':df['decay_1']
                             })

        # fig.update_layout(coloraxis_colorbar=dict(
        # title="Dcay Type",
        # tickvals=[20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1],
        # ticktext=["SF","P","N","IT","ECSF","ECP+EC2P","ECP","EC+B+","EC","B-N","B-2N","B-","B+P","B+","A","2P","2N","2EC","2B-","2B+"]
        # ))
        #fig2.update_layout(legend=dict(text='Decay Type'))
        layout = go.Layout(
            annotations=[
                dict(
                    align="right",
                    valign="top",
                    text='Decay Type',
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    xanchor="center",
                    yanchor="top"
                )
            ]
        )
        fig3 = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("A half-life is the average time on which any given isotope takes to decay half of its mass. Naturally, these decays take several different forms of decay by different mechanisms: Beta-Minus, Beta-Plus, Electron-Capture, Alpha emitting, etc")
    st.markdown("Now, it is pretty interesting to see how much of a difference just the addition or exclusion of a single neutron can do on a single isotope")
    st.title("Data, Data, Data")
    st.markdown("And of course, we can use the data to make some interesting manipulations so we can actually see some cool stuff. For example:")
    #df.loc[df['half_life']=='STABLE','half_life_sec']='STABLE'
    df.loc[df['half_life']=='STABLE','decay_1']='STABLE'
    iso_list = isotopes_dic.values()
    gen2=st.selectbox("Select the nuclear Isotope:",iso_list,key='gen_g2')
    df['sz']=[12]*len(df)
    fig2 = px.scatter(df.loc[df['symbol']==gen2],x='n',y='half_life_sec',color='decay_1',size='sz',log_y=True)

    #Finding the stable ones
    stab = df.loc[(df['symbol']==gen2)&(df['half_life']=='STABLE')]
    stab_len = len(stab)

    if stab_len!=0:
        mx = df.loc[df['symbol']==gen2,'half_life_sec'].max()
        stab['mx']=[mx]*stab_len
        fig2.add_bar(x=stab['n'],y=stab['mx'],text=stab['half_life'],alignmentgroup='n')
            # fig2.add_annotation(x=stab['n'].iloc[i]+0.25,
            #                  y=0.12,
            #                  showarrow=False,
            #                  text="Stable",
            #                  textangle=270,
            #                  xanchor='left',
            #                  xref="paper",
            #                  yref="paper")

    st.plotly_chart(fig2,use_container_width=True)
    st.markdown("Now, nuclear data is data, just like any data, with all its needs of treatment, its inconsistencies and... well, limitations to access. Mainly for a subject so delicate in the discussion - After all, when one says nuclear, everyone seems to remember the horrors of the nuclear arms race, and very few contemplate their medicinal or energetic usages.")
    st.markdown("Luckily for us, the International Agency of Energy makes available a full nuclear database, from which you can (kinda) easily download using the API... or download using this website I made :) You can go to the other tabs and have fun downloading nuclear data from the IAEA itself - in a more interactive way!")


with tab11:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Ground States", "Levels", "Gammas","Cummulative","Decay Radiations"])
    with tab1:
            st.header('Import the Ground States')
            st.markdown('A nucleus can have several excitation levels, which are different levels of energy. These levels can have their own nuclear spin, radius, binding energy, decay type and half life and many more.')
            st.markdown('A Ground State is the lowest energy level on which the nucleus of an atom can exist. Thus its name.')
            st.markdown('*How to use* : Select the desired number of protons and neutrons from the desired isotope and hit **Download (CSV)** to get the data')
            st.markdown('*For Ground States mode only*: IAEA API allows the user to download all the isotopes together in a single table, therefore if you switch on the **Import all the isotopes** option and hit **Download (CSV)** you will get a complete table with all the isotopes and their ground states')
            st.markdown('Note: Some half lifes are in eV, this is due to their very short times. To convert it fully to time one can use the following equation, being gamma the energy you read in the database for these cases:')
            st.latex(r'''T_{1/2}=\frac{\hbar ln(2)}{\Gamma}''')
            col0,col01 = st.columns(2)
            import_all=col0.toggle('Import all the isotopes',key="GS_all")
            if import_all==True:
                st.write('')

                dfs = convert_df_GS('all')
                st.download_button(
                        label='Download (CSV)',
                        #data=iaea.Api.Call('ground_states',ref[i],ref[i]+'_GS',param=None),
                        data = dfs,
                        key=f"dwnld_GS-all",
                        file_name='all_GS.csv',
                        mime='text/csv'
                    )
            else:
                with st.container():
                    col1,col2 = st.columns(2)

                    Isotope_z = col1.number_input("Select Z value",min_value=1, max_value=119,key=f"isoz_GS")
                    Isotope_n = col2.number_input("Select N value", min_value=1, max_value=176,key=f"ison_GS")

                    aa='\huge '+isotopes_dic[Isotope_z]+'^{'+str(Isotope_z)+'}_{'+str(Isotope_n)+'}'

                    ref = str(Isotope_z+Isotope_n)+api_dic[Isotope_z]

                    dfs = convert_df_GS(ref)

                    rest_tex =r'''\begin{cases}
                                Z='''+str(Isotope_z) + r'''
                                \\
                                N='''+str(Isotope_n)+                   r'''\\
                                A=Z+N='''+str(Isotope_n+Isotope_z)+r'''
                            \end{cases}'''
                    st.latex(aa+rest_tex)

                    st.download_button(
                        label='Download (CSV)',
                        #data=iaea.Api.Call('ground_states',ref[i],ref[i]+'_GS',param=None),
                        data = dfs,
                        key=f"dwnld_GS",
                        file_name=ref+'_GS.csv',
                        mime='text/csv'
                    )

    with tab2:
        st.header('Import the Levels')
        st.markdown('A nucleus can have several excitation levels, which are different levels of energy. These levels can have their own nuclear spin, radius, binding energy, decay type and half life and many more.')
        st.markdown('This data lists all the known excitation levels from each known isotope')
        st.markdown('*How to use* : Select the desired number of protons and neutrons from the desired isotope and hit **Download (CSV)** to get the data')
        st.markdown('Note: Some half lifes are in eV, this is due to their very short times. To convert it fully to time one can use the following equation, being gamma the energy you read in the database for these cases:')
        st.latex(r'''T_{1/2}=\frac{\hbar ln(2)}{\Gamma}''')
        with st.container():
                col1,col2 = st.columns(2)

                Isotope_z = col1.number_input("Select Z value",min_value=1, max_value=119,key=f"isoz_Lvls")
                Isotope_n = col2.number_input("Select N value", min_value=1, max_value=176,key=f"ison_Lvls")

                aa='\huge '+isotopes_dic[Isotope_z]+'^{'+str(Isotope_z)+'}_{'+str(Isotope_n)+'}'

                ref = str(Isotope_z+Isotope_n)+api_dic[Isotope_z]

                dfs = convert_df_lvls(ref)

                rest_tex =r'''\begin{cases}
                            Z='''+str(Isotope_z) + r'''
                            \\
                            N='''+str(Isotope_n)+                   r'''\\
                            A=Z+N='''+str(Isotope_n+Isotope_z)+r'''
                        \end{cases}'''
                st.latex(aa+rest_tex)
                st.download_button(
                    label='Download (CSV)',
                    #data=iaea.Api.Call('ground_states',ref[i],ref[i]+'_GS',param=None),
                    data = dfs,
                    key=f"dwnld_Lvs",
                    file_name=ref+'_Lvls.csv',
                    mime='text/csv'
                )


    with tab3:
        st.header('Import the Gamma levels')
        st.markdown('This data lists all the levels of energy which the isotope will emit a photon while also listing the initial and end energy states of the nucleus.')
        st.markdown('*How to use* : Select the desired number of protons and neutrons from the desired isotope and hit **Download (CSV)** to get the data')
        with st.container():
                col1,col2 = st.columns(2)

                Isotope_z = col1.number_input("Select Z value",min_value=1, max_value=119,key=f"isoz_Gam")
                Isotope_n = col2.number_input("Select N value", min_value=1, max_value=176,key=f"ison_Gam")

                aa='\huge '+isotopes_dic[Isotope_z]+'^{'+str(Isotope_z)+'}_{'+str(Isotope_n)+'}'

                ref = str(Isotope_z+Isotope_n)+api_dic[Isotope_z]

                dfs = convert_df_gamma(ref)

                rest_tex =r'''\begin{cases}
                            Z='''+str(Isotope_z) + r'''
                            \\
                            N='''+str(Isotope_n)+                   r'''\\
                            A=Z+N='''+str(Isotope_n+Isotope_z)+r'''
                        \end{cases}'''
                st.latex(aa+rest_tex)
                st.download_button(
                    label='Download (CSV)',
                    #data=iaea.Api.Call('ground_states',ref[i],ref[i]+'_GS',param=None),
                    data = dfs,
                    key=f"dwnld_gam",
                    file_name=ref+'_Gamma.csv',
                    mime='text/csv'
                )
    with tab4:
        st.header('Import the Cummulative chains')
        st.markdown('Given an isotope, this mode lists all the possible products for a specified.')
        st.markdown('''
                    This data has two different modes:

                    - Parents: All the products for the specified parent are returned.

                    - Products: All the fission yields of this product, for any parent, are returned
                    ''')
        st.markdown('*How to use* : Select the desired number of protons and neutrons from the desired isotope. Then select the desired mode (Parents or Products) and hit **Download (CSV)** to get the data')
        with st.container():
                col1,col2 = st.columns(2)

                Isotope_z = col1.number_input("Select Z value",min_value=1, max_value=119,key=f"isoz_Cum")
                Isotope_n = col2.number_input("Select N value", min_value=1, max_value=176,key=f"ison_Cum")
                p = st.selectbox("Mode of the Cummulative",("Parents","Products"), key='mode_cum')

                p_dic={"Parents":"parents","Products":"products"}
                aa='\huge '+isotopes_dic[Isotope_z]+'^{'+str(Isotope_z)+'}_{'+str(Isotope_n)+'}'

                ref = str(Isotope_z+Isotope_n)+api_dic[Isotope_z]

                dfs = convert_df_cum(ref,p_dic[p])

                rest_tex =r'''\begin{cases}
                            Z='''+str(Isotope_z) + r'''
                            \\
                            N='''+str(Isotope_n)+                   r'''\\
                            A=Z+N='''+str(Isotope_n+Isotope_z)+r'''
                        \end{cases}'''
                st.latex(aa+rest_tex)
                st.download_button(
                    label='Download (CSV)',
                    #data=iaea.Api.Call('ground_states',ref[i],ref[i]+'_GS',param=None),
                    data = dfs,
                    key=f"dwnld_cum",
                    file_name=ref+'_'+p_dic[p]+'_.csv',
                    mime='text/csv'
                )

    with tab5:
        st.header('Import the Decay Radiations')
        st.markdown('Given an isotope, this mode lists all the specified radiation decays in the different energy levels.')
        st.markdown(r'''
                    This data lists all the different decay types:

                    - **Alpha**: Emission of 2-proton and 2-neutron particles [Wikipedia](https://en.wikipedia.org/wiki/Alpha_decay)
                    $$
                    U_{146}^{92} -> \alpha^{2}_{2} + Th_{144}^{90}
                    $$
                    - **Beta Minus**: Convertion of the atomic nucleus into a nucleus with atomic number increased by one, while emitting an electron and an electron antineutrino. [Wikipedia](https://en.wikipedia.org/wiki/Beta_decay)
                    $$
                    C_{6}^{8} -> N^{7}_{7} + \bar{\nu}_{e} + e^{{}-{}}
                    $$
                    - **Beta Plus**: Convertion of the atomic nucleus into a nucleus with atomic number increased by one, while emitting a positron and an electron neutrino. Note: Electron Capture is considered within this scope in the IAEA database. [Wikipedia](https://en.wikipedia.org/wiki/Beta_decay)
                    $$
                    C_{6}^{4} -> B^{5}_{5} + \nu_{e} + e^{{}+{}}
                    $$
                    - **Gamma**: It happens when an excited nucleus emits some of its energy (as a gamma particle)in order to return to the ground state or a lower energy state. [Wikipedia](https://en.wikipedia.org/wiki/Gamma_ray)
                    $$
                    Ba_{81}^{{}*{}56} -> Ba^{56}_{81} + \gamma
                    $$

                    - **Auger and conversion electron**: The filling of an inner-shell vacancy of an atom is accompanied by the emission of an electron from the same atom. [Wikipedia](https://en.wikipedia.org/wiki/Auger_effect)

                    - **X-ray**: Lower energy gamma radiation.
                    ''')
        st.markdown('*How to use* : Select the desired number of protons and neutrons from the desired isotope. Then select the desired radiation and hit **Download (CSV)** to get the data')
        with st.container():
                col1,col2 = st.columns(2)

                Isotope_z = col1.number_input("Select Z value",min_value=1, max_value=119,key=f"isoz_dr")
                Isotope_n = col2.number_input("Select N value", min_value=1, max_value=176,key=f"ison_dr")
                p = st.selectbox("Mode of the Cummulative",('Alpha','Beta Plus','Beta Minus','Gamma','Auger and conversion electron','X-ray'), key='mode_dr')

                rad_dic={'Alpha':'a','Beta Plus':'bp','Beta Minus':'bm','Gamma':'g','Auger and conversion electron':'e','X-ray':'x'}
                aa='\huge '+isotopes_dic[Isotope_z]+'^{'+str(Isotope_z)+'}_{'+str(Isotope_n)+'}'

                ref = str(Isotope_z+Isotope_n)+api_dic[Isotope_z]

                dfs = convert_df_dr(ref,rad_dic[p])

                rest_tex =r'''\begin{cases}
                            Z='''+str(Isotope_z) + r'''
                            \\
                            N='''+str(Isotope_n)+                   r'''\\
                            A=Z+N='''+str(Isotope_n+Isotope_z)+r'''
                        \end{cases}'''
                st.latex(aa+rest_tex)
                st.download_button(
                    label='Download (CSV)',
                    #data=iaea.Api.Call('ground_states',ref[i],ref[i]+'_GS',param=None),
                    data = dfs,
                    key=f"dwnld_rd",
                    file_name=ref+'_'+rad_dic[p]+'_.csv',
                    mime='text/csv'
                )
with tab22:
    st.header("Decay Chain generator")
    st.markdown("I always found a little **annoying** to do the decay chains, and that is something that usually it is not inserted in the IAEA database. So I always had to look at that protons vs neutrons graph, see each decay type and list them. Which takes time.")
    st.markdown("Well, as we have full access to the IAEA API, we can fully automatize it now. Check this out:")
    col1,col2,col3 = st.columns(3)

    A = col1.selectbox("Select A value",A_dic.keys(),key=f"dcch_a")
    Symbol = col2.selectbox("Select the symbol",A_dic[A],key=f"dcch_s")
    isotope = str(A)+Symbol
    col3.write('Meaning this isotope-> '+isotope)
    fig = iaea.chain_finder.plot_chain(isotope)
    st.pyplot(fig)
    st.markdown("Why does this matter? Well, when you are calculating the inventory or behavior of the decay of a certain isotope, that is annoying. Because the decay is a property of the nucleus of the isotope, therefore it only depends on itself. In *mafs*, we list it like that:")
    st.latex("{dN_{i} \over {dt}} = -\lambda_{i}*N_{i}")
    st.markdown("That means that the quantity of said isotope depends, with respect to time, to a constant called lambda. Now what is this constant? Well, that is related to the half-life:")
    st.latex("\lambda = {{ln(2)} \over {t_{1/2}}}")
    st.markdown("That is for each and every isotope")
    st.markdown("Now, that is not the whole picture, as other isotopes may decay into the ones we are studying. So, the full equation (for decay) is:")
    st.latex("{dN_{i} \over {dt}} = -\lambda_{i}*N_{i} + \sum{\lambda_{j}*N_{j}}")
    st.markdown("Since we are talking about multiple isotopes, that means:")
    st.latex(r'''
            \begin{bmatrix}
            -\lambda_{1} & 0 & 0 & ... & 0 \\
            \lambda_{1} & \lambda_{2} & 0 & ... & 0 \\
            ... & ... & ... & ... & ... \\
            0 & 0 & 0  & ... & 0
            \end{bmatrix}
            ''')
    st.write("I always hated doing the Bateman matrix - man that took so much time! You have to check each and every line and column to see if the matrix is properly done, otherwise you get results that are bonkers.")
    st.write("At last, we do a numerical integration with this matrix and initial conditions. But that is a subject for another time...")
    st.write("But fear the matrix no more! I did a small routine to automatize that. Click below to import the matrix: ")

    @st.cache_data
    def convert_df_bateman(isotope):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        df_bateman = iaea.bateman_matrix(isotope,export_csv=False)
        return df_bateman.to_csv().encode('utf-8')

    df_bateman = convert_df_bateman(isotope)

    st.download_button(
                    label='Download (CSV)',
                    #data=iaea.Api.Call('ground_states',ref[i],ref[i]+'_GS',param=None),
                    data = df_bateman,
                    key=f"dcch_dwn",
                    file_name=isotope+'_'+'Bateman_decay_.csv',
                    mime='text/csv'
                )

with tab33:
    st.header("About")
    st.write("This is an amateur and small project to make it easier to import nuclear data from the IAEA database. All information and code used to build this is free and open source")
    url="https://www-nds.iaea.org/relnsd/vcharthtml/api_v0_guide.html"
    st.markdown("The IAEA database is accessed via its API:  [IAEA Api](%s)" % url)
    url3="https://github.com/ivantnn/iaea_api"
    st.markdown("Any question or complaint, check out the github from this project: [My GitHub](%s)" % url3)
