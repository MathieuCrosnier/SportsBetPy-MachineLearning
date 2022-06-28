# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 12:30:55 2022

@author: matcr
"""

def app():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import joblib
    import sys
    from sklearn.preprocessing import StandardScaler
    
    sys.tracebacklimit = 0
    
    if "bankroll" not in st.session_state:
        st.session_state["bankroll"] = 10
    
    if "gains" not in st.session_state:
        st.session_state["gains"] = [0]    
    
    st.title("Simulation de paris sportifs")
    st.title("💶 : " + str(st.session_state["bankroll"]) + "€")
    
    if st.session_state["bankroll"] == 0:
        st.subheader("💳 Combien voulez-vous déposer ?")
        depot = st.number_input("Montant du dépot (€)")
        st.session_state["bankroll"] += depot

    if st.session_state["bankroll"] == 0:
        st.markdown("<p , class = 'bold redtext big'>Veuillez recharger votre compte</p>" , unsafe_allow_html = True)
        raise ValueError
    
    df = pd.read_csv("Jeu de données pour Streamlit.csv" , index_col = 0)
       
    df_temp = df[df["Season"] == "2020-2021"]
       
    st.subheader("⚽ Veuillez choisir votre match")
    
    division_selected = st.selectbox("Championnat :" , options = [""] + list(df_temp["Division"].unique()))          
    if division_selected != "":
        df_temp = df_temp[df_temp["Division"] == division_selected]
        
    home_team_selected = st.selectbox("Équipe à domicile :" , options = [""] + list(df_temp["Home team"].unique()))
    if home_team_selected != "":
        df_temp = df_temp[df_temp["Home team"] == home_team_selected]
    
    away_team_selected = st.selectbox("Équipe à l'extérieur :" , options = [""] + list(df_temp["Away team"].unique()))
    if away_team_selected != "":
        df_temp = df_temp[df_temp["Away team"] == away_team_selected]
    
    date_selected = st.selectbox("Date :" , options = [""] + list(df_temp["Date"].unique()))
    if date_selected != "":
        df_temp = df_temp[df_temp["Date"] == date_selected]
    
    index = df_temp.index

    if len(index) != 1:
        st.markdown("<p , class = 'bold redtext big'>Veuillez ne sélectionner qu'un seul match</p>" , unsafe_allow_html = True)
        raise ValueError
    
    st.write(df_temp[["Date" , "Division" , "Home team" , "Away team"]])
       
    X = df.drop(columns = ["Season" , "Division" , "Date" , "Home team" , "Away team" , "FTHG" , "FTAG" , "FTR" , "Max H" , "Max D" , "Max A"])
    y = df["FTR"]
    
    X_train = X[df["Season"] != "2020-2021"]
    X_test = X[df["Season"] == "2020-2021"]
    y_train = y[df["Season"] != "2020-2021"]
    y_test = y[df["Season"] == "2020-2021"]
    
    scaler = StandardScaler().fit(X_train)
    X_train_scaled = pd.DataFrame(scaler.transform(X_train) , index = X_train.index , columns = X_train.columns) 
    X_test_scaled = pd.DataFrame(scaler.transform(X_test) , index = X_test.index , columns = X_test.columns)
    
    best_rf = joblib.load("best_rf.pkl")
    best_svc = joblib.load("best_svc.pkl")
    best_knn = joblib.load("best_knn.pkl")
    best_xgb = joblib.load("best_xgb.pkl")
    best_rfh = joblib.load("best_rfh.pkl")
    vc = joblib.load("vc.pkl")
    
    options = ["KNN" , "Random Forest Classifier" , "SVC" , "XGBoost" , "Random Forest Classifier (hyperopt)" , "Voting Classifier"]
    models = {"Random Forest Classifier" : best_rf ,
              "SVC" : best_svc ,
              "KNN" : best_knn ,
              "XGBoost" : best_xgb ,
              "Random Forest Classifier (hyperopt)" : best_rfh , 
              "Voting Classifier" : vc}
    
    st.subheader("💻 Veuillez choisir votre modèle")
    
    option = st.selectbox("Modèle :" , options = options)
    
    model = models[option]
    
    y_probs = model.predict_proba(X_test_scaled.loc[index])
    
    df_gain = df.loc[index , ["Max H" , "Max D" , "Max A"]]
    df_gain = df_gain.rename(columns = {"Max H" : "Cote réelle H" , "Max D" : "Cote réelle D" , "Max A" : "Cote réelle A"})
    df_gain[["Cote calculée A" , "Cote calculée D" , "Cote calculée H"]] = 1 / y_probs
    df_gain = df_gain[["Cote réelle H" , "Cote calculée H" , "Cote réelle D" , "Cote calculée D" , "Cote réelle A" , "Cote calculée A"]]
    df_gain["Ecart H"] = 100 * (df_gain["Cote réelle H"] - df_gain["Cote calculée H"]) / df_gain["Cote réelle H"]
    df_gain["Ecart D"] = 100 * (df_gain["Cote réelle D"] - df_gain["Cote calculée D"]) / df_gain["Cote réelle D"]
    df_gain["Ecart A"] = 100 * (df_gain["Cote réelle A"] - df_gain["Cote calculée A"]) / df_gain["Cote réelle A"]
    df_gain["Résultat"] = y_test[index]    
    
    st.subheader("💶 Veuillez choisir votre mise")
    
    mise = st.number_input("Montant de la mise (€)" , step = 0.5 , value = 1.0 , min_value = 0.0 , max_value = float(st.session_state["bankroll"]))
    
    for i in index:
        
        st.subheader("⚽ " + str(df.loc[i , "Home team"]) + " :vs: " + str(df.loc[i , "Away team"]))
        
        max_ecart = df_gain.loc[i , ["Ecart H" , "Ecart D" , "Ecart A"]].max()
  
        if df_gain.loc[i , "Ecart H"] == max_ecart:
            df_gain.loc[i , "Pari conseillé"] = "H"
            df_gain.loc[i , "Ecart"] = df_gain.loc[i , "Ecart H"]
        elif df_gain.loc[i , "Ecart D"] == max_ecart:
            df_gain.loc[i , "Pari conseillé"] = "D"
            df_gain.loc[i , "Ecart"] = df_gain.loc[i , "Ecart D"]
        elif df_gain.loc[i , "Ecart A"] == max_ecart:
            df_gain.loc[i , "Pari conseillé"] = "A"
            df_gain.loc[i , "Ecart"] = df_gain.loc[i , "Ecart A"]
            
        col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([0.6 , 0.05 , 0.2 , 0.2 , 0.2 , 0.4 , 0.4])

        with col1:
            st.markdown("<p , class = 'align underline bold'>Résultat :</p>" , unsafe_allow_html = True)
            st.markdown("<p , class = 'align underline bold'>Cotes bookmakers :</p>" , unsafe_allow_html = True)
            st.markdown("<p , class = 'underline bold'>Cotes calculées :</p>" , unsafe_allow_html = True)

        with col2:
            pass
        
        with col3:
            st.markdown("<p , class = 'center'>H</p>" , unsafe_allow_html = True)
            bouton_H = st.button(str(df_gain.loc[i , "Cote réelle H"]))
            if (df_gain.loc[i , "Ecart H"] >= 0) and (df_gain.loc[i , "Pari conseillé"] == "H"):
                st.markdown("<p , class = 'center greenback'>" + str(round(df_gain.loc[i , "Cote calculée H"] , 2)) + "</p>" , unsafe_allow_html = True)
            elif df_gain.loc[i , "Ecart H"] >= 0:
                st.markdown("<p , class = 'center lightgreenback'>" + str(round(df_gain.loc[i , "Cote calculée H"] , 2)) + "</p>" , unsafe_allow_html = True)
            else:
                st.markdown("<p , class = 'center redback'>" + str(round(df_gain.loc[i , "Cote calculée H"] , 2)) + "</p>" , unsafe_allow_html = True)
        
        with col4:
            st.markdown("<p , class = 'center'>D</p>" , unsafe_allow_html = True)
            bouton_D = st.button(str(df_gain.loc[i , "Cote réelle D"]))
            if (df_gain.loc[i , "Ecart D"] >= 0) and (df_gain.loc[i , "Pari conseillé"] == "D"):
                st.markdown("<p , class = 'center greenback'>" + str(round(df_gain.loc[i , "Cote calculée D"] , 2)) + "</p>" , unsafe_allow_html = True)
            elif df_gain.loc[i , "Ecart D"] >= 0:
                st.markdown("<p , class = 'center lightgreenback'>" + str(round(df_gain.loc[i , "Cote calculée D"] , 2)) + "</p>" , unsafe_allow_html = True)
            else:
                st.markdown("<p , class = 'center redback'>" + str(round(df_gain.loc[i , "Cote calculée D"] , 2)) + "</p>" , unsafe_allow_html = True)
        
        with col5:
            st.markdown("<p , class = 'center'>A</p>" , unsafe_allow_html = True)
            bouton_A = st.button(str(df_gain.loc[i , "Cote réelle A"]))
            if (df_gain.loc[i , "Ecart A"] >= 0) and (df_gain.loc[i , "Pari conseillé"] == "A"):
                st.markdown("<p , class = 'center greenback'>" + str(round(df_gain.loc[i , "Cote calculée A"] , 2)) + "</p>" , unsafe_allow_html = True)
            elif df_gain.loc[i , "Ecart A"] >= 0:
                st.markdown("<p , class = 'center lightgreenback'>" + str(round(df_gain.loc[i , "Cote calculée A"] , 2)) + "</p>" , unsafe_allow_html = True)
            else:
                st.markdown("<p , class = 'center redback'>" + str(round(df_gain.loc[i , "Cote calculée A"] , 2)) + "</p>" , unsafe_allow_html = True)
                
        with col6:
            pass

        with col7:
            pass
        
        if bouton_H:
            df_gain.loc[i , "Pari"] = "H"
        elif bouton_D:
            df_gain.loc[i , "Pari"] = "D"
        elif bouton_A:
            df_gain.loc[i , "Pari"] = "A"
        else:
            st.markdown("<p , class = 'bold redtext big'>Veuillez effectuer votre pari en cliquant sur l'une des cotes</p>" , unsafe_allow_html = True)
            raise(ValueError)
      
        st.subheader("Score final : ")
        st.write("⚽ " + str(df.loc[i , "Home team"]) + " " + str(int(df.loc[i , "FTHG"])) + " - " + str(int(df.loc[i , "FTAG"])) + "   " + str(df.loc[i , "Away team"]))
        
        st.subheader("Résultat du pari :")        
        if df_gain.loc[i , "Résultat"] == df_gain.loc[i , "Pari"]:
            if df_gain.loc[i , "Résultat"] == "H":
                df_gain.loc[i , "Gain"] = mise * (df_gain.loc[i , "Cote réelle H"] - 1)
            elif df_gain.loc[i , "Résultat"] == "D":
                df_gain.loc[i , "Gain"] = mise * (df_gain.loc[i , "Cote réelle D"] - 1)
            elif df_gain.loc[i , "Résultat"] == "A":
                df_gain.loc[i , "Gain"] = mise * (df_gain.loc[i , "Cote réelle A"] - 1)
            st.write("🤑 Bravo, vous avez remporté votre pari !")
            st.subheader("Gains :")
            st.write("🤑 Vous avez gagné {:.2f} € !".format(df_gain.loc[i , "Gain"]))
        else:
            df_gain.loc[i , "Gain"] = -mise
            st.write("😭 Désolé, vous avez perdu votre pari...")
            st.subheader("Gains :")
            st.write("😭 Vous avez perdu {} €...".format(-df_gain.loc[i , "Gain"]))
        
        st.session_state["bankroll"] += df_gain.loc[i , "Gain"]
        st.session_state["bankroll"] = round(st.session_state["bankroll"] , 2)
        st.session_state["gains"].append(df_gain.loc[i , "Gain"])
        
        st.subheader("Courbe des gains cumulés :")
        
        fig , ax = plt.subplots(figsize = (15 , 10))
        ax.plot(range(0 , len(st.session_state["gains"])) , np.cumsum(st.session_state["gains"]))
        ax.set_xticks(range(0 , len(st.session_state["gains"])))
        ax.set_xlabel("Nombre de paris effectués" , fontsize = "x-large")
        ax.set_ylabel("Gains cumulés" , fontsize = "x-large")  
        min_cumsum = min(np.cumsum(st.session_state["gains"]))
        max_cumsum = max(np.cumsum(st.session_state["gains"]))
        ax.set_xlim(0 , len(np.cumsum(st.session_state["gains"])) - 1)
        ax.set_ylim(int(min_cumsum) - 1 , int(max_cumsum) + 1)
        step_x_temp = len(np.cumsum(st.session_state["gains"])) // 10
        if step_x_temp == 0:
            step_x = 1
        else:
            step_x = step_x_temp
        step_y_temp = int((max_cumsum - min_cumsum + 3) // 10)
        if step_y_temp == 0:
            step_y = 1
        else:
            step_y = step_y_temp
        ax.set_xticks(range(0 , len(np.cumsum(st.session_state["gains"])) - 1 + step_x , step_x))
        ax.set_yticks(range(int(min_cumsum) - 1 , int(max_cumsum) + 1 + step_y , step_y))
        st.pyplot(fig)
        
        st.subheader("Vos gains totaux s'élèvent à {:.2f} €".format(np.cumsum(st.session_state["gains"])[-1]))