import httplib2
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from ga_sheets import *
import datetime

def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):

  credentials = ServiceAccountCredentials.from_p12_keyfile(
    service_account_email, key_file_location, scopes=scope)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service


def get_results(service):  # Use the Analytics Service Object to query the Core Reporting API
  # for the number of sessions within the past seven days.
  return service.data().realtime().get(
      ids='ga:' + 'xxx',
      metrics='rt:activeUsers',
      filters='rt:eventAction==video_error_ad',
      dimensions='rt:eventCategory, rt:eventAction, rt:minutesAgo').execute()

# 2. Print out the Real-Time Data
# The components of the report can be printed out as follows:

def print_realtime_report(results):
  print '**Real-Time Report Response**'
  print_report_info(results)
  print_query_info(results.get('query'))
  print_profile_info(results.get('profileInfo'))
  print_column_headers(results.get('columnHeaders'))
  print_data_table(results)
  print_totals_for_all_results(results)

def print_data_table(results):
  print 'Data Table:'
  # Print headers.
  output = []
  for header in results.get('columnHeaders'):
    output.append('%30s' % header.get('name'))
  print ''.join(output)
  # Print rows.
  if results.get('rows', []):
    for row in results.get('rows'):
      output = []
      for cell in row:
        output.append('%30s' % cell)
      print ''.join(output)
  else:
    print 'No Results Found'

def print_column_headers(headers):
  print 'Column Headers:'
  for header in headers:
    print 'Column name           = %s' % header.get('name')
    print 'Column Type           = %s' % header.get('columnType')
    print 'Column Data Type      = %s' % header.get('dataType')

def print_query_info(query):
  if query:
    print 'Query Info:'
    print 'Ids                   = %s' % query.get('ids')
    print 'Metrics:              = %s' % query.get('metrics')
    print 'Dimensions            = %s' % query.get('dimensions')
    print 'Sort                  = %s' % query.get('sort')
    print 'Filters               = %s' % query.get('filters')
    print 'Max results           = %s' % query.get('max-results')

def print_profile_info(profile_info):
  if profile_info:
    print 'Profile Info:'
    print 'Account ID            = %s' % profile_info.get('accountId')
    print 'Web Property ID       = %s' % profile_info.get('webPropertyId')
    print 'Profile ID            = %s' % profile_info.get('profileId')
    print 'Profile Name          = %s' % profile_info.get('profileName')
    print 'Table Id              = %s' % profile_info.get('tableId')

def print_report_info(results):
  print 'Kind                    = %s' % results.get('kind')
  print 'ID                      = %s' % results.get('id')
  print 'Self Link               = %s' % results.get('selfLink')
  print 'Total Results           = %s' % results.get('totalResults')

def print_totals_for_all_results(results):
  totals = results.get('totalsForAllResults')
  for metric_name, metric_total in totals.iteritems():
    print 'Metric Name  = %s' % metric_name
    print 'Metric Total = %s' % metric_total

    #GET THE CURRENT TIME TO CREATE A TIME STAMP OF WHEN YOU RETREIVED THE DATA
    currentDT = datetime.datetime.now()

    print ("Current Year is: %d" % currentDT.year)
    print ("Current Month is: %d" % currentDT.month)
    print ("Current Day is: %d" % currentDT.day)
    print ("Current Hour is: %d" % currentDT.hour)
    print ("Current Minute is: %d" % currentDT.minute)
    print ("Current Second is: %d" % currentDT.second)
    print ("Current Microsecond is: %d" % currentDT.microsecond)

    #CALL THE FUNCTION FROM YOUR GOOGLE SHEETS API SO WHEN THIS SCRIPT TO GET THE DATA RUNS, IT ALSO RUNS THE UPDATE GA SHEET SCRIPT AT THE SAME TIME

    client = gspread.authorize(creds)
    sheet = client.open("Ad Start For Dashboard").sheet1

    #USE THIS TO UPDATE SHEET
    #sheet.update_cell(2, 2, metric_total)
    #sheet.update_cell(2, 1, metric_name)
    #sheet.update_cell(2, 3, currentDT.year)
    #sheet.update_cell(2, 4, currentDT.month)
    #sheet.update_cell(2, 5, currentDT.day)
    #sheet.update_cell(2, 6, currentDT.hour)
    #sheet.update_cell(2, 7, currentDT.minute)

    #USE THIS TO APPED A NEW ROW TO A SHEET (MAYBE A CHART OR SAVING HISTORICAL DATA)
    sheet.append_row([metric_name,metric_total,currentDT.hour,currentDT.minute, currentDT.second,currentDT.day,currentDT.month,currentDT.year])


def main():
  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/analytics.readonly']

  service_account_email = 'YOUR_SERVICE_ACCT.iam.gserviceaccount.com'
  key_file_location = 'C:/Users/xxx/PycharmProjects/xxx/xxx-3b8882cbd642.p12'

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,
    service_account_email)

  #print_data_table(get_results(service))

  print_realtime_report(get_results(service))


if __name__ == '__main__':
  main()