import pandas as pd
import os
import re
#import seaborn as sns
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.pyplot import figure
import streamlit as st

def main():
    ''' common explorer '''
st.beta_set_page_config(page_title="Ex-stream-ly Cool App",page_icon="🧊",initial_sidebar_state="expanded",)

st.title('Whatsapp Group Chat Analysis')
st.subheader("Simple Data Explorer")
#st.markdown('Analysis on Whatsapp chats of users.')
st.set_option('deprecation.showfileUploaderEncoding', False)

uploaded_file = st.file_uploader("Upload Your Whatsapp Chat.", type="txt")

st.info("Beta release")

#file selection
#df = pd.read_fwf(uploaded_file, header=None)

#preprocessing
def startsWithDate(s):
    pattern=re.compile(r'([0-2][0-9]|[3][0-9])(\/)([0-2][0-9]|[3][0-9])(\/)(\d{2}|\d{4}), (\d{1}|\d{2})(\:)([0-9][0-9]) am -')
    result = re.match(pattern, s)
    if result:
        return result
    pattern=re.compile(r'([0-2][0-9]|[3][0-9])(\/)([0-2][0-9]|[3][0-9])(\/)(\d{2}|\d{4}), (\d{1}|\d{2})(\:)([0-9][0-9]) pm -')
    result = re.match(pattern, s)
    if result:
        return True
    return False


def startwithauthor(s):
    pattern=re.compile(r'^([\w])+:|([\w]+[\s]+\w+):|([\w]+[\s]+[\w]+[\s]+\w+):|(\+\d{2} \d{5} \d{5}):')
    #first name
    #first name last name
     #first name mid name lastname
      #indian number
   #pattern = '^' + '|'.join(patterns)
 #   print(r'pattern')
   # pattern=re.compile(r'pattern')
    #print(pattern)
    result = re.search(pattern, s)
    #matches=pattern.finditer(s)
    #print(s)
    #print(result)
    if result:
        return True
    return False


def authorfinder(sentence):
    pattern=re.compile(r'([\w])+:|([\w]+[\s]+\w+):|([\w]+[\s]+[\w]+[\s]+\w+):|(\+\d{2} \d{5} \d{5}):')
    #^([\w])+:|([\w]+[\s]+\w+):|([\w]+[\s]+[\w]+[\s]+\w+):|(\+\d{2} \d{5} \d{5}):
    #first name
    #first name last name
    #first name mid name lastname
    #indian number
    #pattern = '^' + '|'.join(patterns)
    #   print(r'pattern')
    # pattern=re.compile(r'pattern')
    result = re.search(pattern, sentence)
    #matches=pattern.finditer(s)
    #print(sentence)
    #print(result)
    if result:
        return True
    return False
    


def getdata(line):
    splitline=line.split('-')
    #print(splitline)
    datetime=splitline[0]
    #print(datetime)
    date,time=datetime.split(',')
    #print(date)
    #print(time)
    #message=" ".join(splitline[1:])
    message=splitline[1]
    #print(message)
    if authorfinder(message):
        splitmessage=message.split(':')
        author=splitmessage[0]
        message=splitmessage[1]
    else:
        author=None
    #print(author)
    return date,time,author,message

if uploaded_file is not None:
    # Process you file here
    #value = uploaded_file.getvalue()
    value=uploaded_file

    parseddata = [] 
    #conversationpath = 'wa.txt' 
    #with open(conversationpath, encoding="utf-8") as fp:
    fp=uploaded_file
    fp.readline()
    messagebuffer=[]
    date,time,author=None,None,None

    while True:
        line = fp.readline() 
        if not line: # Stop reading further if end of file has been reached
            break
        line=line.strip()
        #print(type(line))
        if startsWithDate(line):
            if len(messagebuffer)>0:
                parseddata.append([date,time,author,"".join(messagebuffer)])
            messagebuffer.clear()
            date,time,author,message=getdata(line)
            messagebuffer.append(message)
        else:
            messagebuffer.append(line)

    df = pd.DataFrame(parseddata,columns=['date', 'time', 'author', 'message'])
    # print(df.head())
    #print(df.shape)
    #removing null author
    null_authors_df = df[df['author'].isnull()]
    ##resubstituding to df
    df = df.drop(null_authors_df.index)
   # print(df.shape)
    #print(df.head())
    st.balloons()





    ## top 10

    # top 10 active days
    #top messages sent on this date
    df['date'].value_counts().head(10)

    st.subheader("Top 10 active days")
    plt.xticks(rotation=30)
    plt.title("Top 10 active days")
    plt.xlabel("Dates")
    plt.ylabel("Number of messages")
    #plt.
    plt.plot(df['date'].value_counts().head(10),linewidth=3,color='green',marker='o',linestyle='-')
    st.pyplot()


    #top 10 authors
    df['author'].value_counts().head(10)
    st.subheader("Top 10 Authors")
    #figure(num=None, figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')
    #plt.figure(figsize=(len(combination)*0.25,10))
    plt.xticks(rotation=30)
    plt.title("Top 10 Active Authors")
    plt.xlabel("Amount of Messages")
    plt.ylabel("Authors")
    axes= plt.axes()
    axes.grid()

    chart=(df['author'].value_counts().head(10))
    chart.plot.barh()
    st.pyplot()



    # Top 10 Messages
    st.subheader("Top 10 Messages")
    media_messages_df = df[df['message'] == ' <Media omitted>']
    #http_df = df[df['message'] == ' https']
    nonmedia_messages_df = df.drop(media_messages_df.index)
    #nonmedia_messages_df = df.drop(http_df.index)
    #nonmedia_messages_df
    plt.title("Top 10 Messages")
    plt.xlabel("Times")
    plt.ylabel("Number of messages")

    axes= plt.axes()
    axes.grid()
    plt.xticks(rotation=30)
    #print(nonmedia_messages_df['message'].value_counts().head(10))
    chart=(nonmedia_messages_df['message'].value_counts().head(10))
    chart.plot.barh()
    st.pyplot()



    ##talktive convert

    nonmedia_messages_df['letter_count'] = nonmedia_messages_df['message'].apply(lambda s : len(s) -1)
    nonmedia_messages_df['word_count'] = nonmedia_messages_df['message'].apply(lambda s : len(s.split(" ")) -1)

    #"Top 10 Talkative Authors"
    st.subheader("Top 10 Talkative Authors who writes long messages")
    total_word_count_grouped_by_author = nonmedia_messages_df[['author', 'word_count']].groupby('author').sum()
    sorted_total_word_count_grouped_by_author = total_word_count_grouped_by_author.sort_values('word_count', ascending=False)
    top_10_sorted_total_word_count_grouped_by_author = sorted_total_word_count_grouped_by_author.head(10)
    top_10_sorted_total_word_count_grouped_by_author.plot.barh()

    plt.title("Top 10 Talkative Authors")
    plt.xlabel('Number of Words')
    plt.ylabel('Authors')

    st.pyplot()


    #"Top Frequency of letter counts in words "
    st.subheader("Top Frequency of letter counts in words")
    #plt.figure(figsize=(15, 20))
    #plt.yticks(rotation=90)
    letter_count_value_counts = nonmedia_messages_df['letter_count'].value_counts()
    top_40_letter_count_value_counts = letter_count_value_counts.head(20)
    top_40_letter_count_value_counts.plot.bar()
    plt.title('Frequency & Letter count')
    plt.xlabel('Letter count')
    plt.ylabel('Frequency')

    st.pyplot()



    ##total



    #total numbers
    #total messages
    #print("total Messages")
    #df.shape[0]



    ## converting media message into variable
    media_messages_df=df[df['message']==' <Media omitted>']
    #print(media_messages_df)
    ## total media messages
    #print("Total Media")
    #print(media_messages_df['message'].count())


    ## TOTAL WORDS AND LETTERS
    nonmedia_messages_df['letter_count'] = nonmedia_messages_df['message'].apply(lambda s : len(s) -1)
    nonmedia_messages_df['word_count'] = nonmedia_messages_df['message'].apply(lambda s : len(s.split(" ")) -1)

    #total words
    #print("Total Word Count")
    #print(nonmedia_messages_df['word_count'].sum())

    #total letters
    #print("Total letter Count")
    #print(nonmedia_messages_df['letter_count'].sum())

    #total authors
    totalauthors=df['author'].value_counts().count()

    row=["Total Authors","Total Media Messages","Total Message","Total Word Count","Total Letter Count",]

    col=[totalauthors,media_messages_df['message'].count(),df.shape[0],nonmedia_messages_df['word_count'].sum(),nonmedia_messages_df['letter_count'].sum()]

    data=pd.DataFrame(col,row)
    #plt.figure(figsize=(10,10))

    data=data.rename({0:"Numbers"},axis=1)
    st.subheader("Summary")
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    
    data.plot(table=True,ax=ax,color='green',marker='o',linewidth=2)
    st.pyplot()


    st.dataframe(data)
else:
    st.header("Upload file to continue")

''' functions to add
    per day analysis 
    create function for displaying weeks day msg distribution
    normal 1 person option
    graph of whole msg in year

'''
if __name__=='__main__':
    main()
