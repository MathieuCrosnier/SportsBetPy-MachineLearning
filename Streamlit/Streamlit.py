# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 11:51:36 2022

@author: matcr
"""

import streamlit as st
import Description
import Simulation
from load_css import local_css
local_css("style.css")

PAGES = {"Description" : Description , "Simulation de paris sportifs" : Simulation}

st.sidebar.title('SportsBetPy')
selection = st.sidebar.radio("Sélectionner une page :", PAGES.keys())
page = PAGES[selection]
page.app()