Run python logs_analysis.py

Will create a text file (answers_file.txt) with three sections:
    -Top three read articles by descending number of logs
    -Top authors by descending total of page views
    -Days where more than 1% of requests were sent back with an error status
    
In first section, creates a CASE WHEN statement based on article path in log table, which corresponds to article title from articles table. Non-article paths are filtered out.

In second section, article titles within the CASE WHEN statement used to join articles and logs tables on title.

In third section, two separate queries were used to get:
    -A count of returned error statuses by date
    -A count of all returned statuses by date
This returns two lists of tuples, which are changed to dictionaries (lines 102-109) for easier iteration. Finally, loop through the two dictionaries to get the number of error statuses/all statuses (error_percentage) by date.