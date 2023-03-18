from psycopg_pool import ConnectionPool
import os
import sys

class DB:
  def __init__(self):
    self.init_pool()

  def init_pool(self):
    connection_url = os.getenv("CONNECTION_URL")
    self.pool = ConnectionPool(connection_url)

  def query_commit(self):
    try:
        conn = self.pool.connection()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except Exception as err:
        self.print_sql_err(err)

  def query_array_json(self,sql):
    print("SEQUEL STATEMENT-[Array]----------")
    print(sql)

    wrapped_sql = self.query_wrap_array(sql)    
    with self.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(wrapped_sql)
          json = cur.fetchone()
          return json[0]

  def query_object_json(self,sql):
    print("SEQUEL STATEMENT-[Object]----------")
    print(sql)

    wrapped_sql = self.query_wrap_object(sql)    
    with self.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(wrapped_sql)
          json = cur.fetchone()
          return json[0]

  def query_wrap_object(self, template):
    sql = f"""
    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
    {template}
    ) object_row);
    """
    return sql

  def query_wrap_array(self,template):
    sql = f"""
    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
    {template}
    ) array_row);
    """
    return sql

  def print_sql_err(self,err):

    err_type,err_obj,trcaceback = sys.exc_info()

    line_num = traceback.tb_lineno

    print("\n psycopg2 ERROR:", err, "on line number;", line_num)
    print("psycopg2 traceback:", traceback, "--type:", err_type)

    print("\nextensions.Diagnostics:", err.diag)

    print("pgerror:",err.pgerror)
    print("pgcode:",err.pgcode, "\n")

db = DB()