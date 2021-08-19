from common.execSql import ExecSql
from common.logs import Log
from common.readData import ReadData
from common.readFile import ReadFile

class BasicLogic(object):
    log = Log()
    url_data = ReadFile().read_urlfile()
    sql_exec = ExecSql('mysql_yt')
    sql_exec_basic = ExecSql('mysql_basic')
    sql = ReadData().read_sqlfile()
    update_data = ReadData().read_updatedata()
