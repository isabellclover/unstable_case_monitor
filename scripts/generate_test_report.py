import os
from html_helper import *
from data_helper import *

SUMMARY_TEXT = 'summary_text'
FINAL_REPORT = 'final_report.html'
BRANCH_NAME = 'Product'
PRODUCT_NAME = 'Norton Mobile'

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
            all_builds = []
            current = 0
            source_file=open(os.path.join(root,filename), 'r')
            #final case map
            result={}            

            #write case table
            for casename in source_file:                
                if BUILD_STAMP in casename:                    
                    current = int(casename[casename.find(BUILD_STAMP)+11:])
                    if not (current in all_builds):
                        all_builds.append(current)
                elif SUMMARY_TEXT in casename:
                    #dest_file.write(casename.replace(SUMMARY_TEXT,''))
                    continue
                else:
                    #single case_info [fail_time, max_failed, is_still_failing]
                    if casename in result.keys():
                        case_info = result[casename]
                        case_info[0] += 1
                        if(current >= case_info[1]):
                            case_info[1] = current
                    elif len(casename) >= 2:
                        case_info = [1, current, False]                    
                        result[casename] = case_info   
            source_file.close()
            
            #write job name
            dest_file.write(build_bond_text('Job['+ filename+ '] Latest [' + str(len(all_builds)) +']Builds'))
            dest_file.write(build_normal_text(build_link_text('Job Test Analysis Report', JOB_PATH_NAME+filename+'/test_results_analyzer')))
            
            #no error case
            if len(result) == 0:
                dest_file.write(build_normal_text('Stable. No Error Case Recently.'))
                continue
            
            #write table cols
            cols = ['Case Name','Total Builds', 'Failed Builds', 'Failing(%)','Fail in Latest Build']            

            #write table data
            failing_list = rebuild_res_list(result, all_builds, filename)
            #failing_list = split_res_list(data_source, True)
            #fixed_list = split_res_list(data_source, False)

            dest_file.write(build_table_header(cols))
            for case in failing_list.keys():
                info = failing_list[case]
                dest_file.write(build_case_row([case, info[0], info[1], str(info[2])+'%',info[4]]))

            #dest_file.write(build_row_header(cols))
            #for case in failing_list.keys():
            #    info = failing_list[case]
            #    dest_file.write(build_case_row([case, info[0], info[1], str(info[2])+'%',info[4]]))
                
            dest_file.write(build_table_foot())

    # end the html        
    dest_file.write(build_html_foot())
    dest_file.close()
            
if __name__=='__main__':
    root = os.path.join(CURRENT,'..')
    final = os.path.join(root,FINAL_REPORT) 
    write_report(root,final)
