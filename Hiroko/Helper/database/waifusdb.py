import psycopg2

DB = psycopg2.connect(host='tai.db.elephantsql.com',
                    port='5432',
                    user='pokleimf',
                    password='dn37hWi2kyfPJNimo7Dx2vsxvm9615VM',
                    database='pokleimf'
                    )

cusr = DB.cursor()
DB.rollback()
DB.autocommit = True
