from flask_records import RecordsDao
from flask_records.decorators import query, query_by_page
from flask import current_app


class BaseDao(RecordsDao):
    SELECT_SQL_BY_PID = 'SELECT * FROM {} WHERE public_id = :public_id'
    SELECT_SQL_ALL = 'SELECT * FROM {}'

    def __init__(self):
        super(BaseDao, self).__init__()

    def get_by_public_id(self, public_id):
        """
        Get the record according to the public_id
        """
        @query(BaseDao.SELECT_SQL_BY_PID.format(self.table_name), True)
        def _get(public_id):
            pass

        return _get(public_id)

    def retrieve_list_by_pagination(self, page: int, rpp: int):
        """
        Get the pagination data
        """
        @query_by_page(BaseDao.SELECT_SQL_ALL.format(self.table_name), page_size=rpp)
        def _get_by_pagination(page):
            pass

        return _get_by_pagination(page)

    def insert_many(self, sql, data):
        # 没有返回，如何判定数据库插入是否成功
        current_app.raw_db.bulk_query(sql, data)

