import xml.etree.ElementTree as ET
import os
from html_helper import *

SUMMARY_TEXT = 'summary_text'
BUILD_STAMP = 'BUILD_STAMP'
CURRENT = os.path.dirname(os.path.abspath(__file__))
TEMP_PATH = os.path.join(CURRENT, 'Temp')
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

# returns as data{casename: case_info[total_builds, fail_builds, failing_rate, is_latest_failing, failing_link]}
def rebuild_res_list(result, all_builds, job_name):
    data = {}
    for key in result.keys():
        #init final item
        data_key = key
        data_info = [0,0,0,False,'']
        
        #get source data
        case_info = result[key]
        latest_failed_build = case_info[1]
        if max(all_builds) <= latest_failed_build:
            case_info[2] = True            
        failing_rate = int(case_info[0])*100/len(all_builds)
        latest_failed_text = 'Unknown'
        if(case_info[2]):
            build_link = build_link_text('Build '+str(latest_failed_build), JOB_PATH_NAME+job_name+'/'+str(latest_failed_build)+'/testReport')
            latest_failed_text = 'Yes / '+ build_link
        else:
            latest_failed_text = 'No'

        #buid final item
        data_info[0] = len(all_builds) #total executed builds
        data_info[1] = case_info[0] #total failed builds
        data_info[2] = failing_rate # failing rate
        data_info[3] = case_info[2] # is still failing
        data_info[4] = latest_failed_text # txt info
        data[data_key] = data_info
        
    return data
        
def split_res_list(source, is_failing):
    res = {}
    for key in source.keys():
        case_info = source[key]
        if case_info[3] == is_failing:
            res[key] = case_info
    return res

def sort_res_list_by_rating(source):
    pass
