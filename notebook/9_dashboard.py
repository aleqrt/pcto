"""
# Dashboard
Per adattare la dashboard allo scopo di analizzare il dataset relativo ai test di salto effettuati dagli atleti, seguiremo alcuni step che ci permetteranno di raggiungere l'obiettivo.

1. Definizione del problema
L'obiettivo è analizzare i dati dei test di salto per ottenere insight sugli atleti, come la performance media, la consistenza dei risultati, e eventuali tendenze o correlazioni.

2. Proporre possibili soluzioni
Per fare ciò, possiamo:

- Caricare e esaminare il dataset per comprendere la sua struttura.
- Pulire e preparare i dati se necessario.
- Implementare visualizzazioni interattive per esplorare vari aspetti dei test di salto.
- Aggiungere widget per filtrare i dati in base a parametri specifici, come il nome dell'atleta, la data del test, o il tipo di salto.

3. Valutazione della nostra dashboard
Una dashboard di successo dovrebbe:

- Fornire un'interfaccia chiara e intuitiva.
- Visualizzare efficacemente i dati per facilitare l'analisi.
- Offrire interattività per esplorazioni personalizzate dei dati.
- Caricare rapidamente anche con grandi volumi di dati.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Caricamento dei dati (adatta il percorso del file al tuo ambiente)
df = pd.read_excel("notebook/MyJumpLab_MyJump01.xlsx", header=1)

# Personalizzazione dello stile
st.markdown("""
<style>
.big-font {
    font-size:50px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Titolo della dashboard
st.markdown('<p class="big-font">Analisi dei Test di Salto degli Atleti</p>', unsafe_allow_html=True)

# 1. Selezione dell'atleta con opzione per tutti
atleta = st.selectbox('Seleziona un atleta:', ['Tutti gli atleti'] + list(df['Nome'].unique()))

# 2. Selezione del tipo di salto
tipo_salto = st.selectbox('Seleziona il tipo di salto:', ['Tutti i tipi'] + list(df['Tipo di salto'].unique()))

# Filtraggio dei dati
if atleta != 'Tutti gli atleti':
    df = df[df['Nome'] == atleta]
if tipo_salto != 'Tutti i tipi':
    df = df[df['Tipo di salto'] == tipo_salto]

# 3. Visualizzazione dei boxplot relativi al salto
st.markdown('<p class="big-font">Boxplot Altezza Salto per Atleta</p>', unsafe_allow_html=True)
fig = px.box(df, x='Tipo di salto', y='Altezza salto (cm)', color='Nome', title=f'Boxplot Altezza Salto per {atleta}')
st.plotly_chart(fig)

# 4. Grafici aggiuntivi
st.markdown('<p class="big-font">Andamento del Tempo di Volo nel Tempo</p>', unsafe_allow_html=True)
# Conversione della colonna 'Data' in datetime
df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')

# Filtraggio dei dati in base alla selezione dell'utente
if atleta not in 'Tutti gli atleti':
    df_filtrato = df[df['Nome'] == atleta]
else:
    df_filtrato = df

if tipo_salto not in 'Tutti i tipi':
    df_filtrato = df_filtrato[df_filtrato['Tipo di salto'] == tipo_salto]
else:
    df_filtrato = df

# Creazione e visualizzazione del grafico della serie temporale per il tempo di volo
if atleta not in 'Tutti gli atleti' and tipo_salto not in 'Tutti i tipi':
    fig_tempo_volo = px.line(df_filtrato, x='Data', y='Tempo di volo (ms)', color='Nome')
    st.plotly_chart(fig_tempo_volo)
else:
    st.write("Nessun dato disponibile per la selezione corrente.")


# Selezione del tipo di grafico da visualizzare
st.markdown('<p class="big-font">Analisi di altri parametri</p>', unsafe_allow_html=True)
st.markdown('<p>I grafici relativi alla Potenza, Forza e velocità vengono mostrati solo nel caso in cui venga selezionato un particolare tipo di salto</p>', unsafe_allow_html=True)
tipo_grafico = st.selectbox('Seleziona la variabile da analizzare:',
                            ['Forza', 'Potenza', 'Velocità', 'Correlazioni'])

if tipo_grafico in ['Forza', 'Potenza', 'Velocità'] and tipo_salto not in 'Tutti i tipi':
    # Creazione e visualizzazione del grafico della serie temporale per la variabile selezionata
    colonna = f'{tipo_grafico} (N)' if tipo_grafico == 'Forza' else f'{tipo_grafico} (W)' if tipo_grafico == 'Potenza' else f'{tipo_grafico} (m/s)'
    fig_variabile = px.line(df_filtrato, x='Data', y=colonna, color='Nome' if atleta == 'Tutti gli atleti' else None,
                            title=f'Andamento della {tipo_grafico} nel Tempo per {atleta}')
    st.plotly_chart(fig_variabile)
elif tipo_grafico == 'Correlazioni':
    # Selezione delle variabili da includere nell'analisi delle correlazioni
    variabili_correlazione = ['Altezza salto (cm)', 'Tempo di volo (ms)', 'Forza (N)', 'Potenza (W)', 'Velocità (m/s)']
    df_correlazione = df_filtrato[variabili_correlazione].dropna()

    # Calcolo della matrice di correlazione
    matrice_correlazione = df_correlazione.corr().round(2)

    # Visualizzazione heatmap della matrice di correlazione
    fig_heatmap = px.imshow(matrice_correlazione, text_auto=True,
                            labels=dict(x='Variabile', y='Variabile', color='Correlazione'),
                            title=f'Heatmap di Correlazione tra le Variabili {atleta}')
    st.plotly_chart(fig_heatmap)


# Creazione di un grafico a dispersione per esplorare la correlazione tra l'altezza del box e il tempo di volo
st.markdown('<p class="big-font">Altezza del Box vs Tempo di Volo</p>', unsafe_allow_html=True)

# Filtraggio dei dati per rimuovere eventuali valori mancanti che potrebbero influenzare l'analisi
df_correlazione = df.dropna(subset=['Altezza del box (m)', 'Tempo di volo (ms)'])

# Creazione del grafico
fig_correlazione = px.scatter(df_correlazione, x='Altezza del box (m)', y='Tempo di volo (ms)',
                              color='Nome',
                              title=f'Grafico Altezza del Box vs Tempo di Volo per {atleta}')

# Mostra il grafico nella dashboard
st.plotly_chart(fig_correlazione)
