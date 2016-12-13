import xml.etree.ElementTree as ET
import os

def build_html_header():
    html_txt = '<!DOCTYPE html><html><head>'
    html_txt += '</head><body>'
    return html_txt

def build_html_foot():
    html_txt = '</body></html>'
    return html_txt

def build_table_header(cols):
    html_txt = '<table class="pane sortable bigtable stripped"><tr class="pane-header">'
    for col in cols:
        html_txt += ('<th>'+str(col)+'</th>')
    html_txt += '</tr>'
    return html_txt

def build_table_foot():
    return '</table>'

def build_case_row(datas):
    html = '<tr>'
    for data in datas:
        html += '<td class="pane no-wrap">'+str(data)+'</td>'
    html += '</tr>'
    return html

def build_bond_text(line):
    html = '<p><b>'+ str(line) +'</b></p>'
    return html

def build_normal_text(line):
    return '<p>'+ str(line)+'</p>'

def build_title(product, branch):
    html = '<h1>'
    html += (product+' '+branch+' '+'Unstable Case')
    html += '</h1>'
    return html

def build_link_text(link_text, url):
    html = '<u><a href=\"'
    html += url
    html += ('">' + link_text + '</a></u>')
    return html 
