import psycopg2
import datetime
#import pandas as pd

db = psycopg2.connect("dbname=news")
cursor = db.cursor()

#Question 1
top_views = ("""
             SELECT case when SUBSTRING(path,10,length(path)-10) like '%candidate-is%' then 'Candidate is jerk, alleges rival'
            when SUBSTRING(path,10,length(path)-10) like '%so-many-bear%' then 'There are a lot of bears'
            when SUBSTRING(path,10,length(path)-10) like '%trouble-for-trouble%' then 'Trouble for troubled troublemakers'
            when SUBSTRING(path,10,length(path)-10) like '%balloon-goons-doome%' then 'Balloon goons doomed'
            when SUBSTRING(path,10,length(path)-10) like '%media-obsessed-with-bear%' then 'Media obsessed with bears'
            when SUBSTRING(path,10,length(path)-10) like '%bad-things-gon%' then 'Bad things gone, say good people'
            when SUBSTRING(path,10,length(path)-10) like '%goats-eat-google%' then 'Goats eat Google lawn'
            when SUBSTRING(path,10,length(path)-10) like '%bears-love-berri%' then 'Bears love berries, alleges bear'
            END as path, COUNT(*) FROM log 
            WHERE path like '%article%' 
            GROUP BY SUBSTRING(path,10,length(path)-10) ORDER BY COUNT(*) desc
            LIMIT 3
""")

cursor.execute(top_views)
results = cursor.fetchall()
#print results

#Creating answers text file
with open('answers_file.txt', 'w') as f:
    f.write("Top viewed articles:\n")
    for item in results:
        f.write(str(item)+"\n")
    f.write("\n")
        
        
#Question 2        
test_authors_sql = ("""
            SELECT au.name, count(log)
            
            FROM authors au, articles art,
            (
                SELECT case when SUBSTRING(path,10,length(path)-10) like '%candidate-is%' then 'Candidate is jerk, alleges rival'
                when SUBSTRING(path,10,length(path)-10) like '%so-many-bear%' then 'There are a lot of bears'
                when SUBSTRING(path,10,length(path)-10) like '%trouble-for-trouble%' then 'Trouble for troubled troublemakers'
                when SUBSTRING(path,10,length(path)-10) like '%balloon-goons-doome%' then 'Balloon goons doomed'
                when SUBSTRING(path,10,length(path)-10) like '%media-obsessed-with-bear%' then 'Media obsessed with bears'
                when SUBSTRING(path,10,length(path)-10) like '%bad-things-gon%' then 'Bad things gone, say good people'
                when SUBSTRING(path,10,length(path)-10) like '%goats-eat-google%' then 'Goats eat Google lawn'
                when SUBSTRING(path,10,length(path)-10) like '%bears-love-berri%' then 'Bears love berries, alleges bear'
                END as path, ip, method, status, time, id FROM log 
                WHERE path like '%article%' 
            ) log
            WHERE log.path = art.title
            AND au.id = art.author
            GROUP BY au.name ORDER BY COUNT(log) desc
            LIMIT 3
""")

test = ("""
        SELECT * FROM articles LIMIT 5
""")

cursor.execute(test_authors_sql)
test_authors = cursor.fetchall()
#print test_authors

#Appending top author results to answers text file
with open('answers_file.txt', 'a') as f:
    f.write("Most read authors:\n")
    for item in test_authors:
        f.write(str(item)+"\n")
        
        
#Question 3
error_percentage = ("""
            SELECT date(log.time) as request_date, (count(error_log)*100)/count(log) as error_percentage
                FROM log,
                (SELECT * from log WHERE CAST(substring(status,1,3) as int) between 400 and 599) error_log
    
            WHERE 1=1
            AND log.id = error_log.id
            GROUP BY date(log.time)
            HAVING CAST(count(error_log)/count(log) AS numeric) >= .01
""")

error_logs = ("""
        SELECT CAST(time AS date) as date, count(*) from log WHERE CAST(substring(status,1,3) as int) between 400 and 599
        GROUP BY CAST(time AS date)
""")

all_logs = ("""
        SELECT CAST(time AS date) as date, count(*) from log
        GROUP BY CAST(time AS date)
""")


cursor.execute(error_logs)
error_logs = cursor.fetchall()
cursor.execute(all_logs)
all_logs = cursor.fetchall()

#converting lists of tuples to dictionaries
error_logs_dict = {}
all_logs_dict = {}

for a,b in error_logs:
    error_logs_dict.setdefault(a, b)
for c,d in all_logs:
    all_logs_dict.setdefault(c, d)

#Creating dictionary of days with error percentage higher than 1%
high_error_days = {}

for key in error_logs_dict.keys():
    val1 = float(error_logs_dict[key])
    val2 = float(all_logs_dict[key])
    error_percentage = val1/val2
    if error_percentage >= 0.01:
        new_key = datetime.datetime.strftime(key,'%m-%d-%Y')
        high_error_days[new_key] = error_percentage

#print high_error_days

#Appending top author results to answers text file
with open('answers_file.txt', 'a') as f:
    f.write('\n')
    for k,v in high_error_days.iteritems():
        f.write("On {}, there was an error percentage of {}\n".format(k,v))