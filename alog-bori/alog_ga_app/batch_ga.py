import sys
import datetime
import os
import csv
import time
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, Filter, FilterExpression
from google.protobuf.json_format import MessageToDict
import pandas as pd
import cfg

ppath = "../ga" 

PROPERTY_ID = cfg.PROPERTY_ID

KEY_PATH = "../../cskwak-152504-ff6974c3f80d.json"  # 키 파일명

def fn_ga_todb_exec(pymd) :    
    cfg.fnprt ("fn_ga_todb_exec START " + pymd)
    strSQL = "delete from alog_bori.tga_target where ymd = '" +pymd+ "' "
    cfg.fnSQLexe (strSQL)
  
    strSQL = " /* fn_ga_todb_exec 1 */ insert into alog_bori.tga_target ( ymd,device,depth1,depth2,pv,pagename) \
        with tbl1 as (select split_part(pagescreen, '?', 1) url,pv,pagename from alog_bori.tga_org where device ='a' and ymd ='" +pymd+ "') \
        ,tbl as (select  url depth1,null  depth2 ,pv,array_length(string_to_array(url,'/'),1) ,pagename	  \
        from tbl1  where array_length(string_to_array(url,'/'),1) <= 1 \
        union all  \
        select  (string_to_array(url,'/'))[2] ,case when (string_to_array(url,'/'))[3] is null then null else (string_to_array(url,'/'))[3] end ,pv, array_length(string_to_array(url,'/'),1) ,pagename \
        from tbl1  where array_length(string_to_array(url,'/'),1) > 1 \
        ) select '" +pymd+ "' ymd,'a' device,depth1,depth2,sum(pv) pv ,max(pagename) from tbl group by depth1,depth2" 
    cfg.fnSQLexe (strSQL)

    strSQL =" /* fn_ga_todb_exec 2 */ insert into alog_bori.tga_target ( ymd,device,depth1,depth2,pv,pagename) \
        with tbl as ( select split_part(pagescreen, '?', 1) url,pv,pagename from alog_bori.tga_org where device ='p' and ymd ='" +pymd+ "' )  \
        select '" +pymd+ "' ymd,'p',(string_to_array(url,'/'))[2] ,(string_to_array(url,'/'))[3],sum(pv) pv ,max(pagename) from tbl \
        group by (string_to_array(url,'/'))[2] ,(string_to_array(url,'/'))[3]" 
    cfg.fnSQLexe (strSQL)

    strSQL ="update alog_bori.tga_target set depth1 ='home' where depth1 in ('ListFragment','Boribori_iOS.HomeBodyViewController') and ymd = '" +pymd+ "'"
    cfg.fnSQLexe (strSQL)
     
    strSQL ="update alog_bori.tga_target set depth1 ='home' ,depth2 ='best' where depth1 in ('BestFragment','Boribori_iOS.BestViewController') and ymd = '" +pymd+ "' "
    cfg.fnSQLexe (strSQL)
     
    strSQL ="update alog_bori.tga_target set depth1 ='home' ,depth2 ='event' where depth1 in ('LnbEventFragment','Boribori_iOS.EventViewController')  and ymd = '" +pymd+ "'     "
    cfg.fnSQLexe (strSQL)
     
    strSQL ="update alog_bori.tga_target set depth1 ='home' ,depth2 ='hotdeal' where depth1 in ('Boribori_iOS.HotDealViewController')  and ymd = '" +pymd+ "'     "
    cfg.fnSQLexe (strSQL)
     
    strSQL ="update alog_bori.tga_target set depth2 ='' where depth1 ='search' and depth2 ='menu' and ymd = '" +pymd+ "' "
    cfg.fnSQLexe (strSQL)

    strSQL = "insert into tga_url (url) vaules('http://127.0.0.1:" +cfg.webport +"/?pdevice=a&pday=" +pymd+"')"
    cfg.fnSQLexe (strSQL)

    strSQL = "insert into tga_url (url) vaules('http://127.0.0.1:" +cfg.webport +"/?pdevice=&pday=" +pymd+"')"
    cfg.fnSQLexe (strSQL)

    cfg.fnprt ("fn_ga_todb_exec END " + pymd)



def fn_ga_download_activeUsers_firstTimePurchasers(PROPERTY_ID,KEY_PATH,pymd):
    
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    client = BetaAnalyticsDataClient(credentials=credentials)

    #https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema?hl=ko
    page_size = 100000
    offset = 0

    while True:
        cfg.fnprt ('fn_ga_download_activeUsers_firstTimePurchasers Start ' +pymd + " " + str(offset))
        request = RunReportRequest(
            property=f"properties/{PROPERTY_ID}",
            dimensions=[{"name": "deviceCategory"}],            # 페이지   platform:web,iOS   deviceCategory:mobile,desktop,tablet  {"name": "pagePathPlusQueryString"}]
            metrics=[{"name": "activeUsers"},{"name": "firstTimePurchasers"}],        # PV(화면 페이지뷰)
            date_ranges=[{"start_date": pymd, "end_date": pymd}],               
            limit=page_size,
            offset=offset
        )
        response = client.run_report(request)        
        if not response.rows:
            cfg.fnprt ('fn_ga_download_activeUsers_firstTimePurchasers END ' +pymd + " " + str(offset))
            break
        
        rows = []
        for row in response.rows:
            record = {}
            for header, value in zip(response.dimension_headers, row.dimension_values):
                record[header.name] = value.value
            for header, value in zip(response.metric_headers, row.metric_values):
                record[header.name] = value.value
            rows.append(record)

        df = pd.DataFrame(rows)

        # CSV 저장        
        filename = ppath +"/activeUsers/"+ pymd +"_" + str(PROPERTY_ID) +"_activeUsers_" +str(offset)+".csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")

        offset += page_size  # 다음 페이지        
        print(filename)


def fn_ga_todb_activeUsers(pymd) :

    cfg.fnprt("START fn_ga_todb_activeUsers " +pymd )
    strSQL = "delete from alog_bori.tga_activeUser where ymd = '" +pymd+ "' "
    cfg.fnSQLexe (strSQL)
    folder_exec = ppath+"/activeUsers"
    files = [f for f in os.listdir(folder_exec) if os.path.isfile(os.path.join(folder_exec, f))]
    
    for pfilename in files:    
        if pymd in pfilename :
            pfilename = folder_exec +"/"+pfilename
            print(pfilename)

            with open(pfilename, "r", encoding="utf-8") as fileread:    
                readdata = csv.reader(fileread)
                next(readdata)
                strSQL = "insert into alog_bori.tga_activeUser (ymd,device,activeUsers,firstTimePurchasers) values "
                rowcnt = 0 
                Exec ="N"
                for pvalue in readdata:                                    
                    if pvalue[0] =='mobile':
                        strSQL = strSQL + "('" +pymd+ "','a','"+pvalue[1]+"','"+pvalue[2] + "'),"
                    elif pvalue[0] =='tablet':                        
                        strSQL = strSQL + "('" +pymd+ "','a','"+pvalue[1]+"','"+pvalue[2] + "'),"
                    elif pvalue[0] =='desktop':                        
                        strSQL = strSQL + "('" +pymd+ "','p','"+pvalue[1]+"','"+pvalue[2] + "'),"
                    else :
                        strSQL = strSQL + "('" +pymd+ "','e','"+pvalue[1]+"','"+pvalue[2] + "'),"
                    Exec ="Y"
                    if rowcnt % 100 == 0 :
                        cfg.fnSQLexe (strSQL[0:-1])
                        strSQL = "insert into alog_bori.tga_activeUser (ymd,device,activeUsers,firstTimePurchasers) values "
                        Exec ="N"
                        print(rowcnt)
                    rowcnt = rowcnt + 1
                
                if Exec == "Y":
                    cfg.fnSQLexe (strSQL[0:-1]) 
                #print(rowcnt)                
    cfg.fnprt("END fn_ga_todb_activeUsers " +pymd )



def fn_ga_download_pageview(PROPERTY_ID,KEY_PATH,pymd,pfilter):
    
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    client = BetaAnalyticsDataClient(credentials=credentials)

    #https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema?hl=ko
    page_size = 100000
    offset = 0

    while True:
        cfg.fnprt ('fn_ga_download Start ' +pymd + " " + pfilter + " " + str(offset))
        request = RunReportRequest(
            property=f"properties/{PROPERTY_ID}",
            dimensions=[{"name": "deviceCategory"},{"name": "unifiedPagePathScreen"},{"name": "unifiedScreenName"}],            # 페이지   platform:web,iOS   deviceCategory:mobile,desktop,tablet  {"name": "pagePathPlusQueryString"}]
            metrics=[{"name": "screenPageViews"}],        # PV(화면 페이지뷰)
            date_ranges=[{"start_date": pymd, "end_date": pymd}],    
            dimension_filter=FilterExpression(
                filter=Filter(
                    field_name="deviceCategory",
                    string_filter=Filter.StringFilter(value= pfilter )  # ← 여기서 모바일만 필터
                )
            ),
            limit=page_size,
            offset=offset
        )

        response = client.run_report(request)
        if not response.rows:
            cfg.fnprt ('fn_ga_download END ' +pymd + " " + pfilter + " " + str(offset))
            break

        rows = []
        for row in response.rows:
            record = {}
            for header, value in zip(response.dimension_headers, row.dimension_values):
                record[header.name] = value.value
            for header, value in zip(response.metric_headers, row.metric_values):
                record[header.name] = value.value
            rows.append(record)

        df = pd.DataFrame(rows)

        # CSV 저장        
        filename = ppath +"/pageview/"+ pymd +"_" + str(PROPERTY_ID) +"_pageview_" + pfilter  + "_" +str(offset)+".csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        offset += page_size  # 다음 페이지   

def fn_ga_todb_pageview(pymd) :
    cfg.fnprt("START fn_ga_todb_pageview " +pymd )
    strSQL = "delete from alog_bori.tga_org where ymd = '" +pymd+ "' "
    cfg.fnSQLexe (strSQL)
    folder_exec = ppath+"/pageview"
    files = [f for f in os.listdir(folder_exec) if os.path.isfile(os.path.join(folder_exec, f))]
    
    for pfilename in files:    
        if pymd in pfilename :
            pfilename = folder_exec +"/"+pfilename
            print(pfilename)

            with open(pfilename, "r", encoding="utf-8") as fileread:    
                readdata = csv.reader(fileread)
                next(readdata)
                strSQL = "insert into alog_bori.tga_org (ymd,device,pagescreen,pagename,pv) values "
                pExec ="N"
                rowcnt = 0 
                for pvalue in readdata:                                    
                    if pvalue[0] =='mobile':
                        strSQL = strSQL + "('" +pymd+ "','a','"+cfg.fnsqlvalue(pvalue[1][0:150])+"','"+cfg.fnsqlvalue(pvalue[2][0:150])+"','"+pvalue[3] + "'),"
                    elif pvalue[0] =='tablet':                        
                        strSQL = strSQL + "('" +pymd+ "','a','"+cfg.fnsqlvalue(pvalue[1][0:150])+"','"+cfg.fnsqlvalue(pvalue[2][0:150])+"','"+pvalue[3] + "'),"
                    elif pvalue[0] =='desktop':                        
                        strSQL = strSQL + "('" +pymd+ "','p','"+cfg.fnsqlvalue(pvalue[1][0:150])+"','"+cfg.fnsqlvalue(pvalue[2][0:150])+"','"+pvalue[3] + "'),"
                    else :
                        strSQL = strSQL + "('" +pymd+ "','e','"+cfg.fnsqlvalue(pvalue[1][0:150])+"','"+cfg.fnsqlvalue(pvalue[2][0:150])+"','"+pvalue[3] + "'),"
                    pExec ="Y"
                    if rowcnt % 100 == 0 :
                        #print("Ins " + str(rowcnt))
                        cfg.fnSQLexe (strSQL[0:-1])
                        strSQL = "insert into alog_bori.tga_org (ymd,device,pagescreen,pagename,pv) values "
                        pExec ="N"
                        
                    rowcnt = rowcnt + 1
                
                #print("End " + str(rowcnt))
                if pExec == "Y":
                    cfg.fnSQLexe (strSQL[0:-1]) 
                
    cfg.fnprt("END fn_ga_todb_pageview " +pymd )

                    
#pstartymd = "2025-09-07"

#fn_ga_download_activeUsers_firstTimePurchasers(PROPERTY_ID,KEY_PATH,pstartymd)
#fn_ga_todb_activeUsers(pstartymd)
#sys.exit()

strSQL = " select ymd from tga_target order by ymd desc limit 1 "
pstartymd  = str(cfg.fnSQLselect1(strSQL))
pstartymd = (datetime.datetime.strptime(pstartymd, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d") 

pstep ="Y"


for padd in range(0, 3):
    pymd = (datetime.datetime.strptime(pstartymd, "%Y-%m-%d") + datetime.timedelta(days=padd)).strftime("%Y-%m-%d")
    print(pymd)
    

    if (datetime.datetime.strptime(pymd, "%Y-%m-%d").date()) >= ( datetime.datetime.today().date() ) :
        print("END " +pymd)
        sys.exit()

    if pstep == "Y" :
        fn_ga_download_activeUsers_firstTimePurchasers(PROPERTY_ID,KEY_PATH,pymd)
        fn_ga_todb_activeUsers(pymd)

    if pstep == "Y" :
        fn_ga_download_pageview(PROPERTY_ID,KEY_PATH,pymd,"mobile")
        fn_ga_download_pageview(PROPERTY_ID,KEY_PATH,pymd,"desktop")
        fn_ga_download_pageview(PROPERTY_ID,KEY_PATH,pymd,"tablet")
        fn_ga_todb_pageview(pymd)
        fn_ga_todb_exec(pymd) 
    
    #sys.exit()

  

strSQL = " \
CREATE TABLE alog_bori.tga_org ( \
	ymd date NOT NULL, \
	device varchar(20) NOT NULL, \
	pagescreen varchar(200) NULL, \
	pv int8 NOT NULL, \
	pagename varchar(200) NULL \
);"

strSQL = " \
CREATE TABLE alog_bori.tga_target ( \
	ymd date NULL, \
	device varchar(1) NULL, \
	depth1 varchar(200) NULL, \
	depth2 varchar(200) NULL, \
	pv int8 NULL, \
	pagename varchar(200) NULL \
); "

strSQL = " CREATE INDEX tga_target_ymd_idx ON alog_bori.tga_target USING btree (ymd, device, depth1);"

strSQL =" \
CREATE TABLE alog_bori.tga_activeuser ( \
	ymd date NULL, \
	device varchar(1) NULL, \
	activeusers int8 NULL, \
	firsttimepurchasers int8 NULL \
); "

strSQL = "CREATE INDEX tga_activeuser_ymd_idx ON alog_bori.tga_activeuser USING btree (ymd, device);"

'''
pip install psycopg2
'''
