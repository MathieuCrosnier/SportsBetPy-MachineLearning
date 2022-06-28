# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 22:03:33 2022

@author: matcr
"""

def app():
    import streamlit as st
    
    st.image("Image.jpg")
    
    st.header("Guide d'utilisation")
  
    text = """
    <p , class = 'justify'>
    SportsBetPy vous offre 10€ afin que vous puissiez commencer à effectuer des paris.<br>Si jamais votre solde devient nul, il vous faudra recharger votre compte.
    
    1. Choisissez un unique match à parier en sélectionnant dans l'ordre :
        
        * Le championnat concerné,
        
        * L'équipe à domicile,
        
        * L'équipe à l'extérieur,
        
        * La date du match, s'il reste plusieurs matchs possibles.
    
    Les matches proposés sont ceux de la saison 2020-2021, qui correspond à notre jeu de données de test.
        
    2. Choisissez le modèle de Machine Learning qui calculera les cotes.
    
    3. Choisissez la mise de votre pari.
    
    4. Effectuez votre pari.<br>Pour cela, sélectionnez une cote parmi celles proposées par le bookmaker en cliquant sur le bouton correspondant.<br>Selon les cotes calculées par l'algorithme, une indication sur les Value Bets vous est proposée :
        
        * <p><span , class = 'greentext'>Vert foncé</span> : C'est un Value Bet.<br>S'il y a plusieurs Value Bets pour le même match, il s'agit du meilleur Value Bet.
        
        * <p><span , class = 'lightgreentext'>Vert clair</span> : C'est un Value Bet.<br>S'il y a plusieurs Value Bets pour le même match, il ne s'agit pas du meilleur Value Bet.
           
        * <p><span , class = 'redtext'>Rouge</span> : Ce n'est pas un Value Bet.</p>
            
    5. Obtenez le résultat de votre pari.<br>Plusieurs informations s'affichent :
        
        * Le score final du match,
        
        * Le résultat de votre pari,
        
        * Les gains associés à votre pari,
        
        * La courbe des gains cumulés sur l'ensemble de vos paris,
        
        * Le montant de vos gains totaux sur l'ensemble de vos paris.
        
    Amusez-vous bien !
    </p>
            """
    st.markdown(text , unsafe_allow_html = True)