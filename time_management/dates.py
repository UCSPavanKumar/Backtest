from datetime import datetime, timedelta

back_test_dates = ['{0}-01-01|{0}-01-31',
                    '{0}-02-01|{0}-02-27',
                    '{0}-03-01|{0}-03-31',
                    '{0}-04-01|{0}-04-30',
                    '{0}-05-01|{0}-05-31',
                    '{0}-06-01|{0}-06-30',
                    '{0}-07-01|{0}-07-31',
                    '{0}-08-01|{0}-08-31',
                    '{0}-09-01|{0}-09-30',
                    '{0}-10-01|{0}-10-31',
                    '{0}-11-01|{0}-11-30',
                    '{0}-12-01|{0}-12-31',
          ]

intraday_dates = [(datetime.now()+timedelta(days=-1)).strftime('%Y-%m-%d')+'|'+(datetime.now()+timedelta(days=0)).strftime('%Y-%m-%d')]
