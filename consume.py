
from inotify_simple import INotify, flags
import pickle
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show, output_file, save
from bokeh.layouts import gridplot, widgetbox
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.models.ranges import Range1d
from bokeh.models import LinearAxis, LogAxis, DataRange1d
import threading
from bokeh.models.widgets import Panel, Tabs

class Consumer(object):


    def extract(self,mofile,owfile,xufile): #consume fresh data streamed from the Producer applications

        moFile = mofile #MetOffice
        owFile = owfile #OpenWeather
        xuFile = xufile #APIXU

        with open(moFile, 'rb') as e:

            pick_mo = (pickle.load(e))
            frame_mancity = pick_mo[0] #first club in List
            frame_manunited = pick_mo[1]
            frame_liverpoolfc = pick_mo[2]
            frame_everton = pick_mo[3]
            frame_rangers = pick_mo[4]
            frame_partik = pick_mo[5]
            frame_celtic = pick_mo[6]
            frame_chelsea = pick_mo[7]
            frame_arsenal = pick_mo[8]
            frame_tottenham = pick_mo[9]
            frame_westham = pick_mo[10]
            frame_crystalpalace = pick_mo[11]

        with open(owFile,'rb') as f:
            pick_ow = (pickle.load(f))
            frame_acmilan = pick_ow[0] #first club in List
            frame_intermilan = pick_ow[1]
            frame_juventus = pick_ow[2]
            frame_torino = pick_ow[3]

            #print(type(frame), frame)

        with open(xuFile,'rb') as g:
            pick_xu = (pickle.load(g))
            frame_manchester = pick_xu[0] #first city in List
            frame_liverpool = pick_xu[1]
            frame_glasgow = pick_xu[2]
            frame_london = pick_xu[3]
            frame_milan = pick_xu[4]
            frame_turin = pick_xu[5]

        #prepare dictionaries for pandas dataframe
        return frame_mancity,frame_manunited,frame_liverpoolfc,frame_everton,\
               frame_rangers,frame_partik,frame_celtic,\
               frame_chelsea,frame_arsenal,frame_tottenham,frame_westham,frame_crystalpalace,\
               frame_acmilan,frame_intermilan,frame_juventus,frame_torino,\
               frame_manchester,frame_liverpool,frame_glasgow,frame_london,frame_milan,frame_turin


    #plots using high level Bokeh graphing utilities
    def plot(self,moFile,owFile,xuFile):
        mofile = moFile
        owfile = owFile
        xufile = xuFile
        frame_mancity, frame_manunited, frame_liverpoolfc, frame_everton, \
        frame_rangers, frame_partik, frame_celtic, \
        frame_chelsea, frame_arsenal, frame_tottenham, frame_westham, frame_crystalpalace, \
        frame_acmilan, frame_intermilan, frame_juventus, frame_torino, \
        frame_manchester, frame_liverpool, frame_glasgow, frame_london, frame_milan, frame_turin \
            = self.extract(mofile,owfile,xufile)

        #title of charts
        title1 = 'Manchester'+'(Temp/Precip)'
        title2 = 'Liverpool'+'(Temp/Precip)'
        title3 = 'Glasgow'+'(Temp/Precip)'
        title4 = 'London'+'(Temp/Precip)'
        title5 = 'Milan'+'(Temp/Precip)'
        title6 = 'Turin'+'(Temp/Precip)'

        title7 = 'Temp at ' + 'ManCity'
        title8 = 'Wind at ' + 'ManCity'
        title9 = 'Prob of Precip at ' + 'ManCity'

        title10 = 'Temp at ' + 'ManUnited'
        title11 = 'Wind at ' + 'ManUnited'
        title12 = 'Prob of Precip at ' + 'ManUnited'

        title13 = 'Temp at ' + 'LiverpoolFC'
        title14 = 'Wind at ' + 'LiverpoolFC'
        title15 = 'Prob of Precip at ' + 'LiverpoolFC'

        title16 = 'Temp at ' + 'Everton'
        title17 = 'Wind at ' + 'Everton'
        title18 = 'Prob of Precip at ' + 'Everton'

        title19 = 'Temp at ' + 'ACMilan'
        title20 = 'Wind at ' + 'ACMilan'
        title21 = 'Prob of Precip at ' + 'ACMilan'

        title22 = 'Temp at ' + 'Juventus'
        title23 = 'Wind at ' + 'Juventus'
        title24 = 'Prob of Precip at ' + 'Juventus'



        #Bokeh color palatte
        colors = "'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', " \
        "'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', " \
        "'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', " \
        "'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', " \
        "'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', " \
        "'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', " \
        "'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', " \
        "'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', " \
        "'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', " \
        "'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', " \
        "'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', " \
        "'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', " \
        "'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', " \
        "'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', " \
        "'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', " \
        "'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', " \
        "'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', " \
        "'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', " \
        "'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', " \
        "'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen'"

        #prepare dataframe MANCHESTER
        df1 = pd.DataFrame.from_dict(frame_manchester, orient="index")
        df1.index.name = 'Date'
        df1.index = pd.to_datetime(df1.index)
        df1.sort_index(inplace=True)
        print(df1)

        source = ColumnDataSource(df1)

        p1 = figure(x_axis_type="datetime", title=title1)
        p1.line('Date', 'temp', line_color="black", source=source)
        p1.xaxis.axis_label = 'Date'
        p1.yaxis.axis_label = 'Celcius'
        p1.grid.grid_line_alpha=0
        p1.ygrid.band_fill_color="olive"
        p1.ygrid.band_fill_alpha = 0.1
        p1.background_fill_color = "beige"
        p1.background_fill_alpha = 0.5
        p1.extra_y_ranges = {'rain':Range1d(start=0, end = 1.0)}
        p1.add_layout(LinearAxis(y_range_name="rain",axis_label="in"), 'right')
        p1.circle('Date', 'rain', size=8, color='blue', alpha=0.2, legend='precip(in)', y_range_name='rain', source=source)
        p1.legend.label_text_font_size = "8pt"
        #p1.legend.border_line_alpha = 0.01

        # prepare dataframe LIVERPOOL
        df2 = pd.DataFrame.from_dict(frame_liverpool, orient="index")
        df2.index.name = 'Date'
        df2.index = pd.to_datetime(df2.index)
        df2.sort_index(inplace=True)
        print(df2)

        source = ColumnDataSource(df2)

        p2 = figure(x_axis_type="datetime", title=title2)
        p2.line('Date', 'temp', line_color="black", source=source)
        p2.xaxis.axis_label = 'Date'
        p2.yaxis.axis_label = 'Celcius'
        p2.grid.grid_line_alpha = 0
        p2.ygrid.band_fill_color = "olive"
        p2.ygrid.band_fill_alpha = 0.1
        p2.background_fill_color = "beige"
        p2.background_fill_alpha = 0.5
        p2.extra_y_ranges = {'rain': Range1d(start=0, end=1.0)}
        p2.add_layout(LinearAxis(y_range_name="rain", axis_label="in"), 'right')
        p2.circle('Date', 'rain', size=8, color='blue', alpha=0.2, legend='precip(in)', y_range_name='rain',
                  source=source)
        p2.legend.label_text_font_size = "8pt"
        # p1.legend.border_line_alpha = 0.01

        # prepare dataframe GLASGOW
        df3 = pd.DataFrame.from_dict(frame_glasgow, orient="index")
        df3.index.name = 'Date'
        df3.index = pd.to_datetime(df3.index)
        df3.sort_index(inplace=True)
        print(df3)

        source = ColumnDataSource(df3)

        p3 = figure(x_axis_type="datetime", title=title3)
        p3.line('Date', 'temp', line_color="black", source=source)
        p3.xaxis.axis_label = 'Date'
        p3.yaxis.axis_label = 'Celcius'
        p3.grid.grid_line_alpha = 0
        p3.ygrid.band_fill_color = "olive"
        p3.ygrid.band_fill_alpha = 0.1
        p3.background_fill_color = "beige"
        p3.background_fill_alpha = 0.5
        p3.extra_y_ranges = {'rain': Range1d(start=0, end=1.0)}
        p3.add_layout(LinearAxis(y_range_name="rain", axis_label="in"), 'right')
        p3.circle('Date', 'rain', size=8, color='blue', alpha=0.2, legend='precip(in)', y_range_name='rain',
                  source=source)
        p3.legend.label_text_font_size = "8pt"
        # p1.legend.border_line_alpha = 0.01

        # prepare dataframe LONDON
        df4 = pd.DataFrame.from_dict(frame_london, orient="index")
        df4.index.name = 'Date'
        df4.index = pd.to_datetime(df4.index)
        df4.sort_index(inplace=True)
        print(df4)

        source = ColumnDataSource(df4)

        p4 = figure(x_axis_type="datetime", title=title4)
        p4.line('Date', 'temp', line_color="black", source=source)
        p4.xaxis.axis_label = 'Date'
        p4.yaxis.axis_label = 'Celcius'
        p4.grid.grid_line_alpha = 0
        p4.ygrid.band_fill_color = "olive"
        p4.ygrid.band_fill_alpha = 0.1
        p4.background_fill_color = "beige"
        p4.background_fill_alpha = 0.5
        p4.extra_y_ranges = {'rain': Range1d(start=0, end=1.0)}
        p4.add_layout(LinearAxis(y_range_name="rain", axis_label="in"), 'right')
        p4.circle('Date', 'rain', size=8, color='blue', alpha=0.2, legend='precip(in)', y_range_name='rain',
                  source=source)
        p4.legend.label_text_font_size = "8pt"
        # p1.legend.border_line_alpha = 0.01

        # prepare dataframe MILAN
        df5 = pd.DataFrame.from_dict(frame_milan, orient="index")
        df5.index.name = 'Date'
        df5.index = pd.to_datetime(df5.index)
        df5.sort_index(inplace=True)
        print(df5)

        source = ColumnDataSource(df5)

        p5 = figure(x_axis_type="datetime", title=title5)
        p5.line('Date', 'temp', line_color="black", source=source)
        p5.xaxis.axis_label = 'Date'
        p5.yaxis.axis_label = 'Celcius'
        p5.grid.grid_line_alpha = 0
        p5.ygrid.band_fill_color = "olive"
        p5.ygrid.band_fill_alpha = 0.1
        p5.background_fill_color = "beige"
        p5.background_fill_alpha = 0.5
        p5.extra_y_ranges = {'rain': Range1d(start=0, end=1.0)}
        p5.add_layout(LinearAxis(y_range_name="rain", axis_label="in"), 'right')
        p5.circle('Date', 'rain', size=8, color='blue', alpha=0.2, legend='precip(in)', y_range_name='rain',
                  source=source)
        p5.legend.label_text_font_size = "8pt"
        # p1.legend.border_line_alpha = 0.01

        # prepare dataframe TURIN
        df6 = pd.DataFrame.from_dict(frame_turin, orient="index")
        df6.index.name = 'Date'
        df6.index = pd.to_datetime(df6.index)
        df6.sort_index(inplace=True)
        print(df6)

        source = ColumnDataSource(df6)

        p6 = figure(x_axis_type="datetime", title=title6)
        p6.line('Date', 'temp', line_color="black", source=source)
        p6.xaxis.axis_label = 'Date'
        p6.yaxis.axis_label = 'Celcius'
        p6.grid.grid_line_alpha = 0
        p6.ygrid.band_fill_color = "olive"
        p6.ygrid.band_fill_alpha = 0.1
        p6.background_fill_color = "beige"
        p6.background_fill_alpha = 0.5
        p6.extra_y_ranges = {'rain': Range1d(start=0, end=1.0)}
        p6.add_layout(LinearAxis(y_range_name="rain", axis_label="in"), 'right')
        p6.circle('Date', 'rain', size=8, color='blue', alpha=0.2, legend='precip(in)', y_range_name='rain',
                  source=source)
        p6.legend.label_text_font_size = "8pt"
        # p1.legend.border_line_alpha = 0.01

        # prepare dataframe ManCity
        df7 = pd.DataFrame.from_dict(frame_mancity, orient="index")
        df7.index.name = 'Date'
        df7.index = pd.to_datetime(df7.index)
        df7.sort_index(inplace=True)
        print(df7)

        source = ColumnDataSource(df7)
        p7 = figure(x_axis_type="datetime", title=title7)
        p7.line('Date', 'temp', line_color="black", source=source)
        p7.circle('Date', 'ftemp', size=8, color='blue', alpha=0.2, legend='Feels like (C)', source=source)
        p7.xaxis.axis_label = 'Date'
        p7.yaxis.axis_label = 'Celsius'
        p7.grid.grid_line_alpha=0.1
        p7.ygrid.band_fill_color="olive"
        p7.ygrid.band_fill_alpha = 0.1
        p7.background_fill_color = "mistyrose"


        # prepare dataframe ManCity
        df8 = pd.DataFrame.from_dict(frame_mancity, orient="index")
        df8.index.name = 'Date'
        df8.index = pd.to_datetime(df8.index)
        df8.sort_index(inplace=True)
        print(df8)

        source = ColumnDataSource(df8)
        p8 = figure(x_axis_type="datetime", title=title8)
        p8.line('Date', 'swind', line_color="black", source=source)
        p8.line('Date', 'gwind', line_color='cornflowerblue', legend='Gusts', source=source)
        p8.xaxis.axis_label = 'Date'
        p8.yaxis.axis_label = 'mph'
        p8.grid.grid_line_alpha = 0.1
        p8.ygrid.band_fill_color = "olive"
        p8.ygrid.band_fill_alpha = 0.1
        p8.background_fill_color = "lemonchiffon"

        # prepare dataframe ManCity
        df9 = pd.DataFrame.from_dict(frame_mancity, orient="index")
        df9.index.name = 'Date'
        df9.index = pd.to_datetime(df9.index)
        df9.sort_index(inplace=True)
        print(df9)

        source = ColumnDataSource(df9)
        p9 = figure(x_axis_type="datetime", title=title9)
        p9.circle('Date', 'precip_prob', size=7, color='white', alpha=0.5, source=source)
        p9.xaxis.axis_label = 'Date'
        p9.yaxis.axis_label = '%'
        p9.grid.grid_line_alpha = 0.1
        p9.ygrid.band_fill_color = "olive"
        p9.ygrid.band_fill_alpha = 0.1
        p9.background_fill_color = "deepskyblue"

        # prepare dataframe ManUtd
        df10 = pd.DataFrame.from_dict(frame_manunited, orient="index")
        df10.index.name = 'Date'
        df10.index = pd.to_datetime(df10.index)
        df10.sort_index(inplace=True)
        print(df8)
        source = ColumnDataSource(df10)
        p10 = figure(x_axis_type="datetime", title=title10)
        p10.line('Date', 'temp', line_color="black", source=source)
        p10.circle('Date', 'ftemp', size=8, color='blue', alpha=0.2, legend='Feels like (C)', source=source)
        p10.xaxis.axis_label = 'Date'
        p10.yaxis.axis_label = 'Celsius'
        p10.grid.grid_line_alpha = 0.1
        p10.ygrid.band_fill_color = "olive"
        p10.ygrid.band_fill_alpha = 0.1
        p10.background_fill_color = "mistyrose"

        # prepare dataframe ManUtd
        df11 = pd.DataFrame.from_dict(frame_manunited, orient="index")
        df11.index.name = 'Date'
        df11.index = pd.to_datetime(df11.index)
        df11.sort_index(inplace=True)
        print(df11)

        source = ColumnDataSource(df11)
        p11 = figure(x_axis_type="datetime", title=title11)
        p11.line('Date', 'swind', line_color="black", source=source)
        p11.line('Date', 'gwind', line_color='cornflowerblue', legend='Gusts', source=source)
        p11.xaxis.axis_label = 'Date'
        p11.yaxis.axis_label = 'mph'
        p11.grid.grid_line_alpha = 0.1
        p11.ygrid.band_fill_color = "olive"
        p11.ygrid.band_fill_alpha = 0.1
        p11.background_fill_color = "lemonchiffon"

        # prepare dataframe ManUtd
        df12 = pd.DataFrame.from_dict(frame_manunited, orient="index")
        df12.index.name = 'Date'
        df12.index = pd.to_datetime(df12.index)
        df12.sort_index(inplace=True)
        print(df12)

        source = ColumnDataSource(df12)
        p12 = figure(x_axis_type="datetime", title=title12)
        p12.circle('Date', 'precip_prob', size=7, color='white', alpha=0.5, source=source)
        p12.xaxis.axis_label = 'Date'
        p12.yaxis.axis_label = '%'
        p12.grid.grid_line_alpha = 0.1
        p12.ygrid.band_fill_color = "olive"
        p12.ygrid.band_fill_alpha = 0.1
        p12.background_fill_color = "deepskyblue"

        # prepare dataframe LiverpoolFC
        df13 = pd.DataFrame.from_dict(frame_liverpoolfc, orient="index")
        df13.index.name = 'Date'
        df13.index = pd.to_datetime(df13.index)
        df13.sort_index(inplace=True)
        print(df13)

        source = ColumnDataSource(df13)
        p13 = figure(x_axis_type="datetime", title=title13)
        p13.line('Date', 'temp', line_color="black", source=source)
        p13.circle('Date', 'ftemp', size=8, color='blue', alpha=0.2, legend='Feels like (C)', source=source)
        p13.xaxis.axis_label = 'Date'
        p13.yaxis.axis_label = 'Celsius'
        p13.grid.grid_line_alpha = 0.1
        p13.ygrid.band_fill_color = "olive"
        p13.ygrid.band_fill_alpha = 0.1
        p13.background_fill_color = "mistyrose"

        # prepare dataframe LiverpoolFC
        df14 = pd.DataFrame.from_dict(frame_liverpoolfc, orient="index")
        df14.index.name = 'Date'
        df14.index = pd.to_datetime(df14.index)
        df14.sort_index(inplace=True)
        print(df14)

        source = ColumnDataSource(df14)
        p14 = figure(x_axis_type="datetime", title=title14)
        p14.line('Date', 'swind', line_color="black", source=source)
        p14.line('Date', 'gwind', line_color='cornflowerblue', legend='Gusts', source=source)
        p14.xaxis.axis_label = 'Date'
        p14.yaxis.axis_label = 'mph'
        p14.grid.grid_line_alpha = 0.1
        p14.ygrid.band_fill_color = "olive"
        p14.ygrid.band_fill_alpha = 0.1
        p14.background_fill_color = "lemonchiffon"

        # prepare dataframe LiverpoolFC
        df15 = pd.DataFrame.from_dict(frame_liverpoolfc, orient="index")
        df15.index.name = 'Date'
        df15.index = pd.to_datetime(df15.index)
        df15.sort_index(inplace=True)
        print(df15)

        source = ColumnDataSource(df15)
        p15 = figure(x_axis_type="datetime", title=title15)
        p15.circle('Date', 'precip_prob', size=7, color='white', alpha=0.5, source=source)
        p15.xaxis.axis_label = 'Date'
        p15.yaxis.axis_label = '%'
        p15.grid.grid_line_alpha = 0.1
        p15.ygrid.band_fill_color = "olive"
        p15.ygrid.band_fill_alpha = 0.1
        p15.background_fill_color = "deepskyblue"

        # prepare dataframe Everton
        df16 = pd.DataFrame.from_dict(frame_everton, orient="index")
        df16.index.name = 'Date'
        df16.index = pd.to_datetime(df16.index)
        df16.sort_index(inplace=True)
        print(df16)
        source = ColumnDataSource(df16)
        p16 = figure(x_axis_type="datetime", title=title16)
        p16.line('Date', 'temp', line_color="black", source=source)
        p16.circle('Date', 'ftemp', size=8, color='blue', alpha=0.2, legend='Feels like (C)', source=source)
        p16.xaxis.axis_label = 'Date'
        p16.yaxis.axis_label = 'Celsius'
        p16.grid.grid_line_alpha = 0.1
        p16.ygrid.band_fill_color = "olive"
        p16.ygrid.band_fill_alpha = 0.1
        p16.background_fill_color = "mistyrose"

        # prepare dataframe Everton
        df17 = pd.DataFrame.from_dict(frame_everton, orient="index")
        df17.index.name = 'Date'
        df17.index = pd.to_datetime(df17.index)
        df17.sort_index(inplace=True)
        print(df11)

        source = ColumnDataSource(df17)
        p17 = figure(x_axis_type="datetime", title=title17)
        p17.line('Date', 'swind', line_color="black", source=source)
        p17.line('Date', 'gwind', line_color='cornflowerblue', legend='Gusts', source=source)
        p17.xaxis.axis_label = 'Date'
        p17.yaxis.axis_label = 'mph'
        p17.grid.grid_line_alpha = 0.1
        p17.ygrid.band_fill_color = "olive"
        p17.ygrid.band_fill_alpha = 0.1
        p17.background_fill_color = "lemonchiffon"

        # prepare dataframe Everton
        df18 = pd.DataFrame.from_dict(frame_everton, orient="index")
        df18.index.name = 'Date'
        df18.index = pd.to_datetime(df18.index)
        df18.sort_index(inplace=True)
        print(df18)

        source = ColumnDataSource(df18)
        p18 = figure(x_axis_type="datetime", title=title18)
        p18.circle('Date', 'precip_prob', size=7, color='white', alpha=0.5, source=source)
        p18.xaxis.axis_label = 'Date'
        p18.yaxis.axis_label = '%'
        p18.grid.grid_line_alpha = 0.1
        p18.ygrid.band_fill_color = "olive"
        p18.ygrid.band_fill_alpha = 0.1
        p18.background_fill_color = "deepskyblue"

        # prepare dataframe ACMilan
        df19 = pd.DataFrame.from_dict(frame_acmilan, orient="index")
        df19.index.name = 'Date'
        df19.index = pd.to_datetime(df19.index)
        df19.sort_index(inplace=True)
        print(df19)

        source = ColumnDataSource(df19)
        p19 = figure(x_axis_type="datetime", title=title19)
        p19.line('Date', 'temp', line_color="black", source=source)
        #p19.circle('Date', 'ftemp', size=8, color='blue', alpha=0.2, legend='Feels like (C)', source=source)
        p19.xaxis.axis_label = 'Date'
        p19.yaxis.axis_label = 'Celsius'
        p19.grid.grid_line_alpha = 0.1
        p19.ygrid.band_fill_color = "olive"
        p19.ygrid.band_fill_alpha = 0.1
        p19.background_fill_color = "mistyrose"

        # prepare dataframe ACMilan
        df20 = pd.DataFrame.from_dict(frame_acmilan, orient="index")
        df20.index.name = 'Date'
        df20.index = pd.to_datetime(df20.index)
        df20.sort_index(inplace=True)
        print(df14)

        source = ColumnDataSource(df20)
        p20 = figure(x_axis_type="datetime", title=title20)
        p20.line('Date', 'swind', line_color="black", source=source)
        #p20.line('Date', 'gwind', line_color='cornflowerblue', legend='Gusts', source=source)
        p20.xaxis.axis_label = 'Date'
        p20.yaxis.axis_label = 'mph'
        p20.grid.grid_line_alpha = 0.1
        p20.ygrid.band_fill_color = "olive"
        p20.ygrid.band_fill_alpha = 0.1
        p20.background_fill_color = "lemonchiffon"

        # prepare dataframe ACMilan
        df21 = pd.DataFrame.from_dict(frame_acmilan, orient="index")
        df21.index.name = 'Date'
        df21.index = pd.to_datetime(df21.index)
        df21.sort_index(inplace=True)
        print(df21)

        source = ColumnDataSource(df21)
        p21 = figure(x_axis_type="datetime", title=title21)
        p21.circle('Date', 'precip_prob', size=7, color='white', alpha=0.5, source=source)
        p21.xaxis.axis_label = 'Date'
        p21.yaxis.axis_label = '%'
        p21.grid.grid_line_alpha = 0.1
        p21.ygrid.band_fill_color = "olive"
        p21.ygrid.band_fill_alpha = 0.1
        p21.background_fill_color = "deepskyblue"

        # prepare dataframe Juventus
        df22 = pd.DataFrame.from_dict(frame_juventus, orient="index")
        df22.index.name = 'Date'
        df22.index = pd.to_datetime(df22.index)
        df22.sort_index(inplace=True)
        print(df16)
        source = ColumnDataSource(df22)
        p22 = figure(x_axis_type="datetime", title=title22)
        p22.line('Date', 'temp', line_color="black", source=source)
        #p22.circle('Date', 'ftemp', size=8, color='blue', alpha=0.2, legend='Feels like (C)', source=source)
        p22.xaxis.axis_label = 'Date'
        p22.yaxis.axis_label = 'Celsius'
        p22.grid.grid_line_alpha = 0.1
        p22.ygrid.band_fill_color = "olive"
        p22.ygrid.band_fill_alpha = 0.1
        p22.background_fill_color = "mistyrose"

        # prepare dataframe Juventus
        df23 = pd.DataFrame.from_dict(frame_juventus, orient="index")
        df23.index.name = 'Date'
        df23.index = pd.to_datetime(df23.index)
        df23.sort_index(inplace=True)
        print(df23)

        source = ColumnDataSource(df23)
        p23 = figure(x_axis_type="datetime", title=title23)
        p23.line('Date', 'swind', line_color="black", source=source)
        #p23.line('Date', 'gwind', line_color='cornflowerblue', legend='Gusts', source=source)
        p23.xaxis.axis_label = 'Date'
        p23.yaxis.axis_label = 'mph'
        p23.grid.grid_line_alpha = 0.1
        p23.ygrid.band_fill_color = "olive"
        p23.ygrid.band_fill_alpha = 0.1
        p23.background_fill_color = "lemonchiffon"

        # prepare dataframe Juventus
        df24 = pd.DataFrame.from_dict(frame_juventus, orient="index")
        df24.index.name = 'Date'
        df24.index = pd.to_datetime(df24.index)
        df24.sort_index(inplace=True)
        print(df18)

        source = ColumnDataSource(df24)
        p24 = figure(x_axis_type="datetime", title=title24)
        p24.circle('Date', 'rain', size=7, color='white', alpha=0.5, source=source)
        p24.xaxis.axis_label = 'Date'
        p24.yaxis.axis_label = '%'
        p24.grid.grid_line_alpha = 0.1
        p24.ygrid.band_fill_color = "olive"
        p24.ygrid.band_fill_alpha = 0.1
        p24.background_fill_color = "deepskyblue"


        output_file("consumer.html")

        save(gridplot([[p1,p2,p3,p4,p5,p6],[p7,p8,p9,p10,p11,p12],[p13,p14,p15,p16,p17,p18],[p19,p20,p21,p22,p23,p24]],
                      plot_width=280, plot_height=180))


    def main(self):
        # listen to when a new file is created
        listen_dir = 'data'

        #initialise files
        moFile = 'data/mo_20180316_034523.pkl'
        owFile = 'data/ow_20180316_034513.pkl'
        xuFile = 'data/xu_20180316_034508.pkl'

        while True: #loop until user terminates
            inotify = INotify()
            watch_flags = flags.CREATE  # | flags.DELETE | flags.MODIFY | flags.DELETE_SELF
            wd = inotify.add_watch(listen_dir, watch_flags)
            print("Listening... (Ctrl-C to terminate)")
            for event in inotify.read():
                print("stop C")
                if flags.CREATE in event:
                    print('File created in', event)
                    newfile = event[3]
                    print('Filename = ', newfile, 'TYPE = ', type(newfile))

                    if 'mo' in newfile:
                        moFile = newfile
                    elif 'ow' in newfile:
                        owFile = newfile
                    elif 'xu' in newfile:
                        xuFile = newfile
                    else:
                        continue

                    with open(newfile, 'rb') as f:  # stdout of newfile that was created
                        pick = (pickle.load(f))
                        print('pick = ', pick)

                    self.plot(moFile,owFile,xuFile)


if __name__ == '__main__':
    Consumer().main()
