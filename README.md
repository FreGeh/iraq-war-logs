# Iraq War Logs Data Visualization  

## Overview  
This project visualizes data from the **[Iraq War Logs](https://en.wikipedia.org/wiki/Iraq_War_documents_leak)**, a leak published by WikiLeaks containing over **360,000 SIGACT reports** from the Iraq War. The dataset, parsed into a CSV and hosted on Kaggle ([source](https://www.kaggle.com/datasets/martinmateo/iraq-war-logs)), includes numerical and geographical data, providing insights into various aspects of the conflict.  

Using **Dash, Plotly, Pandas, and Flask**, this project creates interactive visualizations to explore trends, geospatial patterns, and key events.  

## Plots  
- **Plot 1**: **Temporal Distribution** of Fatalities – Displays the number of daily deaths (civilians, enemy forces, friendly forces, and Iraqi forces) with an additional 14-day moving average for trend analysis.
- **Plot 2**: **Geographical Distribution** of Fatalities – A choropleth map showing the percentage of fatalities of different forces across Iraq's provinces over time, with an animated monthly progression. *(note: wait a few seconds when clicking on this plot for it to load)*
- **Plot 3**: **Categorical Breakdown** of Casualties by Cause – A treemap visualizing the distribution of casualties based on the type and category of incidents, providing an overview of major contributing factors.
- **Plot 4**: Civilian Casualties by **Perpetrator Affiliation** – A violin plot comparing civilian deaths and injuries caused by friendly versus enemy forces.
- **Plot 5**: Civilian Casualties by **Incident Type** – A scatter plot showing the average number of civilian casualties per incident type and category.

## Setup  

- **Create a virtual environment** and install the required libraries
- **Run ``dashboard.py``**