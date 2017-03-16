# -*- coding: UTF-8 -*-
import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
import logging
import logging.handlers

class MysqlConnector(object):
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现
    获取连接对象：conn = Mysql.getConn()
    释放连接对象: conn.close()或del conn
    """
    def __init__(self, host, port, user, passwd, dbname, mincached, \
                 maxusage, maxconn, retimes):
      self.__retry_times = retimes
      self.__init_logger(host, port, dbname)
      try:
        self.__pool = PooledDB(creator = MySQLdb, maxusage = maxusage, \
                         host = host, port = port, db = dbname,        \
                         user = user, passwd = passwd, blocking = True,\
                         mincached = mincached, maxcached = maxconn,   \
                         maxshared = maxconn, maxconnections = maxconn,\
                         setsession = ['SET AUTOCOMMIT = 1'])
      except Exception, e:
        self.logger.error('An exception happends when creating db pool in '
                          'host[%s]:port[%d] with [%s]' % (__host, __port, e))

    def __init_logger(self, db_host, db_port, db_name):
      logger_name = db_host + ':' + str(db_port) + ':' + db_name
      self.logger = logging.getLogger(logger_name)

    def query(self, sql):
      rows = []
      for i in range(self.__retry_times):
        try:
          conn = self.__pool.connection() 
          c = conn.cursor()
          c.execute(sql)
          rows = c.fetchall()
          break
        except Exception as e:
          self.logger.error("an exception is hanppened when execute "   \
              "statement:%s. Error info:%s, then retry %d time" % (sql, \
              str(e), i)) 
        finally:
          conn.close()

      return rows

    def execute(self, sql):
      for i in range(self.__retry_times):
        try:
          conn = self.__pool.connection() 
          c = conn.cursor()
          c.execute(sql)
          return True
        except Exception as e:
          self.logger.error("an exception is hanppened when execute "   \
              "statement:%s. Error info:%s, then retry %d time" % (sql, \
              str(e), i)) 
        finally:
          conn.close()

      return False

