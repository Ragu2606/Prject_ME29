**Census Data Processing and Analysis**

**Overview**

This project aims to clean, process, and analyze census data sourced from a given dataset. The tasks include renaming columns for uniformity, standardizing state/UT names, handling new state/UT formations, dealing with missing data, storing data in a MongoDB database, connecting to a relational database, and running queries to extract insights from the data.

**Dataset**

The dataset can be accessed from the following URL: [Dataset](https://drive.google.com/drive/folders/10FLf8dEXqz_vc8p4DVoA5MKAh60gp1f6)

**Problem Statement**

The task involves several data preprocessing and analysis steps, including:

Renaming column names for uniformity.

Standardizing state/UT names.

Handling new state/UT formations.

Finding and processing missing data.

Saving data to MongoDB.

Establishing a database connection and uploading data.

Running queries on the database to extract insights.

**Tasks**

Task 1: Rename Column Names
Columns are renamed to ensure uniformity and consistency across datasets.

Task 2: Rename State/UT Names
State/UT names are standardized to have only the first character of each word capitalized, except for the word "and," which remains lowercase.

Task 3: New State/UT Formation
State/UT names are updated for districts affected by new state/UT formations.

Task 4: Find and Process Missing Data
Missing data is identified, and efforts are made to fill in missing values using information from other cells. The percentage of missing data for each column is calculated before and after the data-filling process.

Task 5: Save Data to MongoDB
Processed data is saved to MongoDB with a collection named "census."

Task 6: Database Connection and Data Upload
Data is fetched from MongoDB and uploaded to a relational database using Python code. Table names correspond to the file names without the extension, and primary key and foreign key constraints are included where necessary.

Task 7: Querying and Analysis
Various queries are run on the database to extract insights, including population statistics, literacy rates, household amenities, transportation modes, household sizes, income distribution, poverty rates, and more.

**Submission**

Python file containing the complete code for the project, organized into sections for data Pipeline and Analysis.

GitHub repository with a proper README file.

Presentation covering Problem Statement, Tools Used, Approaches, and Insights Found.
