import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import sys


matplotlib.style.use('ggplot')

def convert_time(t):
    #t = "1:12:23"
    #print t
    #t,d = t.split(",")
    #print t
    (h, m, s) = t.split(':')
    result = int(h) * 3600 + int(m) * 60 + int(s)
    return  result

def convert_time_mili(t):
    t,d = t.split(".")
    (h, m, s) = t.split(':')
    result = int(h) * 3600 + int(m) * 60 + int(s)
    return  result







#plotviews= data.Views.plot(kind='bar', figsize=(17, 6), width = .9, color = '#278DBC', edgecolor= 'none', grid = False, clip_on=False)


# python barplot.py <input1.csv> <input2.csv> <node_name> <output_name>

def main(input_cdata,input_iodata,node_name,output_name):

    pp = PdfPages(output_name)
    data = pd.read_csv(input_iodata)
    ctempdata = pd.read_csv(input_cdata,',')
    cdata = ctempdata[ctempdata.node_name==node_name]
    M =  cdata['duration']
    N = [convert_time_mili(x) for x in cdata['start_time'] ]
    O = [x for x in cdata['duration']]

    A = data['util']
    B = data['io_wait']
    C = data['await']
    D= data['cpu_user']
    X= data['time_stamp'] #convert this to same unit

    Z= [convert_time(x) for x in data['time_stamp'] ]

    #plt.plot(Z,A)
    #plt.plot(Z,B)
    #plt.plot(Z,C)
    #plt.plot(Z,D)

    #sns.set_style("white")
    #sns.set_style("ticks")

    #csfont = {'fontname':'Comic Sans MS'}
    #hfont = {'fontname':'Helvetica'}
    #sns.set()
    #sns.axes_style("darkgrid"

    sns.set_style("darkgrid", {"axes.facecolor": ".9"})
    #sns.despine(left=True)
    sns.set_context("paper", font_scale=.85, rc={"lines.linewidth": 1.5})

    '''
    ##Two subplots, the axes array is 1-d,
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].plot(x, y)
    axarr[0].set_title('Sharing X axis')
    axarr[1].scatter(x, y)
    '''
    l= len(X)
    a = X[0]
    b = X[l-1]


    f1, ax1 = plt.subplots(1)
    #base = N[0]
    #base = convert_time_mili(ctempdata['start_time'][0])
    base = 0
    T = [ x - base for x in N]
    I = [x for x in range(0,len(N))]

    for i in range(len(T)):
        O[i] =  T[i] + O[i]
        ax1.hlines(i,T[i],O[i],lw='1')
    #ax1.set_xticks(T)
    #for i in range(len(N)):
        #ax1.hlines(i,N[i],O[i])
    #ax1.hlines(i,T,O)

    #print (i,N[i]-base,O[i])
    print (T)
    print(Z)
    print(A)
    f2, axarr = plt.subplots(4, sharex=True)
    #plt.axis([a,b,0,100])
    #axarr[0].plot(Z, A,color="steelblue")
    # axarr[0].plot_date(Z, A,linestyle='solid',lw='1',color="steelblue",aa='True')
    # #axarr[0].patch.set_facecolor('gray')
    #
    # axarr[0].set_title('util')
    # #plt.axis([a,b,0,1000])
    # #axarr[1].plot(Z, B)
    # axarr[1].plot_date(Z, B,linestyle='solid',lw='1',color="slategray",aa='True')
    #
    # axarr[1].set_title('io_wait')
    # #plt.axis([a,b,0,1000])
    # #axarr[2].plot(Z, C)
    # axarr[2].plot_date(Z, C, linestyle='solid',lw='1',color="lightblue",aa='True')
    #
    # axarr[2].set_title('await')
    # #plt.axis([a,b,0,100])
    # axarr[3].plot_date(Z, D, linestyle='solid',lw='1',color="tomato",aa='True')
    # axarr[3].set_title('cpu')
    #
    #
    # plt.gcf().autofmt_xdate()


    # for i in range(0,len(Z)):
    #     #O[i] =  T[i] + O[i]
    #     axarr[0].vlines(Z[i],0,A[i],linestyle='solid',lw='1',color="steelblue")
    axarr[0].plot(Z,A,linestyle='solid',lw='2',color="steelblue",aa='True',dash_capstyle="round")
    axarr[0].set_xticks(Z)
    #axarr[0].plot_(Z, A,linestyle='solid',lw='1',color="steelblue",aa='True')
    #axarr[0].patch.set_facecolor('gray')

    # axarr[0].set_title('util')
    # #plt.axis([a,b,0,1000])
    # #axarr[1].plot(Z, B)
    # axarr[1].plot_date(Z, B,linestyle='solid',lw='1',color="slategray",aa='True')
    #
    # axarr[1].set_title('io_wait')
    # #plt.axis([a,b,0,1000])
    # #axarr[2].plot(Z, C)
    # axarr[2].plot_date(Z, C, linestyle='solid',lw='1',color="lightblue",aa='True')
    #
    # axarr[2].set_title('await')
    # #plt.axis([a,b,0,100])
    # axarr[3].plot_date(Z, D, linestyle='solid',lw='1',color="tomato",aa='True')
    # axarr[3].set_title('cpu')


    plt.gcf().autofmt_xdate()


    #plt.bar(Z,Y)
    #plt.show()

    color_list = ['b', 'g', 'r']
    gap = .8 / len(data)
    #for i, row in enumerate(data):
    #    X = np.arange(len(row))
    #    plt.bar(X + i * gap, row, width = gap, color = color_list[i % len(color_list)])
    #plt.show()
    #plt.savefig(pp, format='pdf')

    #pp = PdfPages('foo.pdf')
    pp.savefig(f1)
    pp.savefig(f2)
    #pp.savefig(plot3)
    pp.close()


if __name__ == "__main__":
    if len(sys.argv)<4:
        print "python barplot.py <input1.csv> <input2.csv> <node_name> <output_name>"
        sys.exit()
    input_cdata = sys.argv[1]
    input_iodata= sys.argv[2]
    node_name = sys.argv[3]
    output_name = sys.argv[4]
    main(input_cdata,input_iodata,node_name,output_name)
