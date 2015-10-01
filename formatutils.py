#!/usr/bin/env python

"""formatutils.py: HTML formatting utilities ..."""

__author__  = "minos197@gmail.com"
__license__ = "LGPL"
__version__ = "0.0.1"
__email__   = "Minos Galanakis"
__project__ = "harpy"
__date__    = "30-09-2015"

from copy import deepcopy

def tabularize_data(headers, data):
    """ Generate an html table from dictionary data """

    # Create the table header
    table_data = "<table border=\"1\" style=\"width:300px\"><thead><tr>"
    for h in headers:
      table_data += "<th>%s</th>"%h
    table_data += "</tr></thead>"

    #Create Table Body
    table_rows = ""
    for entry in data.keys():
      entry_dt = data[entry]
      table_rows += "<tr><td>%s</td>"%entry
      # TODO. Remove it when dictionary is properly generated
      if "color" not in entry_dt.keys(): entry_dt['color']= ""
      for e in entry_dt.keys():
        if e == "time":
          table_rows += "<td>%s</td>"% entry_dt[e].strftime("%w %b %Y %H:%M:%S")
        else:
          table_rows += "<td>%s</td>"% entry_dt[e]

      table_rows += "</tr>"
    
    table_data += table_rows
    table_data += "</table>"

    #print table_data
    return table_data

def gen_radio_buttons(gtype, label, data):
    """Generate a radio buttong group for dynamic forms"""

    form = "<label for=\"%s\">%s:</label>\n"%(gtype,label)
    headers = ["IP","MAC","Hostname","Alias","Last Seen","Color","Select"]
    #make a copy of the dictionary
    temp_data = deepcopy(data)
    
    for entry in temp_data.keys():
      temp_data[entry]['button']= "<input type=\"radio\" name=\"%s\" value=\"%s\" /><br />"%(gtype,entry)

    return tabularize_data(headers,temp_data)

def datedelta_to_human(td, text = False):
    """ Adjust datetime delta object in a more human friend format """

    hrf = (td.days, td.seconds//3600, (td.seconds//60)%60,td.seconds % 60)
    if not text:
      return hrf
    else:
      return("%s days %s hours %s mins %s sec"%hrf)

def datetime_to_human(dt):
    """ Adjust datetime object in a more human friend format """

    return dt.strftime("%w %b %Y %H:%M:%S")

if __name__ == "__main__":
    pass
