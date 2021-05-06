# -*- coding: utf-8 -*-


from bokeh.io import output_file
from bokeh.plotting import figure, show, curdoc
from bokeh.models import CustomJS, Dropdown, ColumnDataSource, Range1d, Select, FactorRange, Legend, LegendItem, Title
from bokeh.transform import factor_cmap
from bokeh.palettes import Blues5
from bokeh.layouts import row, column
from bokeh.models.widgets import Div
import pandas as pd


#-------------------------------------------------
#Reading the csv files
#-------------------------------------------------

datafile= pd.read_csv('Data Sheet Example.csv')    
comments= pd.read_csv('Data_Sheet_Example_Comments.csv') 
source = ColumnDataSource(data=datafile)

## Lists of Parameters 
semester_year= datafile['Semester/Year']
prof= list(datafile['Professor'])
pics= datafile['Picture']
course_prefix= list(datafile['Course Prefix'])
A= datafile['A']
B= datafile['B']
C= datafile['C']
other= datafile['Other']


#---------------------
#Outputting to web
#---------------------
output_file('testing_bokeh.html')

##-----------------------------------------------------------------------
#Professor Picture
#------------------------------------------------------------------------
prof_plot= figure(x_range=(0,400), y_range=(0,400), plot_width = 400, plot_height = 400, title="Professor", toolbar_location=None)


#------------------------------------------------------------------------
#Comment Section
#------------------------------------------------------------------------
# comment= figure(plot_width= 100, plot_height= 200, title= "Comments")
style={'overflow-y':'scroll','height':'200px', 'text-align':'justify'} 
comments_text = Div(text="", width= 120, style = style) 
prof_plot.add_layout(Title(text="Comment Section:", align="left", text_color = "black", text_font_size ="20px"), "below")

# Plot styling
prof_plot.title.text_font_size= '15pt'
prof_plot.axis.visible= False
prof_plot.xgrid.visible= False
prof_plot.ygrid.visible= False


##--------------------------------------------------------------------
#Grade Distribution Bar Graph
#---------------------------------------------------------------------
letters = ['A', 'B', 'C', 'Other']
grades = [0]*4
prof_grades = ColumnDataSource(data=dict(letters=letters, grades=grades)) # << Important!

cmap = {
    "A"         : "#225ea8",
    "B"         : "#41b6c4",
    "C"         : "#a1dab4",
    "Other"     : "#ffffcc",
}

   
TOOLTIP = [
    ("Letter Grade", "@letters"),
    ("Number of Students", "@grades"),
]

pp = figure(x_range = FactorRange(*letters),plot_height = 350, plot_width = 700,
            title = 'Grade Distribution:', tooltips = TOOLTIP, toolbar_location = None, tools="hover")

pp.vbar(x='letters', top='grades',source = prof_grades, width=.3,
        color=factor_cmap('letters', palette=list(cmap.values()), factors=list(cmap.keys())))

# Plot Styling 
pp.y_range.start = 0
pp.x_range.range_padding = 0.1
pp.xaxis.major_label_text_font_size = '15pt'
pp.xaxis.major_label_text_font_style = 'bold'
pp.xgrid.grid_line_color = None
pp.title.text_font_size = '15pt'



#------------------------------------------------------------------------
#For Classes Plot
#------------------------------------------------------------------------

source1 = ColumnDataSource(data=dict(Professor = [], A =[], B = [], 
                        C = [], Other = []))

courses = list(set(datafile['Course Prefix']))


prof_all = figure(x_range=prof, plot_height=350,plot_width = 700, title="Individual Courses",
           toolbar_location=None, tools="hover", tooltips= "$name : @$name")

colors= ['#393b79', '#5254a3', '#6b6ecf', '#9c9ede']  

prof_all.vbar_stack(letters, x='Professor', width=0.9, source=source1,
                    color=colors, legend_label=letters)

# Plot styling
prof_all.y_range.start = 0
prof_all.x_range.range_padding = 0.1
prof_all.xaxis.major_label_orientation = 1/4
prof_all.xgrid.grid_line_color = None
prof_all.axis.minor_tick_line_color = None
prof_all.outline_line_color = None
prof_all.legend.location = "top_left"
prof_all.legend.orientation = "horizontal"
prof_all.title.text_font_size = '15pt'


#--------------------------------------------------------------------------
# Callback Function:
#--------------------------------------------------------------------------
def Callback(attrname, old, new):
    New_Prof = select.value
    index = prof.index(New_Prof)
    
    ### Changing Image ###
    prof_plot.image_url(url= [str(source.data['Picture'][index])], x=0, y=0, w=400, h=400, anchor="bottom_left")
    
    ### Changing Grade Distribution ###
    grades = [A[index], B[index], C[index], other[index]]
    prof_grades.data = dict(letters=letters, grades = grades)
    pp.title.text = 'Grade Distribution: ' + str(course_prefix[index])

    ### Changing Comment Section ###
    text = ''
    for comment in comments[New_Prof]:
        text += '<br>  <br/>' + str(comment)
    comments_text.text = text


def Callback2(attrname, old, new):
    course = select2.value
    prof_class   = []
    grades_A     = []
    grades_B     = []
    grades_C     = []
    grades_other = []

    index = get_index_positions(course_prefix, course)
    
    # Updating Class selected:
    for i in index:
        prof_class.append(prof[i])
        grades_A.append(A[i])
        grades_B.append(B[i])
        grades_C.append(C[i])
        grades_other.append(other[i])      
    
    source1.data=dict(Professor = prof_class, A = grades_A, B = grades_B, 
                        C = grades_C, Other = grades_other)

    #Creating Temp Bar Graph 
    prof_temp = figure(x_range=prof_class, plot_height=350, plot_width = 700, title="Individual Courses",
            toolbar_location=None, tools="hover", tooltips= "$name : @$name")
   
    prof_temp.vbar_stack(letters, x='Professor', width=0.9, source=source1,
                    color=colors, legend_label=letters)
    
    prof_temp.y_range.start = 0
    prof_temp.x_range.range_padding = 0.1
    prof_temp.xaxis.major_label_orientation = 1/4
    prof_temp.xgrid.grid_line_color = None
    prof_temp.axis.minor_tick_line_color = None
    prof_temp.outline_line_color = None
    prof_temp.legend.location = "top_left"
    prof_temp.legend.orientation = "horizontal"
    prof_temp.title.text_font_size = '15pt'
    
    #Updating Bar Graph in Layout
    layout.children[1].children[2] = prof_temp
    
def get_index_positions(list_of_elems, element):
    ''' Returns the indexes of all occurrences of give element in
    the list- listOfElements '''
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            index_pos = list_of_elems.index(element, index_pos)
            # Add the index position in list
            index_pos_list.append(index_pos)
            index_pos += 1
        except ValueError as e:
            break
    return index_pos_list


# Creating Widgets
select= Select(title= 'Choose Professor', value= '', options= prof )
select2= Select(title= 'Choose Class', value= 'all', options= courses )

# Callback Methods
select.on_change('value', Callback)
select2.on_change('value', Callback2)


#----------------------------
# Combining Dashboard Plots:
#----------------------------
layout1= column(select, prof_plot, comments_text)
layout2 = column(pp,select2, prof_all)
layout= row(layout1, layout2)
curdoc().add_root(layout)

# show(layout1)
# show(layout2)
# show(layout)


















