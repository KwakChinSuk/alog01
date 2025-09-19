import sys, datetime, os, string, random, json, psycopg2
from decimal import Decimal

KEY_PATH = "../../cskwak-152504-ff6974c3f80d.json"  # 키 파일명
ppath = "../ga" 

def dbconnp():
    return psycopg2.connect("host=db01.c1i64gi0k41z.ap-northeast-2.rds.amazonaws.com dbname=postgres user=admin01 password=kjs202512 port=5432")


dbschema = "alog_bori"         # DB   - (X) _ (O)
mainpath = "../alog-bori/json" # AWS  - (O) _ (X)
serviceurl = "https://alog-bori.jskwak.pe.kr"

PROPERTY_ID = "349789872"   #  www.boribori.co.kr
#PROPERTY_ID = "394311308"  #  halftest
#PROPERTY_ID = "330117769"  #  www.jskwak.pe.kr


dbcon = dbconnp()
curp = dbcon.cursor()

class DataUrlPara:    
    ymd: str = None    
    ymd_1: str = None   
    ymd_7: str = None   
    ymd_14: str = None   
    ymd: str = None   
    device: str = None  
    jsname: str = None  

def fnsqlvalue(pvalue):
    pvalue = pvalue.replace("'","")
    return pvalue

def fncreatecharid():
    return ''.join(random.sample(string.ascii_uppercase + string.digits, 6))

def df_line_color(no):
    dfcolors =  [
        '#008FFB', # 파랑
        '#00E396', # 초록
        '#FEB019', # 주황
        # '#FF4560', # 빨강
        '#775DD0', # 보라
        '#546E7A', # 회청색
        '#26A69A', # 청록
        '#D10CE8', # 자홍색
        '#8D6E63', # 갈색
        '#F15BB5',  # 갈색
        '#ffb74d',  # 갈색
        '#F15BB5',  # 갈색
        '#F15BB5' # 분홍
    ]
    return dfcolors[no]
def df_line_color_red(no):
    dfcolors =  [
        '#FF4560', # 빨강
        '#f26b6b',
        '#f79494',
        '#ffb3a7',
        '#ffbb80'
    ]
    return dfcolors[no]
def fnprt(pstr):
    print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ " " + pstr)

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    elif isinstance(obj,datetime.date) :
        return obj.strftime("%Y-%m-%d")
    raise TypeError
def format_number(n):
    if n  is None :
        return ""
    if n == int(n):
        return f"{int(n):,}"
    else:
        return f"{n:,.2f}"

def fn_per (pvalue1 , pvalue2):
    if ( (pvalue1 is None) or ( pvalue2 is None) ) :        
        return 0
    if ( pvalue2 == 0)  :
        return 0
    if pvalue1 > pvalue2 :
        return ( (pvalue1 / pvalue2) -1) *100
    else:
        return (-1 * (1- (pvalue1 / pvalue2))) * 100

def fnSQLexe (strSQL) :
    try:
        #print(strSQL)
        #print("exeSQLp")
        tconnp = dbconnp()
        curp = tconnp.cursor()
        curp.execute("SET TIME ZONE 'Asia/Seoul';")
        curp.execute("SET search_path TO " +dbschema+ ";")        
        curp.execute(strSQL)
        tconnp.commit()
        return curp
    except Exception as e:
        print(e)
        print("ERROR SQL 2")
        print(strSQL)
        sys.exit()

def fnSQLselect (strSQL) :        
    try:
        tconnp = dbconnp()
        curp = tconnp.cursor()
        curp.execute("SET TIME ZONE 'Asia/Seoul';")
        curp.execute("SET search_path TO " +dbschema+ ";")        
        curp.execute(strSQL)
        tconnp.commit()
        result =  curp.fetchall()
        if result is None:
            return None
        else:
            if len(result) ==0 :
                return None
            else:
                return result

    except Exception as e:
        print(e)
        print(strSQL)
        sys.exit()

def fnSQLselect1 (strSQL) :
    try:        
        tconnp = dbconnp()
        curp = tconnp.cursor()
        curp.execute("SET TIME ZONE 'Asia/Seoul';")
        curp.execute("SET search_path TO " +dbschema+ ";")        
        curp.execute(strSQL)
        tconnp.commit()
        result = curp.fetchone()
        if result is None:
            return None
        else:
            return result[0]
    except Exception as e:
        print(e)
        print(strSQL)
        sys.exit()



def fnSQLselectC (strSQL,UrlPara) :        
    ppath = mainpath+ "/"+UrlPara.ymd
    pfilename = "/" +UrlPara.device+"_"+ UrlPara.jsname+".json"

    if (os.path.isfile(ppath+pfilename) ):

            f = open(ppath+pfilename, 'r')
            fileread_data = f.readline()

            if ( len(fileread_data) == 0 ):
                f.close()
                os.remove(ppath+pfilename)
                result = []
            else :
                result = json.loads(fileread_data)
            
    else:
        #print("fnSQLselectC EXEC " +ppath + " " +pfilename)
        #print(strSQL)
        result = fnSQLselect(strSQL)        
        if not (result is None) :
            if len(result) >= 1 :
                print(ppath + pfilename)
                if not os.path.exists(ppath):
                    os.mkdir(ppath)
                f = open(ppath+pfilename, 'w+')
                f.write(json.dumps(result,default=decimal_default))
                f.close()
                #print("Write file " + ppath+pfilename)
            else:
                print("ERROR Write file 1" + ppath+pfilename)
                print("ERROR Write file 1 len:" + str(len(result)))
                print(result)
        else:
            print("ERROR Write file EMPTY  2" + pfilename)
            print(result)

    return result


def fn_createtable () :  
    strSQL = " \
    CREATE TABLE tga_org ( \
        ymd date NOT NULL, \
        device varchar(20) NOT NULL, \
        pagescreen varchar(200) NULL, \
        pv int8 NOT NULL, \
        pagename varchar(200) NULL \
    );"

    fnSQLexe(strSQL)

    strSQL = " \
    CREATE TABLE tga_target ( \
        ymd date NULL, \
        device varchar(1) NULL, \
        depth1 varchar(200) NULL, \
        depth2 varchar(200) NULL, \
        pv int8 NULL, \
        pagename varchar(200) NULL \
    ); "
    fnSQLexe(strSQL)

    strSQL = " CREATE INDEX tga_target_ymd_idx ON tga_target USING btree (ymd, device, depth1);"
    fnSQLexe(strSQL)

    strSQL =" \
    CREATE TABLE tga_activeuser ( \
        ymd date NULL, \
        device varchar(1) NULL, \
        activeusers int8 NULL, \
        firsttimepurchasers int8 NULL \
    ); "
    fnSQLexe(strSQL)

    strSQL = "CREATE INDEX tga_activeuser_ymd_idx ON tga_activeuser USING btree (ymd, device);"
    fnSQLexe(strSQL)

