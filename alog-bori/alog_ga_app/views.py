from django.shortcuts import render
from alog_ga_app import cfg
import datetime
import time
from decimal import Decimal


def chartarray_to_html(title,arraylist,UrlPara):

    divid = "home_chart_" +title+ str(int(time.time() * 1000))
    divid = divid.replace("/","")
    divid = divid.replace("(", "")
    divid = divid.replace(")", "")
    divid = divid.replace("<", "")
    divid = divid.replace(">", "")
    divid = divid.replace(" ", "")
    divid = divid.replace(",", "")
    divid = divid.replace(".", "")
    divid = divid.replace("=", "")
    divid = divid.replace("'", "")
    divid = divid.replace(";", "")
    divid = divid.replace(":", "")

    strHtml = "<div class='col-md-12 col-xl-12'><div class='d-flex align-items-flex-start  mb-0'>"

    if title =="구좌_HOME" :
        strHtml_Home_screen ="<select onchange='changeselect(this.value);' name='fservice_no' id='fservice_no' style = 'width:100px;font-size:12px; color:blue;font-weight: bold;padding: 3px 3px;'>"
        strHtml_Home_screen = strHtml_Home_screen + "<option value=''>Screenshot</option>"
        strSQL = "select filename,to_char(ymd,'YYYY-MM-DD') ymd from ( \
        SELECT  filename ,max(ymd) ymd    FROM crm.thome where ymd >= CURRENT_DATE - INTERVAL '0 days' and filename is not null  group by filename \
        union \
        SELECT max(filename) ,max(ymd) ymd   FROM crm.thome where ymd > CURRENT_DATE - INTERVAL '10 days' and filename is not null group by ymd \
        ) tbl order by filename desc "
        #results = cfg.exeSQLApC(strSQL, 'chartarray_to_html1', "account_home", UrlPara)
        results = cfg.exeSQLAp(strSQL)
        for row in results:
            strHtml_Home_screen = strHtml_Home_screen+ "<option value="+ row[1]+","+row[0]+ ">"+row[0]+ "</option>"
        strHtml_Home_screen = strHtml_Home_screen+ "</select>"
        strHtml = strHtml + "<button style='min-width: 120px;border: 0px'><h5 class='mb-0'>"+title+"<br>"+strHtml_Home_screen+"</h5></button>"
    elif title =="메뉴비중" :
        strHtml = strHtml + "<button style='min-width: 120px;border: 0px'><h5 class='mb-0'>메뉴 비중<br><font size='1'>(메뉴PV/전체PV)</font></h5></button>"
    elif title =="자체" :
        strHtml = strHtml + "<button style='min-width: 120px;border: 0px'><h5 class='mb-0'>유입채널<br><font size='1'>(자체,비중)</font></h5></button>"
    elif title =="제휴" :
        strHtml = strHtml + "<button style='min-width: 120px;border: 0px'><h5 class='mb-0'>유입채널<br><font size='1'>(제휴,비중)</font></h5></button>"
    else:
        strHtml = strHtml + "<button style='min-width: 120px;border: 0px'><h5 class='mb-0'>" +title+ "</h5></button>"

    strHtml = strHtml + "&nbsp;&nbsp;&nbsp;<ul class='nav nav-pills'  >"

    idno = 0

    for row in arraylist:
        strHtml = strHtml + "<li class='nav-item' ><button data-bs-target='#" + divid+str(idno) + "' class='nav-link ' aria-selected='false' type='button'  data-bs-toggle='pill' "
        strHtml = strHtml + " style='min-width: 200px; padding: 1px 3px; border: 2px solid " + row[0] + "</button></li> &nbsp; "
        idno = idno + 1

    strHtml = strHtml + "<li class='nav-item'><button data-bs-toggle='pill' type='button' style='border: 0px solid; padding: 1px 3px;'><svg viewBox='0 0 24 24' width='24' height='24' fill='none' stroke='currentColor' stroke-width='2'><line x1='18' y1='6' x2='6' y2='18'/><line x1='6' y1='6' x2='18' y2='18'/></svg></button></li> &nbsp; "

    strHtml = strHtml + "</ul></div><div class='card-body'><div class='tab-content'>"
    idno = 0
    for row in arraylist:
        strHtml = strHtml + "<div class='tab-pane' id='" + divid+str(idno) + "' aria-labelledby='" + divid+str(idno) + "-tab' style='border: 1px solid #aaaaaa;'  >"
        strHtml = strHtml + row[1]
        strHtml = strHtml + "</div>"
        idno = idno + 1

    strHtml = strHtml + ""
    strHtml = strHtml + "</div><br></div></div>"
    return  strHtml




def fn_bnttitle(ptitle,n,UrlPara,pGArrList, pGArrValue):

    pValuetoday  = pdataarr_out(n, UrlPara.ymd, pGArrList, pGArrValue)

    pValueday_1  = pdataarr_out(n, UrlPara.ymd_1, pGArrList, pGArrValue)
    pValueday_7  = pdataarr_out(n, UrlPara.ymd_7, pGArrList, pGArrValue)
    pValueday_14 = pdataarr_out(n, UrlPara.ymd_14, pGArrList, pGArrValue)

    pvalue1 = cfg.fn_per(pValuetoday, pValueday_1)
    pvalue7 = cfg.fn_per(pValuetoday, pValueday_7)
    pvalue14 = cfg.fn_per(pValuetoday, pValueday_14)

    pValuePageView = pdataarr_out("ALL~~ALL", UrlPara.ymd, pGArrList, pGArrValue)

    stradd1 =""
    strunit =""

    strBtnColor = "#f2f2f2;' >"
    
    if "조회수" == ptitle :
        strTitle = "<div class='parent'>" + ptitle + " <div class='parent-right'>사용자가 조회한 앱 화면 또는 웹페이지의 수입니다.<br>한 페이지 또는 한 화면을 반복해서 조회한 횟수도 집계에 포함됩니다.<br>(screen_view 이벤트 수 + page_view 이벤트 수)</div></div>"
        strunit = "pv"       
    elif "활성 사용자" == ptitle :
        strTitle = "<div class='parent'>" + ptitle + " <div class='parent-right'>내 사이트 또는 앱을 방문한 개별 사용자의 수입니다.<br>(activeUsers)</div></div>"
        strunit = "명"               
    elif "최초 구매자 수" == ptitle :
        strTitle = "<div class='parent'>" + ptitle + " <div class='parent-right'>첫 구매 이벤트를 완료한 사용자의 수입니다.<br>(GA 기준,firstTime Purchasers)</div></div>"
        strunit = "명"                       
    elif "~~ALL" in n :
        strTitle = "<div class='parent'>" + ptitle + " <div class='parent-right'>URL (샘플) : /" +n.replace("~~ALL","")+ "/~~~ <br>건수 : 2 depth 건수 (Unique)</div></div>"
        strunit = "%"
    elif "~~" in n :
        pvalue = ptitle.split('~sub~')
        purl = n.split('~~')
        
        result = pvalue[1]
        result = "".join("*" if i % 2 == 0 else ch for i, ch in enumerate(str(result)))

        strTitle = "<div class='parent'>" + pvalue[0] + "<div class='parent-right'>URL : /"+ purl[0]+"/"+ purl[1]+"<br><p style='font-size: 0.8em;'>Title : " +result+ "</P></div></div>"        
        strunit = "pv"                          
    else:
        return strBtnColor + " NoData fn_bnttitle " + n


    strHTML ="<table width='100%' >"
    strHTML = strHTML + "<Tr >"
    strHTML = strHTML + "<td>" +strTitle+ "</td>"
    strHTML = strHTML + "<td width='50' rowspan=2>"
    strScript =""

    if pValueday_1 == None :
        strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;---</span></span>"
        pvalue1=0
    else :
        
        pdisvalue = cfg.format_number(pValuetoday) + "/<font color='red'>" + cfg.format_number(pValueday_1) + "</font>"

        if pvalue1 >= 100:
            pvalue1 = 99.9
    
        if pvalue1 >= 10:
            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark2' ><i class='ti ti-trending-up'></i> " + f"{pvalue1:.1f}" + "%</span></span>"
            strHTML = strHTML + "<div class='parent-black'>전일<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_1) + ")</font>대비상승<br> " + pdisvalue + "</div></div>"
        elif (pvalue1 == 0) :            
            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark' >" + f"{pvalue1:.1f}" + "%</span></span>"
            strHTML = strHTML + "<div class='parent-black'>전일<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_1) + ")</font>대비상승<br> 0/" + cfg.format_number(pValueday_1) + "</div></div>"
        elif (pvalue1 > 0 and pvalue1 < 10) :                
            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark' ><i class='ti ti-trending-up'></i> " + f"{pvalue1:.1f}" + "%</span></span>"
            strHTML = strHTML + "<div class='parent-black'>전일<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_1) + ")</font>대비상승<br> " +pdisvalue + "</div></div>"
        elif (pvalue1 >= -10 and pvalue1 < 0):            
            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-danger'><i class='ti ti-trending-down'></i> " + f"{pvalue1:.1f}" + "%</span>"
            strHTML = strHTML + "<div class='parent-read'>전일<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_1) + ")</font>대비하락<br> " + pdisvalue + "</div></div>"
        else:
            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-danger2'><i class='ti ti-trending-down'></i> " + f"{pvalue1:.1f}" + "%</span>"
            strHTML = strHTML + "<div class='parent-read'>전일<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_1) + ")</font>대비하락  <br> " + pdisvalue + "</div></div>"
    strHTML = strHTML + "<br>"

    if pValueday_7 == None :
        strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;---</span></span>"
        pvalue7 = 0
    else :

        pdisvalue = cfg.format_number(pValuetoday) + "/<font color='red'>" + cfg.format_number(pValueday_7) + "</font>"

        if pvalue7 >= 100:
            pvalue7 = 99.9

        if pvalue7 >= 10:
            # if n == "PageView" :
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark2' ><i class='ti ti-trending-up'></i><span id='span_pv2'>전주대비</span></span>"
            #     strScript = strScript + "const badge2 = document.getElementById('span_pv2'); badge2.textContent = '" + f"{pvalue7:.1f}" + "%';"
            # elif "전환율" in n:
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark2' ><i class='ti ti-trending-up'></i> " + f"{pValueday_7:.1f}" + "%</span>"
            # else:
            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark2' ><i class='ti ti-trending-up'></i> " + f"{pvalue7:.1f}" + "%</span>"
            strHTML = strHTML + "<div class='parent-black'>전주<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_7) + ")</font>대비상승<br> " + pdisvalue+ "</div></div>"

        elif ( pvalue7 == 0 ):
            # if n == "PageView":
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark' ><span id='span_pv2'>전주대비</span></span>"
            #     strScript = strScript + "const badge2 = document.getElementById('span_pv2'); badge2.textContent = '" + f"{pvalue7:.1f}" + "%';"
            # elif "전환율" in n:
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark' >" + f"{pValueday_7:.1f}" + "%</span>"
            # else:

            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark' >" + f"{pvalue7:.1f}" + "%</span>"
            strHTML = strHTML + "<div class='parent-black'>전주<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_7) + ")</font>대비상승<br>  0/<font color='red'>" + cfg.format_number(pValueday_7) + "</font></div></div>"

        elif ( pvalue7 > 0 and pvalue7 < 10):
            # if n == "PageView":
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark' ><i class='ti ti-trending-up'></i><span id='span_pv2'>전주대비</span></span>"
            #     strScript = strScript + "const badge2 = document.getElementById('span_pv2'); badge2.textContent = '" + f"{pvalue7:.1f}" + "%';"
            # elif "전환율" in n:
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark' ><i class='ti ti-trending-up'></i> " + f"{pValueday_7:.1f}" + "%</span>"
            # else:

            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark' ><i class='ti ti-trending-up'></i> " + f"{pvalue7:.1f}" + "%</span>"
            strHTML = strHTML + "<div class='parent-black'>전주<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_7) + ")</font>대비상승<br>  " + pdisvalue + "</div></div>"
        elif (pvalue7 >= -10 and pvalue7 < 0):
            # if n == "PageView":
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-danger'><i class='ti ti-trending-down'></i><span id='span_pv2'>전주대비</span></span>"
            #     strScript = strScript + "const badge2 = document.getElementById('span_pv2'); badge2.textContent = '" + f"{pvalue7:.1f}" + "%';"
            # elif "전환율" in n:
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-danger'><i class='ti ti-trending-down'></i> " + f"{pValueday_7:.1f}" + "%</span>"
            # else:
            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-danger'><i class='ti ti-trending-down'></i> " + f"{pvalue7:.1f}" + "%</span>"
            strHTML = strHTML + "<div class='parent-read'>전주<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_7) + ")</font>대비하락 <br> " + pdisvalue + "</div></div>"
        else:
            # if n == "PageView":
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-danger2'><i class='ti ti-trending-down'></i><span id='span_pv2'>전주대비</span></span>"
            #     strScript = strScript + "const badge2 = document.getElementById('span_pv2'); badge2.textContent = '" + f"{pvalue7:.1f}" + "%';"
            # elif "전환율" in n:
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-danger2'><i class='ti ti-trending-down'></i> " + f"{pValueday_7:.1f}" + "%</span>"
            # else:

            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-danger2'><i class='ti ti-trending-down'></i> " + f"{pvalue7:.1f}" + "%</span>"
            strHTML = strHTML + "<div class='parent-read'>전주<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_7) + ")</font>대비하락  <br> " + pdisvalue + "</div></div>"

    if pValueday_14 == None :
        strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;---</span></span>"
        pvalue14 = 0
    else :

        pdisvalue = cfg.format_number(pValuetoday) + "/<font color='red'>" + cfg.format_number(pValueday_14) + "</font>"

        if pvalue14 >= 100:
            pvalue14 = 99.9

        if pvalue14 >= 10:
            # if n == "PageView" :
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark2' ><i class='ti ti-trending-up'></i><span id='span_pv3'>2주전대비</span></span>"
            #     strScript = strScript + "const badge3 = document.getElementById('span_pv3'); badge3.textContent = '" + f"{pvalue14:.1f}" + "%';"
            # elif "전환율" in n:
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark2' ><i class='ti ti-trending-up'></i> " + f"{pValueday_14:.1f}" + "%</span>"
            # else:

            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark2' ><i class='ti ti-trending-up'></i> " + f"{pvalue14:.1f}" + "%</span>"
            strHTML = strHTML + "<div class='parent-black'>2주전<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_14) + ")</font>대비상승  <br> " + pdisvalue + "</div></div>"
        elif ( pvalue14 == 0 ) :
            # if n == "PageView" :
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark' ><span id='span_pv3'>2주전대비</span></span>"
            #     strScript = strScript + "const badge3 = document.getElementById('span_pv3'); badge3.textContent = '" + f"{pvalue14:.1f}" + "%';"
            # elif "전환율" in n:
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark' >" + f"{pValueday_14:.1f}" + "%</span>"
            # else:

            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark' >" + f"{pvalue14:.1f}" + "%</span>"
            strHTML = strHTML + "<div class='parent-black'>2주전<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_14) + ")</font>대비상승 <br> 0/" + cfg.format_number(pValueday_14) + "</div></div>"
        elif ( pvalue14 > 0 and pvalue14 < 10) :
            # if n == "PageView" :
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark' ><i class='ti ti-trending-up'></i><span id='span_pv3'>2주전대비</span></span>"
            #     strScript = strScript + "const badge3 = document.getElementById('span_pv3'); badge3.textContent = '" + f"{pvalue14:.1f}" + "%';"
            # elif "전환율" in n:
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark' ><i class='ti ti-trending-up'></i> " + f"{pValueday_14:.1f}" + "%</span>"
            # else:
            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-dark' ><i class='ti ti-trending-up'></i> " + f"{pvalue14:.1f}" + "%</span>"
            strHTML = strHTML + "<div class='parent-black'>2주전<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_14) + ")</font>대비상승 <br> " + pdisvalue + "</div></div>"
        elif (pvalue14 >= -10 and pvalue14 < 0):
            # if n == "PageView":
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-danger'><i class='ti ti-trending-down'></i><span id='span_pv3'>2주전대비</span></span>"
            #     strScript = strScript + "const badge3 = document.getElementById('span_pv3'); badge3.textContent = '" + f"{pvalue14:.1f}" + "%';"
            # elif "전환율" in n:
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-danger'><i class='ti ti-trending-down'></i> " + f"{pValueday_14:.1f}" + "%</span>"
            # else:

            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-danger'><i class='ti ti-trending-down'></i> " + f"{pvalue14:.1f}" + "%</span>"
            strHTML = strHTML + "<div class='parent-read'>2주전<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_14) + ")</font>대비하락  <br> " + pdisvalue + "</div></div>"

        else:
            # if n == "PageView":
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-danger2'><i class='ti ti-trending-down'></i><span id='span_pv3'>2주전대비</span></span>"
            #     strScript = strScript + "const badge3 = document.getElementById('span_pv3'); badge3.textContent = '" + f"{pvalue14:.1f}" + "%';"
            # elif "전환율" in n:
            #     strHTML = strHTML + "<div class='parent'><span class='badge bg-light-danger2'><i class='ti ti-trending-down'></i> " + f"{pValueday_14:.1f}" + "%</span>"
            # else:
            
            strHTML = strHTML + "<div class='parent'><span class='badge bg-light-danger2'><i class='ti ti-trending-down'></i> " + f"{pvalue14:.1f}" + "%</span>"
            strHTML = strHTML + "<div class='parent-read'>2주전<font style='font-size: 10px;' color='red'>("+str(UrlPara.ymd_14) + ")</font>대비하락 <br> " + pdisvalue + "</div></div>"

    strHTML = strHTML + "</td>"
    strHTML = strHTML + "</Tr>"

 
    if pValuetoday != None:
        strHTML = strHTML + "<Tr style='border-collapse: collapse;'>"
        if "ALL~~ALL" == n :
            strHTML = strHTML + "<td style='color: black; text-align: right;  border-collapse: collapse;'>" +stradd1+ "&nbsp;&nbsp;&nbsp;<div class='parent'><div class='parent-read'></div></div>"+ cfg.format_number(pValuetoday) +"<font size=1> " + strunit + "</font></td>"
        elif "~~ALL" in n:            
            strHTML = strHTML + "<td style='color: black; text-align: right;  border-collapse: collapse;'>" + stradd1 + "&nbsp;&nbsp;&nbsp;"
            strHTML = strHTML + " <div class='parent' onclick=""fn_depth1('" + UrlPara.ymd + "','" + UrlPara.device + "','"+n.replace('~~ALL','')+"');""><button style='font-size: 0.8em;padding: 1px 3px; border: 1px solid #e5e5e5; border-radius:6px;'>"
            strHTML = strHTML + " TOP 100</button></div>"
            strHTML = strHTML + " <div class='parent'><div class='parent'>" +cfg.format_number(pValuetoday/pValuePageView*100)+ "</span><div class='parent-black'>PV : " +cfg.format_number(pValuetoday)+ " / " + cfg.format_number(pValuePageView) +"</div> %</td>"
        else:
            strHTML = strHTML + "<td style='color: black; text-align: right;  border-collapse: collapse;'>" +stradd1+ "&nbsp;&nbsp;&nbsp;<div class='parent'><div class='parent-read'></div></div>"+ cfg.format_number(pValuetoday) +"<font size=1> " + strunit + "</font></td>"
        strHTML = strHTML + "</Tr>"
    strHTML = strHTML +"</table>"

    if pvalue1 >= 1:
        strBtnColor = "#c2c2c2; background-color: #FFFFFF;' >" #black
        if pvalue7 >= 1:
            strBtnColor = "#8c8c8c;background-color: #FFFFFF;' >"  # black
            if pvalue14 >= 1:
                strBtnColor = "#FFFFFF;background-color: #d4d4d4;' >"  # black

    elif pvalue1 == 0:
        strBtnColor = "#f2f2f2;background-color: #FFFFFF;'>"
    elif pvalue1 < 0:
        strBtnColor = "#ffb3a7;background-color: #FFFFFF;'>"
        if pvalue7 < 0:
            strBtnColor = "#ffb3a7;background-color: #FFFFFF;'>" 
            if pvalue14 < 0:
                strBtnColor = "#FFFFFF;background-color: #ffb3a7;'>"  # black
    else:
        strBtnColor = "#FFFFFF;background-color: #FFFFFF;' >" #red

    if n == "PageView":
        strHTML = strHTML + " <script>setTimeout(() => {" +strScript+"}, 3000);</script>"

    return strBtnColor + strHTML


def fnbutton_sub_line2w(pnames, pvalues, pday,displayvalue):

    rowno = 0
    rcolor = 0
    rcolorred = 0
    pwidth =[]
    pdasharray = []
    plinecolor = []
    strData = " var baseSeries = ["
    for row in pnames:
        pwidth.append (2)
        if '전년' in pnames[rowno]:
            strData = strData + "{name: '" + pnames[rowno] + "',type: 'line', data: [" + pvalues[rowno] + "]},"
            pdasharray.append(5)
            plinecolor.append(cfg.df_line_color_red(rcolorred))
            rcolorred = rcolorred + 1
        else:
            strData = strData + "{name: '" + pnames[rowno] + "' ,type: 'area' , data: [" + pvalues[rowno] + "]},"
            pdasharray.append(0)
            plinecolor.append(cfg.df_line_color(rcolor))
            rcolor = rcolor + 1
        rowno = rowno + 1
    rvalue_title =  strData[0:-1] + "];var series_data = baseSeries.map(function(s) {return { name: s.name, type: s.type, data: zeroToNull(s.data) };});"

    rvalue = "{chart: {height: 450,type: 'area',toolbar: {show: false}} "
    rvalue = rvalue + ",series: series_data"

    if displayvalue == "%":
        rvalue = rvalue + ",dataLabels: {enabled: true,formatter: function(val) { return (val == null ? '' : val.toFixed(1) + '%'); }}"
    else:
        rvalue = rvalue + ",dataLabels: {enabled: true,formatter: function(val) { return (val == null ? '' : Number(val).toLocaleString()); }}"

    rvalue = rvalue + ",stroke: {curve: 'smooth',width: " + str(pwidth) + " ,dashArray : " + str(pdasharray) + "  } "
    rvalue = rvalue + ",xaxis: {categories: [" + pday + "],}"

    predate = ""
    startdate = ""
    enddate = ""
    
    for row in pday.split(","):
        rowdate = datetime.datetime.strptime(row, "'%Y-%m-%d'").date()
        if predate == "" :
            predate = rowdate
        elif predate > rowdate :
            if startdate == "":
                startdate = rowdate

    #rvalue = rvalue + ",yaxis: {labels: {formatter: function (value) {return value.toLocaleString();}}} "
    rvalue = rvalue + ",yaxis: {labels: {formatter: function (value) {  return (value == null ? '' : Number(value).toLocaleString());}}} "

    if startdate != "":
        enddate = rowdate
        rvalue = rvalue + ",annotations: {xaxis: [{x: '" +str(startdate)+ "',x2: '" +str(rowdate)+ "',fillColor: '#CCCCCC', opacity: 0.2,label: {borderColor: '#FF0000',style: { color: '#fff', background: '#FF0000' },text: '전년 KPI(52주전)'}}]}"
        
    rvalue = rvalue + ",colors:  " + str(plinecolor) + " "
    rvalue = rvalue + "}"
    pvalue_option = rvalue

    chartid = cfg.fncreatecharid()
    rvalue = "<div class='tab-pane ' id='"+chartid+"'  aria-labelledby='"+chartid+"-tab'><div id='d"+chartid+"'></div>"
    rvalue = rvalue + "<script>" +rvalue_title+" var chart = new ApexCharts(document.querySelector('#d"+chartid+"')," +pvalue_option+");chart.render();</script>"
    rvalue = rvalue + "</div>"

    return rvalue



def pdataarr_in(pkind,pday,pvalue,pGArrList,pGArrValue):
    pidx = [pkind,pday]
    if isinstance(pvalue,Decimal)  :
       pvalue = int(pvalue) 
        
    if not( pidx in pGArrList):
        pGArrList.append(pidx)
        pGArrValue.append(pvalue)

    return pGArrList,pGArrValue

def pdataarr_out(pkind,pday,pGArrList,pGArrValue):
    pidx = [pkind, pday]
    if pidx in pGArrList:
        return pGArrValue[pGArrList.index(pidx)]
    
def fn_pageview(depth1,depth2,UrlPara,pGArrList,pGArrValue):
    strSQL = " with tbl_date as (select DATE(generate_series(to_date('" +UrlPara.ymd+ "','YYYY-MM-DD') - INTERVAL '14 days' ,to_date('" +UrlPara.ymd+ "','YYYY-MM-DD') + INTERVAL '6 days',  INTERVAL '1 day'))  AS ymd,date(generate_series(to_date('" +UrlPara.ymd+ "','YYYY-MM-DD') - INTERVAL '14 days'  - INTERVAL '52 weeks',  to_date('" +UrlPara.ymd+ "','YYYY-MM-DD') - INTERVAL '52 weeks' + INTERVAL '6 days',INTERVAL '1 day')) AS ymdyear) \
    ,tbl as (select  ymd,sum(pv) pv from tga_target where device ='" +UrlPara.device+ "' and ( ( ('ALL'='" +depth1+ "') or (depth1='" +depth1+ "') ) and ( ('ALL'='" +depth2+ "') or (depth2='" +depth2+ "') ) ) and ymd in (select ymd from tbl_date union all select ymdyear from tbl_date)   group by ymd) \
    select case when tbl_now.ymd is null then tbl_date.ymdyear else tbl_now.ymd end \
    ,coalesce(tbl_now.pv,0) pv \
    ,coalesce(tbl_year.pv,0) pvy  \
    from tbl_date left outer join tbl tbl_now on  tbl_date.ymd = tbl_now.ymd left outer join  tbl tbl_year on  tbl_date.ymdyear = tbl_year.ymd  \
    where ( tbl_year.pv is not null or tbl_now.pv is not null)  \
    order by tbl_date.ymd "    
    
    UrlPara.jsname = "fn_pageview_" + depth1+depth2+"_01"
    result = cfg.fnSQLselectC(strSQL,UrlPara)
    pday = ""
    pday_year = ""
    ppv = ""
    ppv_y = ""

    for row in result:        
        pday = pday + "'" + str(row[0]) + "',"        
        ppv = ppv + "" + str(row[1]) + ","
        ppv_y = ppv_y + "" + str(row[2]) + ","
        pGArrList,pGArrValue = pdataarr_in(depth1+"~~"+depth2 , str(row[0]), row[1],pGArrList,pGArrValue)        
    
    return fnbutton_sub_line2w(['Page Views','Page Views(전년)'], [ppv[0:-1],ppv_y[0:-1]], pday[0:-1], "")



def fn_activeusers(UrlPara,pGArrList,pGArrValue):
    strSQL = " with tbl_date as (select DATE(generate_series(to_date('" +UrlPara.ymd+ "','YYYY-MM-DD') - INTERVAL '14 days' ,to_date('" +UrlPara.ymd+ "','YYYY-MM-DD') + INTERVAL '6 days',  INTERVAL '1 day'))  AS ymd,date(generate_series(to_date('" +UrlPara.ymd+ "','YYYY-MM-DD') - INTERVAL '14 days'  - INTERVAL '52 weeks',  to_date('" +UrlPara.ymd+ "','YYYY-MM-DD') - INTERVAL '52 weeks' + INTERVAL '6 days',INTERVAL '1 day')) AS ymdyear) \
    ,tbl as (select  ymd,sum(activeusers) pv from tga_activeUser where device ='" +UrlPara.device+ "' and ymd in (select ymd from tbl_date union all select ymdyear from tbl_date)   group by ymd) \
    select case when tbl_now.ymd is null then tbl_date.ymdyear else tbl_now.ymd end \
    ,coalesce(tbl_now.pv,0) pv \
    ,coalesce(tbl_year.pv,0) pvy  \
    from tbl_date left outer join tbl tbl_now on  tbl_date.ymd = tbl_now.ymd left outer join  tbl tbl_year on  tbl_date.ymdyear = tbl_year.ymd  \
    where ( tbl_year.pv is not null or tbl_now.pv is not null)  \
    order by tbl_date.ymd "    
    
    UrlPara.jsname = "fn_activeusers" + "_0312"
    
    result = cfg.fnSQLselectC(strSQL,UrlPara)
    pday = ""
    pday_year = ""
    ppv = ""
    ppv_y = ""

    for row in result:        
        pday = pday + "'" + str(row[0]) + "',"        
        ppv = ppv + "" + str(row[1]) + ","
        ppv_y = ppv_y + "" + str(row[2]) + ","
        pGArrList,pGArrValue = pdataarr_in( "activeusers", str(row[0]), row[1],pGArrList,pGArrValue)

    return fnbutton_sub_line2w(['activeusers','activeusers(전년)'], [ppv[0:-1],ppv_y[0:-1]], pday[0:-1], "")

def fn_firstTimePurchasers(UrlPara,pGArrList,pGArrValue):
    strSQL = " with tbl_date as (select DATE(generate_series(to_date('" +UrlPara.ymd+ "','YYYY-MM-DD') - INTERVAL '14 days' ,to_date('" +UrlPara.ymd+ "','YYYY-MM-DD') + INTERVAL '6 days',  INTERVAL '1 day'))  AS ymd,date(generate_series(to_date('" +UrlPara.ymd+ "','YYYY-MM-DD') - INTERVAL '14 days'  - INTERVAL '52 weeks',  to_date('" +UrlPara.ymd+ "','YYYY-MM-DD') - INTERVAL '52 weeks' + INTERVAL '6 days',INTERVAL '1 day')) AS ymdyear) \
    ,tbl as (select  ymd,sum(firstTimePurchasers) pv from tga_activeUser where device ='" +UrlPara.device+ "' and ymd in (select ymd from tbl_date union all select ymdyear from tbl_date)   group by ymd) \
    select case when tbl_now.ymd is null then tbl_date.ymdyear else tbl_now.ymd end \
    ,coalesce(tbl_now.pv,0) pv \
    ,coalesce(tbl_year.pv,0) pvy  \
    from tbl_date left outer join tbl tbl_now on  tbl_date.ymd = tbl_now.ymd left outer join  tbl tbl_year on  tbl_date.ymdyear = tbl_year.ymd  \
    where ( tbl_year.pv is not null or tbl_now.pv is not null)  \
    order by tbl_date.ymd "    
    
    UrlPara.jsname = "fn_firstTimePurchasers" + "_03"
    
    result = cfg.fnSQLselectC(strSQL,UrlPara)
    pday = ""
    pday_year = ""
    ppv = ""
    ppv_y = ""

    for row in result:        
        pday = pday + "'" + str(row[0]) + "',"        
        ppv = ppv + "" + str(row[1]) + ","
        ppv_y = ppv_y + "" + str(row[2]) + ","
        pGArrList,pGArrValue = pdataarr_in( "firstTimePurchasers", str(row[0]), row[1],pGArrList,pGArrValue)
    
            
    return fnbutton_sub_line2w(['firstTimePurchasers','firstTimePurchasers(전년)'], [ppv[0:-1],ppv_y[0:-1]], pday[0:-1], "")

def fn_menu_pageview(depth1,UrlPara, pGArrList, pGArrValue):
    pmemn_tmp =[]
    
    strSQL = " /* fn_menu_pageview */ select depth2,pagename from tga_target  where depth1 = '" +depth1+ "' and ymd='" +UrlPara.ymd +"' and device ='" +UrlPara.device +"' group by depth2 ,pagename order by sum(pv) desc limit 7 "    
    UrlPara.jsname = "fn_menu_pageview_" + depth1+"_0112"
    result = cfg.fnSQLselectC(strSQL,UrlPara)
    
    for row in result:                
        if not ( (row[0] is None) or (row[0] == "") ) :
            ptmp = fn_pageview(depth1,row[0],UrlPara,pGArrList,pGArrValue)
            pmemn_tmp.append([fn_bnttitle(row[0]+"~sub~" +row[1],depth1+"~~"+row[0], UrlPara, pGArrList, pGArrValue), ptmp])

    return pmemn_tmp

def menulist(request):        
    UrlPara = cfg.DataUrlPara()
    
    UrlPara.device = request.GET.get('pdevice')
    
    if UrlPara.device is None:
        UrlPara.device= "a" 
    
    UrlPara.ymd = request.GET.get('pymd')
    pdepth1 = request.GET.get('pdepth1')
    
    
    strSQL = " select to_char((to_date('" +UrlPara.ymd +"','YYYY-MM-DD') - INTERVAL '1 days'),'MM/DD') \
union select to_char((to_date('" +UrlPara.ymd +"','YYYY-MM-DD') - INTERVAL '2 days'),'MM/DD') \
union select to_char((to_date('" +UrlPara.ymd +"','YYYY-MM-DD') - INTERVAL '3 days'),'MM/DD') \
union select to_char((to_date('" +UrlPara.ymd +"','YYYY-MM-DD') - INTERVAL '4 days'),'MM/DD') \
union select to_char((to_date('" +UrlPara.ymd +"','YYYY-MM-DD') - INTERVAL '5 days'),'MM/DD') \
union select to_char((to_date('" +UrlPara.ymd +"','YYYY-MM-DD') - INTERVAL '6 days'),'MM/DD') \
union select to_char((to_date('" +UrlPara.ymd +"','YYYY-MM-DD') - INTERVAL '7 days'),'MM/DD') \
order by 1 desc "
    result = cfg.fnSQLselect(strSQL)  

    pbodylist ="<thead><tr><th>depth2</th><th>페이지 제목 및 화면 이름 (unifiedScreenName)</th><th>" +UrlPara.ymd +"</th><th>합계(주간)</th>"

    for row in result:           
        pbodylist = pbodylist + "<th>" + row[0] + "</th>"

    pbodylist = pbodylist+"</tr></thead>"


    strSQL = "with tbl_0 as( select depth2 ,max(pagename)pagename,sum(pv) pv from tga_target   \
where ymd='" +UrlPara.ymd +"' and device ='" +UrlPara.device +"' and depth1 ='" +pdepth1+ "'  and depth2 is not null and length(depth2) > 1 group by depth2 order by sum(pv) desc limit 100) \
,tbl_1 as(select depth2 ,sum(pv) pv from tga_target   \
where ymd= (to_date('" +UrlPara.ymd +"','YYYY-MM-DD') - INTERVAL '1 days')  and device ='" +UrlPara.device +"' and depth1 ='" +pdepth1+ "' group by depth2 order by sum(pv) desc limit 100) \
,tbl_2 as(select depth2 ,sum(pv) pv from tga_target   \
where ymd= (to_date('" +UrlPara.ymd +"','YYYY-MM-DD') - INTERVAL '2 days')  and device ='" +UrlPara.device +"' and depth1 ='" +pdepth1+ "' group by depth2 order by sum(pv) desc limit 100) \
,tbl_3 as(select depth2 ,sum(pv) pv from tga_target   \
where ymd= (to_date('" +UrlPara.ymd +"','YYYY-MM-DD') - INTERVAL '3 days')  and device ='" +UrlPara.device +"' and depth1 ='" +pdepth1+ "' group by depth2 order by sum(pv) desc limit 100) \
,tbl_4 as(select depth2 ,sum(pv) pv from tga_target   \
where ymd= (to_date('" +UrlPara.ymd +"','YYYY-MM-DD') - INTERVAL '4 days')  and device ='" +UrlPara.device +"' and depth1 ='" +pdepth1+ "' group by depth2 order by sum(pv) desc limit 100) \
,tbl_5 as(select depth2 ,sum(pv) pv from tga_target   \
where ymd= (to_date('" +UrlPara.ymd +"','YYYY-MM-DD') - INTERVAL '5 days')  and device ='" +UrlPara.device +"' and depth1 ='" +pdepth1+ "' group by depth2 order by sum(pv) desc limit 100) \
,tbl_6 as(select depth2 ,sum(pv) pv from tga_target   \
where ymd= (to_date('" +UrlPara.ymd +"','YYYY-MM-DD') - INTERVAL '6 days')  and device ='" +UrlPara.device +"' and depth1 ='" +pdepth1+ "' group by depth2 order by sum(pv) desc limit 100) \
,tbl_7 as(select depth2 ,sum(pv) pv from tga_target   \
where ymd= (to_date('" +UrlPara.ymd +"','YYYY-MM-DD') - INTERVAL '7 days')  and device ='" +UrlPara.device +"' and depth1 ='" +pdepth1+ "' group by depth2 order by sum(pv) desc limit 100) \
select tbl_0.depth2,tbl_0.pagename,tbl_0.pv \
,coalesce (tbl_1.pv,0) + coalesce (tbl_2.pv,0) + coalesce (tbl_3.pv,0) + coalesce (tbl_4.pv,0) + coalesce (tbl_5.pv,0) + coalesce (tbl_6.pv,0) + coalesce (tbl_7.pv,0) pvsum \
,coalesce (tbl_1.pv,0) pv_1,coalesce (tbl_2.pv,0) pv_2,coalesce (tbl_3.pv,0) pv_3,coalesce (tbl_4.pv,0) pv_4,coalesce (tbl_5.pv,0) pv_5,coalesce (tbl_6.pv,0) pv_6,coalesce (tbl_7.pv,0) pv_7 \
From tbl_0 \
left outer join tbl_1 on tbl_0.depth2 = tbl_1.depth2 \
left outer join tbl_2 on tbl_0.depth2 = tbl_2.depth2 \
left outer join tbl_3 on tbl_0.depth2 = tbl_3.depth2 \
left outer join tbl_4 on tbl_0.depth2 = tbl_4.depth2 \
left outer join tbl_5 on tbl_0.depth2 = tbl_5.depth2 \
left outer join tbl_6 on tbl_0.depth2 = tbl_6.depth2 \
left outer join tbl_7 on tbl_0.depth2 = tbl_7.depth2 \
order by tbl_0.pv desc"
    
    result = cfg.fnSQLselect(strSQL)    


    pbodylist = pbodylist + "<tbody>"
    if result is not None :
        for row in result:           

            result = str(row[1])
            result = "".join("*" if i % 2 == 0 else ch for i, ch in enumerate(str(result)))

            pbodylist = pbodylist+"<tr>"
            pbodylist = pbodylist+"<td class='lf'>" + str(row[0]) + "</td>"
            pbodylist = pbodylist+"<td class='lf'>" + result + "</td>"            
            pbodylist = pbodylist+"<td>" + rdiffcolor(row[2],row[4]) + "</td>"
            pbodylist = pbodylist+"<td>" + cfg.format_number(row[3]) + "</td>"            
            pbodylist = pbodylist+"<td>" + rdiffcolor(row[4],row[5]) + "</td>"
            pbodylist = pbodylist+"<td>" + rdiffcolor(row[5],row[6]) + "</td>"
            pbodylist = pbodylist+"<td>" + rdiffcolor(row[6],row[7]) + "</td>"
            pbodylist = pbodylist+"<td>" + rdiffcolor(row[7],row[8]) + "</td>"
            pbodylist = pbodylist+"<td>" + rdiffcolor(row[8],row[9]) + "</td>"
            pbodylist = pbodylist+"<td>" + rdiffcolor(row[9],row[10]) + "</td>"
            pbodylist = pbodylist+"<td>" + cfg.format_number(row[10]) + "</td>"
            pbodylist = pbodylist+"</tr>"    
    pbodylist = pbodylist+"</tbody>"
    
    return render(request, 'list.html' , {                
        "pdepth1" : pdepth1
        ,"pbodylist": pbodylist        
        }
    )

def rdiffcolor(pvalue1,pvalue2):        
    if pvalue1 > pvalue2:
        return "<font color='black'>"+ cfg.format_number(pvalue1) +"</font>"
    elif pvalue1 == pvalue2:
        return "<font color='black'>"+ cfg.format_number(pvalue1) +"</font>"
    else:
        return "<font color='red'>"+ cfg.format_number(pvalue1) +"</font>"

def home(request):        

    pGArrList =[]
    pGArrValue =[]

    UrlPara = cfg.DataUrlPara()
    
    UrlPara.device = request.GET.get('pdevice')
    
    if UrlPara.device is None:
        UrlPara.device= "a" 
    
    

    pday = request.GET.get('pday')

    if pday is None:
        strSQL = " select ymd from tga_target where device ='" +UrlPara.device +"'  order by ymd desc limit 1 "
        UrlPara.ymd  = str(cfg.fnSQLselect1(strSQL))
    else:
        UrlPara.ymd  = pday

       
    UrlPara.ymd_1 = ( datetime.datetime.strptime(UrlPara.ymd, "%Y-%m-%d")  + datetime.timedelta(days=-1) ).strftime("%Y-%m-%d")
    UrlPara.ymd_7 = ( datetime.datetime.strptime(UrlPara.ymd, "%Y-%m-%d")  + datetime.timedelta(days=-7) ).strftime("%Y-%m-%d")
    UrlPara.ymd_14 = ( datetime.datetime.strptime(UrlPara.ymd, "%Y-%m-%d")  + datetime.timedelta(days=-14) ).strftime("%Y-%m-%d")

    pmemn01 =[]    
    ptmp = fn_pageview("ALL","ALL",UrlPara,pGArrList,pGArrValue)
    pmemn01.append([fn_bnttitle("조회수","ALL~~ALL", UrlPara, pGArrList, pGArrValue), ptmp])

    ptmp = fn_activeusers(UrlPara,pGArrList,pGArrValue)
    pmemn01.append([fn_bnttitle("활성 사용자","activeusers", UrlPara, pGArrList, pGArrValue), ptmp])

    ptmp = fn_firstTimePurchasers(UrlPara,pGArrList,pGArrValue)
    pmemn01.append([fn_bnttitle("최초 구매자 수","firstTimePurchasers", UrlPara, pGArrList, pGArrValue), ptmp])

    strSQL = " select depth1 ,count(distinct depth2),sum(pv) from tga_target  where ymd='" +UrlPara.ymd +"' and device ='" +UrlPara.device +"' and depth1 is not null  " 
    strSQL = strSQL + " group by depth1 order by sum(pv) desc limit 10 "    
    result_depth1 = cfg.fnSQLselect(strSQL)
    pmemn02 =[]  
    pmemnsub =[]
    rowcnt = 0 
    for row in result_depth1:           
        ptmp = fn_pageview(row[0],"ALL",UrlPara,pGArrList,pGArrValue)
        pmemn02.append([fn_bnttitle(row[0] + ' (' +cfg.format_number(row[1])+'건)',row[0]+"~~ALL", UrlPara, pGArrList, pGArrValue),ptmp ])

        if ( (row[1] > 0) & (rowcnt < 6)) :
            rowcnt =  rowcnt + 1
            ptmp = fn_menu_pageview(row[0],UrlPara, pGArrList, pGArrValue)
            pmemnsub.append(chartarray_to_html(row[0]+"<p style='font-size: 0.7em;'>"+ cfg.format_number(row[2]) +" pv</p>",ptmp,UrlPara) )


    return render(request, 'home.html' , {
        "UrlPara" :  UrlPara
        ,"pcharthtml01": chartarray_to_html("방문",pmemn01,UrlPara) 
        ,"pcharthtml02": chartarray_to_html("메뉴",pmemn02,UrlPara) 
        ,"pcharthtml03": pmemnsub[0]
        ,"pcharthtml04": pmemnsub[1]
        ,"pcharthtml05": pmemnsub[2]
        ,"pcharthtml06": pmemnsub[3]
        ,"pcharthtml07": pmemnsub[4]
        ,"pcharthtml08": pmemnsub[5]        
        }
    )