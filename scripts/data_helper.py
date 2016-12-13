import xml.etree.ElementTree as ET
import os

SUMMARY_TEXT = 'summary_text'
BUILD_STAMP = 'BUILD_STAMP'
CURRENT = os.path.dirname(os.path.abspath(__file__))
TEMP_PATH = os.path.join(CURRENT, 'Temp')

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

   
