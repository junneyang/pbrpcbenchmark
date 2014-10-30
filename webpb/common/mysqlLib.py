#!/usr/bin/env python
#-*- coding: utf-8 -*-
from logLib import *
import datetime

import MySQLdb
host='10.48.55.39'
user='root'
passwd='Admin@123'
db='db_pb'
port=33306

from dynsqlLib import *

class mysqlLib():
    def __init__(self,host=host,user=user,passwd=passwd,db=db,port=port,charset='utf8'):
        try:
            self.host=host
            self.user=user
            self.passwd=passwd
            self.db=db
            self.port=port
            self.charset=charset
            self.conn=MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,port=self.port,charset=self.charset)
            self.cursor=self.conn.cursor()
        except Exception as e:
            logging.error(str(e))
    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            logging.error(str(e))
    ##################################################################server操作####################################################
    def add_server(self,param):
        try:
            sql="""insert into tbl_server(id,name,ip,username,password,workspace,belong,descpt) values(NULL,%s,%s,%s,%s,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    def query_server(self,param):
        try:
            s=DynSql("""select id,name,ip,workspace,belong,descpt,username,password from tbl_server where 1=1
            { and id=$id} { and belong=$belong}
            ORDER BY id DESC {limit {$offset,} $limit}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_server_totalcnt(self,param):
        try:
            s=DynSql("""select count(*) from tbl_server where 1=1
            { and belong=$belong}
            """)
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            totalcnt=ret[0][0]
            return ret
        except Exception as e:
            logging.error(str(e))
    def del_server(self,param):
        try:
            sql="delete from tbl_server where id=%s"
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))

    ##################################################################testdata操作####################################################
    def add_testdata(self,param):
        try:
            sql="""insert into tbl_testdata(id,type,name,belong,filenum,descpt) values(NULL,%s,%s,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    def query_testdata(self,param):
        try:
            s=DynSql("""select id,name,type,belong,filenum,descpt from tbl_testdata where 1=1
            { and id=$id} { and belong=$belong} { and type=$datatype}
            ORDER BY id DESC {limit {$offset,} $limit}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_testdata_totalcnt(self,param):
        try:
            s=DynSql("""select count(*) from tbl_testdata where 1=1
            { and belong=$belong} { and type=$datatype}
            """)
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            totalcnt=ret[0][0]
            return ret
        except Exception as e:
            logging.error(str(e))
    def add_datastr(self,param):
        try:
            sql="""insert into tbl_datafile(id,testdata_id,filename,filestr) values(NULL,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    def del_testdata(self,param):
        try:
            sql="delete from tbl_testdata where id=%s"
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def del_datafile(self,param):
        try:
            sql="delete from tbl_datafile where testdata_id=%s"
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))

    def query_datafile(self,param):
        try:
            s=DynSql("""select filename,filestr from tbl_datafile where 1=1
            { and testdata_id=$testdata_id}
            ORDER BY id DESC {limit {$offset,} $limit}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    ##################################################################download stat操作####################################################
    def add_downloadstat(self,param):
        try:
            sql="""insert into tbl_downloadstat(id,type,user,time) values(NULL,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    def query_downloadstat(self,period,param):
        try:
            if(period == 1):
                s=DynSql("""select type,count(*) from tbl_downloadstat where 1=1
                { and id=$id} and DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(time)
                group by type order by type""")
            else:
                s=DynSql("""select type,count(*) from tbl_downloadstat where 1=1
                { and id=$id}
                group by type order by type""")
            sql=s(param)
            #print sql[0] %sql[1]
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))



    def query_pjt(self,param):
        try:
            s=DynSql("""select * from tbl_project where 1=1 { and id=$id}
            { and name=$name} { and info=$info} { and status=$status} ORDER BY id DESC {limit {$offset,} $row_cnt}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            self.conn.commit()
            return ret
        except Exception as e:
            logging.error(str(e))
    def add_pjt(self,param):
        try:
            sql="insert into tbl_project(id,name,info,status) values(NULL,%s,%s,%s)"
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    def updata_pjt(self,param):
        try:
            sql="update tbl_project set name=%s,info=%s,status=%s where name=%s"
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def del_pjt(self,param):
        try:
            sql="delete from tbl_project where name=%s"
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def query_task(self,param):
        try:
            #sql="select * from tbl_task limit %s,%s"
            s=DynSql("""select * from tbl_task where 1=1 { and id=$id}
            { and pjt_id=$pjt_id} { and name=$name} { and version=$version} { and info=$info}
            { and testtype=$testtype} { and processtype=$processtype} { and filepath=$filepath} { and starttime=$starttime}
            { and endtime=$endtime} { and status=$status}
            ORDER BY id DESC {limit {$offset,} $row_cnt}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            self.conn.commit()
            return ret
        except Exception as e:
            logging.error(str(e))
    def add_task(self,param):
        try:
            sql="""insert into tbl_task(id,pjt_id,name,version,info,testtype,processtype,filepath,starttime,endtime,status)
            values(NULL,%s,%s,%s,%s,%s,%s,%s,NULL,NULL,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    def update_task_starttime(self,param):
        try:
            sql="""update tbl_task set starttime=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def update_task_endtime(self,param):
        try:
            sql="""update tbl_task set endtime=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def update_task_status(self,param):
        try:
            sql="""update tbl_task set status=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def del_task(self,param):
        try:
            sql="delete from tbl_task where name=%s"
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def add_script(self,param):
        try:
            sql="""insert into tbl_script(id,task_id,caseid,casename,starttime,endtime,result,testlog)
            values(null,%s,%s,%s,%s,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0

    ##################################
    def query_task_management(self,param):
        try:
            s=DynSql("""select * from tbl_task_management where 1=1 { and id=$id}
            { and pjt_id=$pjt_id} { and name=$name} { and version=$version} { and processtype=$processtype}
            { and testtype=$testtype} { and filepath=$filepath} { and info=$info}
            ORDER BY id DESC {limit {$offset,} $row_cnt}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_total_task_management(self,param):
        try:
            s=DynSql("""select * from tbl_task_management where 1=1 { and pjt_id=$pjt_id}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            cnt=self.cursor.rowcount
            return cnt
        except Exception as e:
            logging.error(str(e))
    def add_task_management(self,param):
        try:
            sql="""insert into tbl_task_management(id,pjt_id,name,version,processtype,testtype,filepath,info,benchmark_test_time,benchmark_test_data)
            values(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0

    def del_task_management(self,param):
        try:
            sql="delete from tbl_task_management where id=%s"
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def update_task_management(self,param):
        try:
            sql="""update tbl_task_management set pjt_id=%s,name=%s,version=%s,processtype=%s,testtype=%s,filepath=%s,info=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))

    def query_test_management(self,param):
        try:
            s=DynSql("""select * from tbl_test_management where 1=1 { and id=$id}
            { and task_id=$task_id} { and pjt_id=$pjt_id} { and testtype=$testtype} { and starttime=$starttime}
            { and endtime=$endtime} { and status=$status} { and log=$log} { and startby=$startby}
            ORDER BY id DESC {limit {$offset,} $row_cnt}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_test_management_early_date(self,param):
        try:
            s=DynSql("""select date(starttime) as date from tbl_test_management ORDER BY id ASC {limit {$offset,} $row_cnt}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_all_QA_RD(self):
        try:
            sql="""select distinct(startby) from tbl_test_management;"""
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()

            from SOAPpy import WSDL
            from SOAPpy import headerType
            wsdlUrl = 'http://itebeta.baidu.com:8102/ws/UserRemoteService?wsdl'
            server = WSDL.Proxy(wsdlUrl)
            hd = headerType(data={"appKey":"UICWSTestKey"})
            server.soapproxy.header = hd
            qa_list=[]
            rd_list=[]
            for item in ret:
                user = server.getUserByUsername(arg0=item[0])
                if(u'测试' in user.departmentName):
                    qa_list.append('\''+user.username+'\'')
                else:
                    rd_list.append('\''+user.username+'\'')
            #print user
            return qa_list,rd_list
        except Exception as e:
            logging.error(str(e))
    def query_usage_statbypeople_per_day(self,param):
        try:
            s=DynSql("""select date(starttime) as date,count(distinct startby) as usage_statbypeople_per_day from tbl_test_management
             where date(starttime)={$starttime}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_usage_statbypeople_per_day_qa(self,param):
        try:
            qa_list,rd_list=self.query_all_QA_RD()
            s=DynSql("""select date(starttime) as date,count(distinct startby) as usage_statbypeople_per_day from tbl_test_management
             where date(starttime)={$starttime} and startby in (%s)""" % (",".join(map(str,qa_list)))  )
            sql=s(param)
            #print sql[0]
            #print sql[1]
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_usage_statbypeople_per_day_rd(self,param):
        try:
            qa_list,rd_list=self.query_all_QA_RD()
            s=DynSql("""select date(starttime) as date,count(distinct startby) as usage_statbypeople_per_day from tbl_test_management
             where date(starttime)={$starttime} and startby in (%s)""" % (",".join(map(str,rd_list)))  )
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_usage_statbypeople_acc_day_qa(self,param):
        try:
            qa_list,rd_list=self.query_all_QA_RD()
            s=DynSql("""select count(distinct startby) as usage_per_day from tbl_test_management where date(starttime)<={$starttime}
            and startby in (%s)""" % (",".join(map(str,qa_list))) )
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_usage_statbypeople_acc_day_rd(self,param):
        try:
            qa_list,rd_list=self.query_all_QA_RD()
            s=DynSql("""select count(distinct startby) as usage_per_day from tbl_test_management where date(starttime)<={$starttime}
            and startby in (%s)""" % (",".join(map(str,rd_list))) )
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_usage_statbypeople_acc_day(self,param):
        try:
            s=DynSql("""select count(distinct startby) as usage_per_day from tbl_test_management where date(starttime)<={$starttime}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_usage_statbycnt_acc_day(self,param):
        try:
            s=DynSql("""select pjt_id,count(*) as usage_per_day from tbl_test_management where pjt_id={$pjt_id} and date(starttime)<={$starttime}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_stat_test_result(self,param):
        try:
            s=DynSql("""select count(*) from tbl_test_management where 1=1 {and status=$status} group by pjt_id order by pjt_id""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_honor_list(self,param):
        try:
            s=DynSql("""select startby,count(*) as cnt from tbl_test_management group by startby order by cnt desc limit 3""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_test_management_monitor(self):
        try:
            sql="""SELECT * from tbl_test_management where status=0 ORDER BY id ASC LIMIT 0,1"""
            cnt=self.cursor.execute(sql)
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_total_test_management(self,param):
        try:
            s=DynSql("""select * from tbl_test_management where 1=1 { and pjt_id=$pjt_id}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            cnt=self.cursor.rowcount
            return cnt
        except Exception as e:
            logging.error(str(e))
    def history_query_test_management(self,param):
        try:
            s=DynSql("""select id,task_id,pjt_id,testtype,starttime,endtime,status,startby from tbl_test_management where 1=1 { and id=$id}
            { and task_id=$task_id} { and pjt_id=$pjt_id} { and testtype=$testtype} { and starttime>=$stime} { and starttime<=$etime}
            { and status=$status} { and startby=$startby}
            ORDER BY id DESC {limit {$offset,} $row_cnt}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return cnt,ret
        except Exception as e:
            logging.error(str(e))
    def add_test_management(self,param):
        try:
            sql="""insert into tbl_test_management(id,task_id,pjt_id,testtype,starttime,status,startby)
            values(NULL,%s,%s,%s,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    def update_test_management_endtime(self,param):
        try:
            sql="""update tbl_test_management set endtime=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def update_test_management_status(self,param):
        try:
            sql="""update tbl_test_management set status=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def update_test_management_log(self,param):
        try:
            sql="""update tbl_test_management set log=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def query_project_management(self,param):
        try:
            s=DynSql("""select * from tbl_project_management where 1=1 { and id=$id}
            { and name=$name} { and info=$info} { and status=$status} { and parent=$parent} { and position=$position} { and showid=$showid}
            ORDER BY id ASC {limit {$offset,} $row_cnt}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def query_show_project_management(self):
	    try:
	        s="""select * from tbl_project_management where showid>0
            ORDER BY showid ASC """
	        cnt=self.cursor.execute(s)
	        ret=self.cursor.fetchall()
	        return ret
	    except Exception as e:
	        logging.error(str(e))
    def add_test_script(self,param):
        try:
            sql="""insert into tbl_script(id,task_id,caseid,casename,starttime)
            values(NULL,%s,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    def update_test_script_endtime(self,param):
        try:
            sql="""update tbl_script set endtime=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def update_test_script_result(self,param):
        try:
            sql="""update tbl_script set result=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def update_test_script_testlog(self,param):
        try:
            sql="""update tbl_script set testlog=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def query_test_script(self,param):
        try:
            s=DynSql("""select * from tbl_script where 1=1 { and id=$id}
            { and task_id=$task_id} { and caseid=$caseid} { and casename=$casename} { and starttime=$starttime}
            { and endtime=$endtime} { and result=$result} { and testlog=$testlog}
            ORDER BY id ASC {limit {$offset,} $row_cnt}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
    def add_benchmark_test(self,param):
        try:
            sql="""insert into tbl_benchmark(id,task_id,casename,starttime)
            values(NULL,%s,%s,%s)"""
            n=self.cursor.execute(sql,param)
            last_id=int(self.cursor.lastrowid)
            self.conn.commit()
            return n,last_id
        except Exception as e:
            logging.error(str(e))
            return 0,0
    def update_benchmark_test(self,param):
        try:
            sql="""update tbl_benchmark set endtime=%s,totalrequest=%s,totalresponse=%s,totalerror=%s,qps_curve=%s where id=%s"""
            n=self.cursor.execute(sql,param)
            self.conn.commit()
            return n
        except Exception as e:
            logging.error(str(e))
    def query_benchmark_test(self,param):
        try:
            s=DynSql("""select * from tbl_benchmark where 1=1 { and id=$id}
            { and task_id=$task_id} { and casename=$casename} { and starttime=$starttime} { and endtime=$endtime}
            { and totalrequest=$totalrequest} { and totalresponse=$totalresponse} { and totalerror=$totalerror}
            ORDER BY id ASC {limit {$offset,} $row_cnt}""")
            sql=s(param)
            cnt=self.cursor.execute(sql[0],sql[1])
            ret=self.cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(str(e))
if __name__ == "__main__":
    mysql=mysqlLib()

    '''n=mysql.add_pjt(param=("UserPreference",u"用户偏好",0))
    print(u"插入数据:"+str(n))

    ret=mysql.query_pjt()
    print(u"查询数据:"+str(len(ret)))
    print ret
    for record in ret:
        for field in record:
            print field

    n=mysql.updata_pjt(param=("UserPreference_NEW",u"用户偏好_NEW",1,"UserPreference"))
    print(u"更新数据:"+str(n))

    n=mysql.del_pjt(param=(u"UserPreference",))
    print(u"删除数据:"+str(n))'''

    '''param=(2,'task_userpreference','1.0.1.1',u'标记一下',0,1,
    'ftp://getprod:getprod@product.scm.baidu.com:/data/prod-64/app/search/lbs-da/upps/openservice/openservice_1-0-11-4_PD_BL',0)
    n,last_id=mysql.add_task(param)
    print(u"插入数据:"+str(n)+","+str(last_id))

    ret=mysql.query_task((0,10))
    print(u"查询数据:"+str(len(ret)))
    print ret
    for record in ret:
        for field in record:
            print field

    now=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    param=(2,'task_userpreference_new','1.0.1.1',u'标记一下',0,1,
    'ftp://getprod:getprod@product.scm.baidu.com:/data/prod-64/app/search/lbs-da/upps/openservice/openservice_1-0-11-4_PD_BL',
    now,now,0,'task_userpreference')
    n=mysql.update_task(param)
    print(u"更新数据:"+str(n))

    ret=mysql.query_task((0,10))
    print(u"查询数据:"+str(len(ret)))
    print ret
    for record in ret:
        for field in record:
            print field

    n=mysql.del_task(param=(u"task_userpreference",))
    print(u"删除数据:"+str(n))'''

    '''ret=pjt_list=mysql.query_pjt({"offset":0,"row_cnt":10})
    print ret'''
    qa,rd=mysql.query_all_QA_RD()
    print qa
    print rd

    mysql.close()

