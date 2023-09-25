import psycopg2

DB = psycopg2.connect(host='tai.db.elephantsql.com',
                    port='5432',
                    user='pokleimf',
                    password='0vZaMzYqpIqlbzfZVRenc4WQ50uv63rX',
                    database='pokleimf'
                    )

cusr = DB.cursor()
DB.rollback()
DB.autocommit = True
