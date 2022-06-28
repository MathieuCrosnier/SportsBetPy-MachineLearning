# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 12:27:03 2022

@author: matcr
"""

import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html = True)