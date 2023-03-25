from psycopg_pool import ConnectionPool
import os
import sys
import re 
from flask import current_app as app

class DB:
  def __init__(self):
    self.init_pool()

  def init_pool(self):
    connection_url = os.getenv("CONNECTION_URL")
    self.pool = ConnectionPool(connection_url)


  def load_template(self,*args):
    pathh = list((app.root_path,'db','sql',) + args)
    pathh[-1] = pathh[-1] + ".sql"

    template_path = os.path.join(*pathh)
    with open(template_path, 'r') as f:
      template_content = f.read()
    return template_content

  def print_sql(self,title,sql,params={}):
    cyan = '\033[96m'
    no_color = '\033[0m'
    print("\n")
    print(f'{cyan}SQL STATEMENT [{title}]---------{no_color}')
    print(sql, params)

  def query_commit(self,sql,params={}):

    self.print_sql('commit with returning', sql,params)

    pattern = r"\bRETURNING\b"
    is_returning_id = re.search(pattern,sql)
    try:
      with self.pool.connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        if is_returning_id:
          returning_id = cur.fetchone()[0]
        conn.commit()
        if is_returning_id:
          return returning_id
    except Exception as err:
        self.print_sql_err(err)

  def query_value(self,sql,params={}):
    self.print_sql('value',sql,params)

    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql,params)
        json = cur.fetchone()
        return json[0]

  def query_array_json(self,sql,params={}):
    self.print_sql('array', sql)

    wrapped_sql = self.query_wrap_array(sql)    
    with self.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(wrapped_sql,params)
          json = cur.fetchone()
          return json[0]

  def query_object_json(self,sql,params={}):
    self.print_sql('json object', sql)

    wrapped_sql = self.query_wrap_object(sql)    
    with self.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(wrapped_sql,params)
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

    err_type,err_obj,traceback = sys.exc_info()

    line_num = traceback.tb_lineno

    print("\n psycopg2 ERROR:", err, "on line number;", line_num)
    print("psycopg2 traceback:", traceback, "--type:", err_type)

    print("pgerror:",err.pgerror)
    print("pgcode:",err.pgcode, "\n")

db = DB()