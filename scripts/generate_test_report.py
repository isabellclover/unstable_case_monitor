import xml.etree.ElementTree as ET
import os

SUMMARY_TEXT = 'summary_text'
FINAL_REPORT = 'final_report.html'
UNIT_TEST_PROJECT = 'unit'
REGRESSION_TEST_PROJECT = 'regression'
BRANCH_NAME = 'Develop'
PRODUCT_NAME = 'Norton Clean'
CURRENT = os.path.dirname(os.path.abspath(__file__))
TEMP_PATH = os.path.join(CURRENT, 'Temp')
BUILD_STAMP = 'BUILD_STAMP'

def grab_unstable_case_list(root_path, target_file_path):    
    total = 0
    failure = 0
    error = 0
    os.mkdir(TEMP_PATH)
    for root,directories,files in os.walk(root_path):
        for filename in files:
            if '.xml' in filename and 'TEST' in filename:
                print 'Find Test report as' + filename
                print root
                #get job and build information
                jobinfo = root[root.find('TestReports'):].split(os.sep)
                jobname = jobinfo[1]
                buildnumber = jobinfo[2]
                datafile = os.path.join(root,filename)                
                target_file = open(target_file_path + os.sep + jobname, 'a')
                target_file.write('\n'+BUILD_STAMP+buildnumber+'\n')
                
                #begin parse TEST.xml
                tree = ET.parse(datafile)
                general = tree.getroot()
                if(general.tag != 'testsuite'):
                    general = general.find('testsuite')
                if general==None:
                    continue
                total += int(general.attrib['tests'])

                #all case passed
                if general.attrib['failures']=='0' and general.attrib['errors']=='0':
                    print 'all passed, skip'
                    continue
                #find error/failed case
                else:
                    failure += int(general.attrib['failures'])
                    error += int(general.attrib['errors'])                    
                    for failcase in general.findall('.//failure/..'):
                        print 'fail case:' + failcase.tag
                        target_file.write(str(failcase.attrib['classname']+'.'+failcase.attrib['name']) + os.linesep)
                    for errorcase in general.findall(".//error/.."):
                        print 'error case:' + errorcase.tag
                        target_file.write(str(failcase.attrib['classname']+'.'+failcase.attrib['name']) + os.linesep)
                target_file.write('\n'+SUMMARY_TEXT+'Total:'+str(total)+',Failure:'+str(failure)+',Error:'+str(error))
                target_file.close()    

def build_html_header():
    html_txt = '<!DOCTYPE html><html><head>'
    html_txt += '</head><body>'
    return html_txt

def build_html_foot():
    html_txt = '</body></html>'
    return html_txt

def build_table_header(cols):
    html_txt = '<table style="border: 1px solid #000000;text-align: left;padding: 8px;"><tr style="background-color:#dddddd">'
    for col in cols:
        html_txt += ('<th>'+str(col)+'</th>')
    html_txt += '</tr>'
    return html_txt

def build_table_foot():
    return '</table>'

def build_case_row(datas):
    html = '<tr>'
    for data in datas:
        html += '<td style="text-align:left">'+str(data)+'</td>'
    html += '</tr>'
    return html

def build_bond_text(line):
    html = '<p><b>'+line+'</b></p>'
    return html

def build_normal_text(line):
    return '<p>'+line+'</p>'

def build_title():
    html = '<h1>'
    html += (PRODUCT_NAME+' '+BRANCH_NAME+' '+'Unstable Case')
    html += '</h1>'
    return html

def write_report(source, dest):
    # filter data
    grab_unstable_case_list(source,TEMP_PATH)
    
    # create html report
    dest_file = open(dest, 'w')    
    dest_file.write(build_html_header())
    dest_file.write(build_title())
    
    # inject tables
    for root,directories,files in os.walk(TEMP_PATH):
        for filename in files:                              
            buildnumber = 0
            source_file=open(os.path.join(root,filename), 'r')
            result={}           

            #write case table
            for casename in source_file:
                if BUILD_STAMP in casename:
                    buildnumber += 1
                elif SUMMARY_TEXT in casename:
                    #dest_file.write(casename.replace(SUMMARY_TEXT,''))
                    continue
                else:
                    if casename in result.keys():
                        result[casename]+=1
                    elif len(casename) >= 2:
                        result[casename]=1
            source_file.close()
            
            #write job name
            dest_file.write(build_bond_text('Job['+ filename+ '] Latest [' + str(buildnumber) +']Builds'))
            if len(result) == 0:
                continue
            #cols = ['Package Name','Case Name', 'Failing Rate', 'Still Fail in latest 5 builds', 'Latest Message', 'Report Link']
            cols = ['Case Name','Total Builds', 'Failed Builds', 'Failing Rate']
            dest_file.write(build_table_header(cols))
            for key in result.keys():
                dest_file.write(build_case_row([key,buildnumber, result[key], '0']))
            dest_file.write(build_table_foot())

    # end the html        
    dest_file.write(build_html_foot())
    dest_file.close()
            
if __name__=='__main__':
    root = os.path.join(CURRENT,'..')
    final = os.path.join(root,FINAL_REPORT) 
    write_report(root,final)
