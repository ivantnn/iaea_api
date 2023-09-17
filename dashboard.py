import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st
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

#Mode = st.selectbox("Select the data type to be imported", ('Ground States','Levels','Gammas','Cummulative','Decay Radiations'))

isotopes_dic={1:'H',2:'He',3:'Li',4:'Be',5:'B',6:'C',7:'N',8:'O',9:'F',10:'Ne',11:'Na',12:'Mg',13:'Al',14:'Si',15:'P',16:'S',17:'Cl',18:'Ar',19:'K',20:'Ca',21:'Sc',22:'Ti',23:'V',24:'Cr',25:'Mn',26:'Fe',27:'Co',28:'Ni',29:'Cu',30:'Zn',31:'Ga',32:'Ge',33:'As',34:'Se',35:'Br',36:'Kr',37:'Rb',38:'Sr',39:'Y',40:'Zr',41:'Nb',42:'Mo',43:'Tc',44:'Ru',45:'Rh',46:'Pd',47:'Ag',48:'Cd',49:'In',50:'Sn',51:'Sb',52:'Te',53:'I',54:'Xe',55:'Cs',56:'Ba',57:'La',58:'Ce',59:'Pr',60:'Nd',61:'Pm',62:'Sm',63:'Eu',64:'Gd',65:'Tb',66:'Dy',67:'Ho',68:'Er',69:'Tm',70:'Yb',71:'Lu',72:'Hf',73:'Ta',74:'W',75:'Re',76:'Os',77:'Ir',78:'Pt',79:'Au',80:'Hg',81:'Tl',82:'Pb',83:'Bi',84:'Po',85:'At',86:'Rn',87:'Fr',88:'Ra',89:'Ac',90:'Th',91:'Pa',92:'U',93:'Np',94:'Pu',95:'Am',96:'Cm',97:'Bk',98:'Cf',99:'Es',100:'Fm',101:'Md',102:'No',103:'Lr',104:'Rf',105:'Db',106:'Sg',107:'Bh',108:'Hs',109:'Mt',110:'Ds',111:'Rg',112:'Cn',113:'Nh',114:'Fl',115:'Mc',116:'Lv',117:'Ts',118:'Og',}

api_dic={1:'h',2:'he',3:'li',4:'be',5:'b',6:'c',7:'n',8:'o',9:'f',10:'ne',11:'na',12:'mg',13:'al',14:'si',15:'p',16:'s',17:'cl',18:'ar',19:'k',20:'ca',21:'sc',22:'ti',23:'v',24:'cr',25:'mn',26:'fe',27:'co',28:'ni',29:'cu',30:'zn',31:'ga',32:'ge',33:'as',34:'se',35:'br',36:'kr',37:'rb',38:'sr',39:'y',40:'zr',41:'nb',42:'mo',43:'tc',44:'ru',45:'rh',46:'pd',47:'ag',48:'cd',49:'in',50:'sn',51:'sb',52:'te',53:'i',54:'xe',55:'cs',56:'ba',57:'la',58:'ce',59:'pr',60:'nd',61:'pm',62:'sm',63:'eu',64:'gd',65:'tb',66:'dy',67:'ho',68:'er',69:'tm',70:'yb',71:'lu',72:'hf',73:'ta',74:'w',75:'re',76:'os',77:'ir',78:'pt',79:'au',80:'hg',81:'tl',82:'pb',83:'bi',84:'po',85:'at',86:'rn',87:'fr',88:'ra',89:'ac',90:'th',91:'pa',92:'u',93:'np',94:'pu',95:'am',96:'cm',97:'bk',98:'cf',99:'es',100:'fm',101:'md',102:'no',103:'lr',104:'rf',105:'db',106:'sg',107:'bh',108:'hs',109:'mt',110:'ds',111:'rg',112:'cn',113:'nh',114:'fl',115:'mc',116:'lv',117:'ts',118:'og',}

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Ground States", "Levels", "Gammas","Cummulative","Decay Radiations","About"])

with tab1:
    Mode='ground_states'
    st.header('Import the Ground States')
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
    st.header('Import the cummulative chains')
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
    st.header('Import the decay radiations')
    with st.container():
            col1,col2 = st.columns(2)

            Isotope_z = col1.number_input("Select Z value",min_value=1, max_value=119,key=f"isoz_dr")
            Isotope_n = col2.number_input("Select N value", min_value=1, max_value=176,key=f"ison_dr")
            p = st.selectbox("Mode of the Cummulative",('Alpha','Beta Plus','Beta Minus','Gamma','Electron','X-ray'), key='mode_dr')

            rad_dic={'Alpha':'a','Beta Plus':'bp','Beta Minus':'bm','Gamma':'g','Electron':'e','X-ray':'x'}
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

with tab6:
    st.header("About")
    st.write("This is an amateur and small project to make it easier to import nuclear data from the IAEA database. All information and code used to build this is free and open source")
    url="https://www-nds.iaea.org/relnsd/vcharthtml/api_v0_guide.html"
    st.markdown("The IAEA database is accessed via its API:  [IAEA Api](%s)" % url)
    url3="https://github.com/ivantnn/iaea_api"
    st.markdown("Any question or complaint, check out the github from this project: [My GitHub](%s)" % url3)
