### Introduction
The objective was to build a dashboard that is sufficiently high level for easy reference through data visualisation, 
and should also be reproducible, extensible and scalable. The Client is concerned with the effects of weather
that might affect the outcome of sporting events, and requires forecasting data from 3 sources to assist
in improving their prediction models so that it can in turn provide a realistic user experience on their gaming platform.
 

### Installation (Unix)
1. Install the folder as source root of the project (you may want to do so in virtualenv - please see Notes for instruction)
2. In shell, **'pip install -r requirements.txt'**
3. In your IDE (or separate sessions in shell), start 'consumer.py' to begin listening for newly created files.
4. Start 'mo.py', 'ow.py', 'xu.py' to begin producing data. You have to insert your API keys in these programs.
5. Start 'visualise.py' and view through your browser <http://localhost:8080> or visit [link](http://35.178.148.146/) 
(the author has hosted it on an EC2 instance).

_Notes_
To install **virtualenv**, in shell:
- 'cd' to main directory (e.g. 'cd rush')
- 'pip install virtualenv'
- 'virtualenv rushenv'
- 'source rushenv/bin/activate'
You are now in virtual environment and can start the installation as above. In shell, 'deactivate' to 
exit the virtual environment.
 

### Approach
The two main considerations for designing the solution was 1) determining the relevant data to extract, and 2) building
the pipeline for which the data is extracted, processed and served, as part of the wider ETL concept. 

1) A review of the data available from the 3 sources, including the structure and format in which data is presented,
revealed that it was not possible to cursorily determine which service provider offered the most accurate
prediction as there was no historical data for forecast vs actual weather variables. Although most of the key variables,
such as temperature, precipitation, wind, etc were available from all service providers, they varied in the time steps that
were callable, and also variations exist in the way that a key variable was described. For example, 'Wind' would be described
in subsets as 'Wind Speed' and 'Gusts' by the Met Office (MO), whereas Open Weather (OW) presents only wind speed as an average.
Granularity can also be observed in the time steps available, where APIXU (XU) only gives forecast as daily averages in the free version, whereas
MO and OW are able to drill down to hourly forecasts. With the incompleteness of data from any one source, the general idea
was to use the different sources of data to complement each other and fill a predetermined unified data frame. It could
also be used as a broad validation across providers. For example, a 5-day average forecast for the 6 cities was provided by
XU, and can be used as a check on reality, whereas location specific data for the purpose of grid granularity
was provided by MO and OW.

    In terms of outdoor competitive sporting events where fine margins determine outcome, space partitioning and finer time steps 
    become more important. As examples, the information on the dashboard provides location specific forecasts for 
    a few top football clubs in Manchester, Liverpool and Milan. More specific locations can be added in future from 
    a drop down menu. Co-ordinates of the center of the football pitch were obtained using Google Maps in finding the closest
    weather station to give as accurate readings, and arguably forecasts, as possible. 'Wind Gusts' might then become more
    relevant for a football team that kicks high balls into their opponent's half as an offensive strategy. In tennis, some 
    players are known to be good 'wind players', and are usually those that play with a lot of top spin off the ball that 
    land well within the boundaries of the court, rather than those that have flatter strokes that rely on striking the ball 
    to land close to the lines to effect the same velocity and positional advantage, given the flatter trajectory. Rainfall
    is also known to affect a rugby match and horse racing, but not always during the actual match, but how it affects the
    grounds as a result of earlier and/or sustained precipitation.
    
    Based on the principles above, the task was to extract data from MO, OW, and XU to build a data frame with the following keys:
    **'timestamp','temp', 'temp feels like', 'textual description', 'wind speed', 'wind gust', 'precip prob', 'rainfall', 'location'.**

2) The architecture replicates a publish/subscribe message queueing model, such as that used in Kafka, so that data can be streamed
using the methodology where data would be Produced by separate applications (extraction via API) 
and pushed to a virtual repository, in this case a simple folder. Another application, acting on top of the folder, listens
to new file logs as an when they are created, where it also acts as the Consumer of the data and transforms the data for further usage by 
other applications. So the flow of the data can be represented by data>producer>folder application>consumer, where the endpoint 
would be the dashboard for Business Intelligence as a data stream. Separately, the data can be persisted into an analytical database
where it can be recalled for predictive models.

    Based on the above, the 3 programs producing the data after extracting from source are **'mo.py'**, **'ow.py'**, and **'xu.py'**. 
    This is supported by **'consumer.py'** that, together with the folder that the binary files are stored in, transforms the data for 
    Consumption. **'visualise.py'**, is a high level application that uses an asynchronous, non-blocking Tornado webserver instance, 
    to serve the data visualisations, **'consumer.html'**, after they are processed. The merits of structuring the architecture as 
    microservices within a pub/sub message queuing environment are a combination of fault-tolerance, parallelism, scalability, 
    extensibility, and streaming of raw or processed data in an efficient and timely manner, without needing to invoke costly read/writes
    to a transactional database.
    
    Lastly, for rapid deployment, Bokeh, a high level data visualisation tool is used. The Producer applications publish the data
    as serialised Python dictionaries, and loaded in Pandas data frames within the Consumer application, and to Bokeh 
    as the dataset for rendering the plots. Bokeh has a lot of inbuilt functions for visualising data and for designing layout,
    as well as highly customisable as a low level implementation. 
    
### Future development

The above represents a minimum viable product in which the author hopes to raise important considerations when 
designing the product, and serves as a working prototype in which to engage with the Stakeholders for further developements.
Using the pub/sub and microservice model, one could also build thin API layers on top of the pipeline for machine learning
and other anaytical SQL queries. Some added specifications could be as follow:
- Install databases to collect forecast weather information to perform analysis of historical accuracy
- Connect to a Kafka cluster as part of the mainstream architecture
- Enrich the data with online textual evidence of weather conditions affecting the psychology of a player or team using NLP.
One could look at social media, such as Twitter or Facebook accounts, and study if there is a correlation between weather,
perception, and actual performance.
- Use video analytics to look for visual cues that support or augment a hypothesis.

