# Created by zhouwang on 2018/6/8.

from .base import BaseRequestHandler, permission

def query_valid(func):
    def _wrapper(self, pk):
        error = {}
        if not pk and self.request.arguments:
            argument_keys = self.request.arguments.keys()
            query_keys = ['id', 'uri', 'method', 'record_time']
            error = {key:'参数不可用' for key in argument_keys if key not in query_keys}
        if error:
            self._write({'code': 400, 'msg': 'Bad GET param', 'error': error})
            return
        return func(self, pk)
    return _wrapper

class Auditlog():
    def __init__(self):
        self.reqdata = {}

    @query_valid
    def _query(self, pk):
        select_sql = '''
            SELECT
              t1.id,
              t2.username,
              t1.uri,
              t1.method,  
              date_format(t1.record_time, "%%Y-%%m-%%d %%H:%%i:%%s") as record_time,
              t1.reqdata 
            FROM 
              auditlog t1
            INNER JOIN
              user t2
            ON
              t1.user_id = t2.id
            %s
        ''' % self.format_where_param(int(pk), self.request.arguments)
        self.mysqldb_cursor.execute(select_sql)
        results = self.mysqldb_cursor.fetchall()
        return {'code': 200, 'msg': 'Query Successful', 'data': results}

class Handler(BaseRequestHandler, Auditlog):
    @permission(role=1)
    def get(self, pk=0):
        ''' Query audit log '''
        response_data = self._query(int(pk))
        self._write(response_data)