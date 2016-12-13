import xml.etree.ElementTree as ET
import os
from html_helper import *

SUMMARY_TEXT = 'summary_text'
FINAL_REPORT = 'final_report.html'
UNIT_TEST_PROJECT = 'unit'
REGRESSION_TEST_PROJECT = 'regression'
BRANCH_NAME = 'Develop'
PRODUCT_NAME = 'Norton Clean'
CURRENT = os.path.dirname(os.path.abspath(__file__))
TEMP_PATH = os.path.join(CURRENT, 'Temp')
BUILD_STAMP = 'BUILD_STAMP'
JOB_PATH_NAME = 'http://nortonmobile.usccqa.qalabs.symantec.com/jenkins/job/'

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
                        target_file.write(str(failcase.attrib['classname']+'.'+failcase.attrib['name']) + os.linesep)
                    for errorcase in general.findall(".//error/.."):
                        target_file.write(str(failcase.attrib['classname']+'.'+failcase.attrib['name']) + os.linesep)

                #write summary
                target_file.write('\n'+SUMMARY_TEXT+'Total:'+str(total)+',Failure:'+str(failure)+',Error:'+str(error))
                target_file.close()    

def write_report(source, dest):
    # filter data
    grab_unstable_case_list(source,TEMP_PATH)
    
    # create html report
    dest_file = open(dest, 'w')    
    dest_file.write(build_html_header())
    dest_file.write(build_title(PRODUCT_NAME, BRANCH_NAME))
    
    # inject tables
    for root,directories,files in os.walk(TEMP_PATH):
        # one file for one job
        for filename in files:                              
            total_builds = 0
            max_build = 0        
            source_file=open(os.path.join(root,filename), 'r')
            #final case map
            result={}            

            #write case table
            for casename in source_file:                
                if BUILD_STAMP in casename:
                    total_builds += 1
                    current = int(casename[casename.find(BUILD_STAMP)+11:])
                    if current >= max_build:
                        max_build = current
                elif SUMMARY_TEXT in casename:
                    #dest_file.write(casename.replace(SUMMARY_TEXT,''))
                    continue
                else:
                    #single case_info [fail_time, max_failed, is_still_failing]
                    if casename in result.keys():
                        case_info = result[casename]
                        case_info[0] += 1
                        case_info[1] = max_build
                    elif len(casename) >= 2:
                        case_info = [1, max_build, False]                    
                        result[casename] = case_info   
            source_file.close()
            
            #write job name
            dest_file.write(build_bond_text('Job['+ filename+ '] Latest [' + str(total_builds) +']Builds'))
            dest_file.write(build_normal_text(build_link_text('Job Test Analysis Report', JOB_PATH_NAME+filename)))
            
            #no error case
            if len(result) == 0:
                dest_file.write(build_normal_text('Stable. No Error Case Recently.'))
                continue
            
            #write table cols
            cols = ['Case Name','Total Builds', 'Failed Builds', 'Failing(%)','Fail in Latest Build']
            dest_file.write(build_table_header(cols))

            #write table data
            for key in result.keys():
                case_info = result[key]
                if max_build <= case_info[1]:
                    case_info[2] = True
                failing_rate = int(case_info[0])*100/total_builds
                latest_failing = 'Unknown'
                if(case_info[2]):
                    latest_failing = 'Yes / Build '+str(case_info[1])
                else:
                    latest_failing = 'No'
                dest_file.write(build_case_row([key, total_builds, case_info[0], str(failing_rate)+'%', latest_failing]))
            dest_file.write(build_table_foot())

    # end the html        
    dest_file.write(build_html_foot())
    dest_file.close()
            
if __name__=='__main__':
    root = os.path.join(CURRENT,'..')
    final = os.path.join(root,FINAL_REPORT) 
    write_report(root,final)
