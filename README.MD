## Instructions to Run:
Run the following commands in order:

    make setup

    make pipeline

    make dashboard

If sqlite3 throws a UNIQUE constraint error, then the database is already initialized

## Schema Explanation:
The database schema is a 1 to 1 translation of the csv file because the analyses use each column of the original data. 

It would scale well to hundreds of projects and thousands of samples because there is only a moderate number of columns in the schema, unless each project has thousands of samples. In that case, the database might need to load just a subset of the rows for each request.

Since the database captures all the information in the original dataset, it works well for many kinds of analyses. Some of the visualizations comparing categories, however, could not work if these categories began taking on more values. For example, comparing the number of melanoma samples on a bar graph per project works better if there are 3 projects instead of 100. If the analyses were outside the scope of the dataset, then the database schema would also have to be updated by hand.

## Code Structure
The code is separated into 3 Python files, load_data, pipeline, and dashboard. Because the makefile has 3 instructions, it made sense to separate code into 3 Python files. pipeline.py contains code to generate images, and dashboard.py both starts the dashboard and displays interactive graphs. pipeline.py has helper functions whose sole purpose is to process and return dataframes. Since these dataframes are both used to create images and appear on the dashboard, the helper functions save many lines of code.
