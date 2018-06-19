# Created by zhouwang on 2018/6/8.

from .base import BaseRequestHandler, permission

class History():
    def __init__(self):
        pass

    def _query(self):
        select_sql = '''
          SELECT
            uri,
            method,
            reqdata,
            date_format(record_time, "%%Y-%%m-%%d %%H:%%i:%%s") as record_time
          FROM
            auditlog
          WHERE 
            user_id="%s"
          ORDER BY -record_time                  
        ''' % (self.requser['id'])

        self.mysqldb_cursor.execute(select_sql)
        results = self.mysqldb_cursor.fetchall()
        return {'code': 200, 'msg': 'Query Successful', 'data': results}

class Handler(BaseRequestHandler, History):
    @permission()
    def get(self):
        response_data = self._query()
        self._write(response_data)