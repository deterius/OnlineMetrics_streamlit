from altair.vegalite.v4.schema.core import TitleFrame
import pandas as pd
import plotly.express as px


def rolling_window_func(option):
    rolling_window = 7
    if option == 'Date':
        rolling_window = 7
    elif option == 'Week':
        rolling_window = 4
    else:
        rolling_window = 2
        
    return rolling_window


def total_revenue(df_name,option):
    return df_name.groupby([option])['Net Revenue'].sum().sort_index(ascending=False)

#Plot total revenue
def plotter_func(df_plot, title, ytitle):
    fig = px.line(df_plot)
    fig.update_layout(title_text=title, title_x=0.5 )
    fig.update_yaxes(title_text = ytitle)
    return fig

#Complex plot
def complex_plot(df_name, title, yaxis_name, xaxis_name):
    fig_complex = px.line(df_name)
    fig_complex.update_layout(title_text=title, title_x=0.5, xaxis_rangeslider_visible=True, legend=dict(x=0,y=1,traceorder='normal',
    bgcolor = 'rgba(255,255,255,.5)',
    font=dict(size=10,)))
    fig_complex.update_yaxes(title_text = yaxis_name)
    fig_complex.update_xaxes(title_text = xaxis_name)
    return fig_complex

def revenue_per_shop(df_name,option,store_column_name,rev_column_name):
    df_return = pd.crosstab(df_name[option].sort_values(ascending=False), df_name[store_column_name], values=df_name[rev_column_name], aggfunc='sum', ).sort_index(ascending=False)
    df_return.sort_values(by=[option], inplace=True, ascending=False)
    return df_return

#SMA per store
def sma_per_store(df_name, option, store_column_name, rev_column_name, rolling_window):
    df_sma_store = pd.crosstab(df_name[option].sort_values(ascending=False), df_name[store_column_name], values=df_name[rev_column_name], aggfunc='sum', ).sort_index(ascending=False)
    df_sma_store.reset_index(inplace=True)
    df_sma_store.set_index(option, inplace=True)
    sma_col = []
    old_sma_col = df_sma_store.columns
    for c in df_sma_store.columns:
        c = c+' sma'
        sma_col.append(c)
    
    df_sma_store[sma_col] = df_sma_store.loc[:,df_sma_store.columns].rolling(window=rolling_window).mean()
    df_sma_store.drop(columns=df_sma_store.loc[:,old_sma_col].columns.tolist(), inplace=True)
    df_sma_store.dropna(inplace=True)
    return df_sma_store

#SMA per column
def sma_per_col(df_name, time_window):
    df_name = df_name.copy(deep=True)
    for col in df_name.columns:
        df_name[col] = df_name[col].rolling(window=time_window).mean()
    
    
    return df_name