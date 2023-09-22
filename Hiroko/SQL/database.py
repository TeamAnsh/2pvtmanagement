import psycopg2

DB = psycopg2.connect(host='balarama.db.elephantsql.com',
                    port='5432',
                    user='nizpwdkk',
                    password='0vZaMzYqpIqlbzfZVRenc4WQ50uv63rX',
                    database='nizpwdkk'
                    )

cusr = DB.cursor()
DB.rollback()
DB.autocommit = True
