from collections import Counter
import base64
import pandas as pd
from io import BytesIO
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import plotly.express as px
from chatvisualizer import  dfmain, emoji_df




def chart1(df):
    """Generate time series figure chart."""
    date_df = df.groupby("Date").sum()
    date_df.reset_index(inplace=True)
    fig = px.line(date_df, x="Date", y="Word's", title='Number of Words as time moves on.')
    fig.update_xaxes(nticks=20)
    return fig



def chart2(df):
    fig = px.pie(emoji_df, values='count', names='emoji',
             title='Emoji Distribution')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig



def dayofweek(i):
  l = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
  return l[i];

def chart3(df):
    """Daywise Distribution"""
    day_df=pd.DataFrame(df["Message"])
    day_df['day_of_date'] = df['Date'].dt.weekday
    day_df['day_of_date'] = day_df["day_of_date"].apply(dayofweek)
    day_df["messagecount"] = 1
    day = day_df.groupby("day_of_date").sum()
    day.reset_index(inplace=True)

    fig = px.line_polar(day, r='messagecount', theta='day_of_date', line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0,250]
        )),
    showlegend=False
    )
    return fig


def chart4(df):
    """Generate WordCloud."""
    text = " ".join(review for review in df.Message).strip()
    list_words = text.lower().split(" ")
    stopwords = set(STOPWORDS)
    counter = dict(Counter(list_words))
    counter = {key: counter[key] for key in counter if key not in stopwords and key.isalpha()}
    wc = WordCloud(stopwords=stopwords, prefer_horizontal=0.9, colormap='tab10', background_color='white', min_font_size=10, width=1000, height=250, scale=2)
    wc_img = wc.generate_from_frequencies(frequencies=counter).to_image()
    with BytesIO() as buffer:
        wc_img.save(buffer, 'png')
        img = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()
    return img



def chart5(df):
    """Most happening Days."""
    vr = df['Date'].value_counts().to_frame().head(10)
    # Barplot
    fig = px.bar(vr, 
             y='Date', 
             color="Date",
             labels = {'index' : 'Date', 'Date' : 'Number of Messages'},
             title = "Most happening Days"
            )
    return fig




def chart6(df):
    """When are group members Most active?."""
    vr = df['Time'].value_counts().to_frame().head(10)
    # Barplot
    fig = px.bar(vr, 
             y='Time', 
             color="Time",
             labels = {'index' : 'Time', 'Time' : 'Number of Messages'},
             title = "Most Active Times"
            )
    return fig



def chart7(df):
    """Most Active Author in the Group."""
    vr = df['Author'].value_counts().to_frame().head(10)
    # Barplot
    fig = px.bar(vr, 
             y='Author', 
             color="Author",
             labels = {'index' : 'Authors', 'Author' : 'No. Of Messages'},
             title = "Most Active Members of the Group."
            )
    return fig



def chart8(df):
    """Most active day in the week."""
    vr = df['Day'].value_counts().to_frame().head(10)
    # Barplot
    fig = px.bar(vr, 
             y='Day', 
             color="Day",
             labels = {'index' : 'Day', 'Day' : 'No. Of Messages'},
             title = "Mostly active day of Week in the Group"
            )
    return fig


def chart9(df):
    """Top-10 media contributor of Group."""
    mm = df[df['Message'] == r' <Media omitted>']
    vr = mm['Author'].value_counts().to_frame().head(10)
    # Barplot
    fig = px.bar(vr, 
             y='Author', 
             color="Author",
             labels = {'index' : 'Author', 'Author' : 'No. Of Messages'},
             title = "Top-10 media contributor of Group"
            )
    return fig





