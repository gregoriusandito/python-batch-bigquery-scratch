from datetime import datetime, timedelta
from google.cloud import bigquery
client = bigquery.Client()

def custom_batch_process(start_date = None, end_date = None):
    if (start_date == None and end_date == None):
        # if start date and end date is not defined
        end_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
        start_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    elif (end_date == None):
        # if start date defined but end date is not defined, set end date as today
        end_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    elif (start_date == None):
        # if end date is defined but the start date is not defined, set start date to before end date
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        start_date = datetime.strftime(end_date - timedelta(1), '%Y-%m-%d')    
    
    if ( datetime.strptime(start_date, '%Y-%m-%d') > datetime.strptime(end_date, '%Y-%m-%d') ):
        # start date must be earlier than the end date
        return print("wrong input, start date must be earlier than end_date. Aborting")
    
    query = (
        'SELECT order_date, order_type, sum(bulk_total_customer) OVER (PARTITION BY order_type, order_payment ORDER BY bulk_total_customer) AS total_customer_per_order_detail, sum(bulk_total_customer) OVER () AS total_customer, order_payment'  
        'FROM (SELECT Date(order_time) as order_date, order_type, COUNT(order_type) AS bulk_total_customer, order_payment FROM (`bi-dwhdev-01:source.daily_order`) WHERE ORDER_STATUS = "Completed" GROUP BY order_date, order_type, order_payment)'
        'WHERE DATE(order_date) between DATE(%s) and DATE(%s)'
        'ORDER BY order_date, total_customer_per_order_detail, order_payment'% (start_date, end_date)
    )

    query_job = client.query(
        query,
        location="US",
    )  

    for row in query_job:
        print(row)


custom_batch_process(start_date = None, end_date = None)

