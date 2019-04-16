from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from matplotlib.pyplot import *
from Tkinter import *
import tkMessageBox
import numpy as np
import ttk

def create_plot(*args):
    #-------------------------------PURELY FOR ASTHETIC REASONS, AND TO KEEP THE BUTTONS SELECTED----------------------------------------
    numchange = False
    xchange = False
    ychange = False
    titlechange = False
    if (num_of_plots_.get() == -1) :
        num_of_plots_.set(other_num.get())
        numchange = True
    if (x_axis_.get() == 'other') :
        x_axis_.set(other_x.get())
        xchange = True
    if (y_axis_.get() == 'other') :
        y_axis_.set(other_y.get())
        ychange = True
    if (title_.get() == 'other') :
        title_.set(other_title.get())
        titlechange = True
    #----------------------------------------------------------------------------------------------------------------------------------

    #define the arrays for multiple inputs
    data = []
    names = []

    #run try catch so program doesn't crash if worng types of imputs are selected, this is lazy coding
    try :
        if (subtract.get()) : #----------------------------------------------------SUBRACT--------------------------------------------------------------------
            
            #Make sure there are at least two plots selected
            if (num_of_plots_.get() == 1) :
                tkMessageBox.showinfo('ERROR','Number 0f plots must be at least 2, to subtract!')
                return

            #Load the data
            for i in range(0,num_of_plots_.get()) :
                #set title for TK_askopenfilename
                if (i == 0) :
                    x = 'Data Being Subtracted from'
                else :
                    x = 'Data Being Subtracted'
                load_data(x,names,data)

            #Chop the data if necessary
            if (chopped.get()) :
                data[0] = chop(data[0],chopped_num.get(),find_length(data[0][:,x_.get()]))

            #Set inital data to be subtracted from
            x_values = data[0][:,x_.get()]
            y_values = data[0][:,y_.get()]

            #Subract the data
            for i in range(1,num_of_plots_.get()) :
                #Chop the data if necessary
                if (chopped.get()) :
                    data[i] = chop(data[i],chopped_num.get(),find_length(data[i][:,x_.get()]))
                
                #Actually subract the data
                y_values = y_values - data[i][:,y_.get()]

            #Average if necessary
            if (average_.get()) :
                plot(average(x_values,find_length(x_values)),average(y_values,find_length(x_values)),'.')
            #Otherwise simply plot the dtata
            else :
                plot(x_values,y_values,'.')

            #Set title and save file
            name = names[0]
            for i in range(1,num_of_plots_.get()) :
                name = name + '_minus_{0}'.format(names[i])
            if (average_.get()) :
                name = name + '_AVERAGED'
            save_and_set_axis(name)


        else : #---------------------------------------------------------------MULTI-PLOT----------------------------------------------------------------------------------------------------------
            #Load the data
            for i in range(0,num_of_plots_.get()) :
                load_data('Data Being Plotted',names,data)

            #For each data set do the following
            for i in range(0,num_of_plots_.get()) :
                #Chop if necessary
                if (chopped.get()) :
                    data[i] = chop(data[i],chopped_num.get(),find_length(data[i][:,x_.get()]))

                #Average and Plot if necessary
                if (average_.get()) :
                    plot(average(data[i][:,x_.get()],find_length(data[i][:,x_.get()])),average(data[i][:,y_.get()],find_length(data[i][:,x_.get()])),'.',label=names[i])
                
                #Otherwise just plot the data
                else :
                    plot(data[i][:,x_.get()],data[i][:,y_.get()],'.',label=names[i])
                    #errorbar(data[i][:x_.get()],data[i][:y_.get()], yerr=data[i][:3])

            #Create titles and save the plot
            name = names[0]
            for i in range(1,num_of_plots_.get()) :
                name = name + '_&_{0}'.format(names[i])
            if (average_.get()) :
                name = name + "_AVERAGED"
            save_and_set_axis(name)

    except :
        tkMessageBox.showinfo('ERROR','SOMETHING WENT, CHECK ALL INPUT FIELDS!')

    #-----------------------------------------------------RESELECT THE BUTTONS, NOT IMPORTANT FOR FUNCTIONALITY -------------------------
    if (numchange) :
        num_of_plots_.set(-1)
    if (xchange) :
        x_axis_.set('other')
    if (ychange) :
        y_axis_.set('other')
    if (titlechange) :
        title_.set('other')
    #-------------------------------------------------------------------------------------------------------------------------------------

def flip(*args) :
    if (flipped.get()) :
        x_.set(1)
        y_.set(0)
    else :
        x_.set(0)
        y_.set(1)

def load_data(title_,_names_,_data_) :
    filename = askopenfilename(initialdir='D:/Vojin/',title=title_)
    _names_.append((filename.split("/")[len(filename.split("/")) - 1]).split('.')[0])
    _data_.append(np.genfromtxt(filename,delimiter=delimiter_.get(),skip_header=header_.get(),skip_footer=footer_.get()))

def save_and_set_axis(_name_) :
    title(title_.get())
    xlabel(x_axis_.get())
    ylabel(y_axis_.get())
    loc = _loc.get()
    savefig('{0}/{1}_plot.pdf'.format(loc,_name_),format='pdf',dpi=10000) #png'.format(loc,_name_))#
    show()


def save_loc(*args) :
   _loc.set(askdirectory())

def find_length(arr) :
    for i in range(1,len(arr)) :
        if (arr[0] == arr[i]) :
            return i
    return 0

def average(arr,n) :
    out__ = []
    c = len(arr)/n
    for i in range(0, n) :
        a = 0
        for j in range (0,c) :
            a += arr[i + j*n]
        out__.append(a/c) 
    return out__
    
def chop(arr,n,l) :
    out___ = arr[0:n*l]
    return out___


root = Tk()
root.title('Create and Save Plots')
ttk.Style().theme_use('classic')

mainframe = ttk.Frame(root,padding='3 3 12 12')
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
mainframe.columnconfigure(0,weight=1)
mainframe.rowconfigure(0,weight=1)

#Define the gloabal variables
other_title = StringVar()
other_x = StringVar()
other_y = StringVar()
other_num = IntVar()
title_ = StringVar()
x_axis_ = StringVar()
y_axis_ = StringVar()
num_of_plots_ = IntVar()
delimiter_ = StringVar()
header_ = IntVar()
footer_ = IntVar()
x_ = IntVar()
y_ = IntVar()
flipped = BooleanVar()
subtract = BooleanVar()
average_ = BooleanVar()
_loc = StringVar()
chopped = BooleanVar()
chopped_num = IntVar()

title_lf = ttk.LabelFrame(mainframe,text='Title')
title_lf.grid(column=0,row=0,sticky=W)

ttk.Radiobutton(title_lf,text='Background CV',variable=title_,value='Background CV').grid(row=0,column=0,sticky=W)
ttk.Radiobutton(title_lf,text='CV Diagram of Ferrocene',variable=title_,value='CV Diagram of Ferrocene').grid(row=1,column=0,sticky=W)
ttk.Radiobutton(title_lf,text='UV-Vis of Gold Np with FDT',variable=title_,value='UV-Vis of Gold Np with FDT').grid(row=2,column=0,sticky=W)
ttk.Radiobutton(title_lf,text='Other:',variable=title_,value='other').grid(row=3,column=0,sticky=W)
ttk.Entry(title_lf,width=10,textvariable=other_title).grid(row=4,column=0)
title_.set('CV Diagram of Ferrocene')

axes_lf = ttk.LabelFrame(mainframe,text='Axes')
axes_lf.grid(column=0,row=1,sticky=W)

x_axis_lf = ttk.LabelFrame(axes_lf,text='X-Axis')
x_axis_lf.grid(column=0,row=0,sticky=W)

ttk.Radiobutton(x_axis_lf,text='Voltage',variable=x_axis_,value='Potential ($mV$) vs. Ag/AgCl').grid(row=0,column=0,sticky=W)
ttk.Radiobutton(x_axis_lf,text='Wave Length',variable=x_axis_,value='Wave Length ($nm$)').grid(row=1,column=0,sticky=W)
ttk.Radiobutton(x_axis_lf,text='Other:',variable=x_axis_,value='other').grid(row=2,column=0,sticky=W)
ttk.Entry(x_axis_lf,width=10,textvariable=other_x).grid(row=3,column=0)
x_axis_.set('Potential ($mV$) vs. Ag/AgCl')

y_axis_lf = ttk.LabelFrame(axes_lf,text='Y-Axis')
y_axis_lf.grid(column=1,row=0,sticky=W)

ttk.Radiobutton(y_axis_lf,text='Current',variable=y_axis_,value='Current ($\mu A$)').grid(row=0,column=0,sticky=W)
ttk.Radiobutton(y_axis_lf,text='Absorbance',variable=y_axis_,value='Absorbance (Ratio)').grid(row=1,column=0,sticky=W)
ttk.Radiobutton(y_axis_lf,text='Other:',variable=y_axis_,value='other').grid(row=2,column=0,sticky=W)
ttk.Entry(y_axis_lf,width=10,textvariable=other_y).grid(row=4,column=0)
y_axis_.set('Current ($\mu A$)')

ttk.Checkbutton(axes_lf,text='XY Axes Inverted',command=flip,variable=flipped,onvalue=True,offvalue=False).grid(column=0,row=1,sticky=W,rowspan=2)
flipped.set(True)
x_.set(1)
y_.set(0)

right_frame = ttk.Frame(mainframe) 
right_frame.grid(column=1,row=0,rowspan=2,sticky=W)

multi_plot_lf = ttk.LabelFrame(right_frame,text='Multi-Plot')
multi_plot_lf.grid(column=0,row=0,sticky=W)

num_of_plots_lf = ttk.LabelFrame(multi_plot_lf,text='Number Of DataSets')
num_of_plots_lf.grid(column=0,row=0,sticky=W)

ttk.Radiobutton(num_of_plots_lf,text='1',variable=num_of_plots_,value=1).grid(row=0,column=0,sticky=W)
ttk.Radiobutton(num_of_plots_lf,text='2',variable=num_of_plots_,value=2).grid(row=1,column=0,sticky=W)
ttk.Radiobutton(num_of_plots_lf,text='3',variable=num_of_plots_,value=3).grid(row=2,column=0,sticky=W)
ttk.Radiobutton(num_of_plots_lf,text='4',variable=num_of_plots_,value=4).grid(row=3,column=0,sticky=W)
ttk.Radiobutton(num_of_plots_lf,text='More:',variable=num_of_plots_,value=-1).grid(row=4,column=0,sticky=W)
ttk.Entry(num_of_plots_lf,width=10,textvariable=other_num).grid(row=5,column=0)
num_of_plots_.set(1)
other_num.set(5)

ttk.Radiobutton(multi_plot_lf,text='Multiple DataSet Plot',variable=subtract,value=False).grid(column=0,row=1,sticky=W)
ttk.Radiobutton(multi_plot_lf,text='Subtract From One',variable=subtract,value=True).grid(column=0,row=2,sticky=W)

data_lf = ttk.LabelFrame(right_frame,text='Data Settings')
data_lf.grid(column=0,row=1)

ttk.Label(data_lf,text='Delimiter').grid(column=0,row=0,sticky=W)
ttk.Label(data_lf,text='Header').grid(column=0,row=1,sticky=W)
ttk.Label(data_lf,text='Footer').grid(column=0,row=2,sticky=W)

ttk.Entry(data_lf,width=3,textvariable=delimiter_).grid(column=1,row=0,sticky=W)
ttk.Entry(data_lf,width=3,textvariable=header_).grid(column=1,row=1,sticky=W)
ttk.Entry(data_lf,width=3,textvariable=footer_).grid(column=1,row=2,sticky=W)


ttk.Checkbutton(data_lf,text='Only the first',variable=chopped,onvalue=True,offvalue=False).grid(row=3,column=0,sticky=W)
ttk.Entry(data_lf,width=3,textvariable=chopped_num).grid(row=3,column=1,sticky=W)

ttk.Checkbutton(data_lf,text='Average Values',variable=average_,onvalue=True,offvalue=False).grid(column=0,row=4,sticky=W,columnspan=2)

delimiter_.set(',')
header_.set(2)
footer_.set(1)
chopped_num.set(5)

ttk.Button(mainframe,text='Choose Save Location',command=save_loc).grid(row=2,column=1)
_loc.set('C:/plots')

ttk.Button(mainframe,text='Create Plot',command=create_plot).grid(row=2,column=0)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()