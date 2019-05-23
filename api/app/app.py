import os
import pyodbc
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

api_host_os = os.name
server = os.environ['dbServer']
database = 'asterisk'
username = os.environ['dbLogin']
password = os.environ['dbPassword']

# Use different driver based on OS version
if api_host_os=='posix':
    cnxn = pyodbc.connect('Driver={FreeTDS};SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
else:
    cnxn = pyodbc.connect('Driver={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = cnxn.cursor()


def get_data(channel=' !=\'\'',_startDate='2019-05-07 00:00:00',_endDate='2019-05-08 23:59:59',_status="=\'ANSWERED\'"):
    #Get all data query
    query = "select c.userfield,c.start,c.id,c.uniqueid,c.dstchannel,c.disposition,c.src,oc.eventtime as strttime,cc.eventtime as clstime,datediff(second,oc.eventtime,cc.eventtime) as diff " \
        "from cdr1 as c join cel as oc on c.uniqueid=oc.uniqueid join cel as cc on c.uniqueid=cc.uniqueid" \
        " "+f"where c.start >= \'{_startDate}\' and c.start <= \'{_endDate}\' and c.dstchannel {channel}" \
        " and oc.eventtype='BRIDGE_ENTER' and cc.eventtype='BRIDGE_EXIT' and c.dcontext in ('24ns-ivr','ivr-support-ua','ivr-support-ru')" \
        " "+ f"and c.disposition{_status} order by c.id desc"
    cursor.execute(query)

    result = []

    #Get columns names
    columns = [column[0] for column in cursor.description]

    #Create list w/ objects like comumn_name:value
    for row in cursor.fetchall():

        #Verify all except answered w/ no call time and no media source
        if row.disposition!='ANSWERED':
            row.diff='-'
            row.userfield=''

        #Trim just operator number from long response DB query string
        row.dstchannel=row.dstchannel[4:8]

        result.append(dict(zip(columns, row)))
    return result

@app.route('/api/calls', methods=['POST'])
def get_calls():

    #Get values from request
    operator=request.get_json()['operator']
    startDate=request.get_json()['startDate']
    endDate=request.get_json()['endDate']
    status=request.get_json()['status']

    #Set values in proper way
    _startDate=f"{startDate} 00:00:00"
    _endDate=f"{endDate} 23:59:59"
    if status=="all":
        _status=" in (\'ANSWERED\',\'BUSY\',\'NO ANSWER\') "
    else:
        _status=f"=\'{status}\'"
    if operator=="all":
        _operator=" !=\'\'"
    else:
        _operator=f" like \'%{operator}%\'"

    #Fetch data from DB w/ get_data() function
    result = get_data(_startDate=_startDate,_endDate=_endDate,channel=_operator,_status=_status)

    #responce results with fetched data
    return jsonify(result)

app.run(host='0.0.0.0',port=3000,debug=True)