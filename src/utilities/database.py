import psycopg2 as pg

class Database:

    def __init__(self, database: str, user: str = None, password: str = None, host: str = None, port: int = None):
        paramlist = []

        if database is not None:
            paramlist.append("dbname=" + database)
        
        if user is not None:
            paramlist.append("user=" + user)
        
        if password is not None:
            paramlist.append("password=" + password)
        
        if host is not None:
            paramlist.append("host=" + host)
        
        if port is not None:
            paramlist.append("port=" + str(port))
        
        self.dsn = " ".join(paramlist)

    def execute_query(self, sql: str, mapping = None):
        try:
            with pg.connect(dsn=self.dsn) as connection:
                with connection.cursor() as cursor:
                    if mapping is None:
                        cursor.execute(sql)
                    else:
                        cursor.execute(sql, mapping)
                    
                    return cursor.fetchall()

        except Exception as e:
            print(e)
    
    def execute_update(self, sql: str):
        try:
            with pg.connect(dsn=self.dsn) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql)

        except Exception as e:
            print(e)
