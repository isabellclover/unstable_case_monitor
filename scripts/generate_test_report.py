import xml.etree.ElementTree as ET
import os

SUMMARY_TEXT = 'summary_text'
FINAL_REPORT = 'final_report.html'
UNIT_TEST_PROJECT = 'unit'
REGRESSION_TEST_PROJECT = 'regression'
BRANCH_NAME = 'Develop'
PRODUCT_NAME = 'Norton Clean'
CURRENT = os.path.dirname(os.path.abspath(__file__))
TEMP = os.path.join(CURRENT, 'temp.txt')

def grab_unstable_case_list(root_path, target_file_path):
    target_file = open(target_file_path, 'w')
    total = 0
    failure = 0
    error = 0
    for root,directories,files in os.walk(root_path):
        for filename in files:
            if '.xml' in filename:
                datafile = os.path.join(root,filename)
                tree = ET.parse(datafile)
                general = tree.getroot()
                if(general.tag != 'testsuite'):
                    general = general.find('testsuite')
                if general==None:
                    continue
                total += int(general.attrib['tests'])
                if general.attrib['failures']=='0' and general.attrib['errors']=='0':
                    print 'all passed, skip'
                    continue
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
    html_txt = '<table style="border: 1px solid #dddddd;text-align: left;padding: 8px;"><tr style="background-color::#dddddd">'
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

def build_title():
    html = '<h1>'
    html += (PRODUCT_NAME+' '+BRANCH_NAME+' '+'Unstable Case')
    html += '</h1>'
    return html

def write_report(source, dest):
    grab_unstable_case_list(source,TEMP)    
    dest_file = open(dest, 'w')    
    dest_file.write(build_html_header())
    dest_file.write(build_title())
    source_file=open(TEMP, 'r')
    result={}
    for casename in source_file:        
        if not (SUMMARY_TEXT in casename):
            if casename in result.keys():
                result[casename]+=1
            elif len(casename) >= 2:
                result[casename]=1
        else:
            dest_file.write(casename.replace(SUMMARY_TEXT,''))
    source_file.close()
    cols = ['Case Name','Fail Times']
    dest_file.write(build_table_header(cols))
    for key in result.keys():
        dest_file.write(build_case_row([key,result[key]]))
    dest_file.write(build_table_foot())
    dest_file.write(build_html_foot())
    dest_file.close()
            
if __name__=='__main__':
    root = os.path.join(CURRENT,'..')
    final = os.path.join(root,FINAL_REPORT) 
    write_report(root,final)
