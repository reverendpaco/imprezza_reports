#
#sqlite3 imprezza-report.db < init-db.sql
#


cat <<HERE | sqlite3 imprezza-report.db

.mode csv
.import order_transaction.csv order_transaction
.import product_line_item_sale.csv product_line_item_sale
.import pixel_event.csv pixel_event 
.import cpc_event.csv cpc_event


create view product_by_day as 
    select 
        avg(unit_count * actual_price_per ) as avg_revenue,
        sum(unit_count * actual_price_per ) as total_revenue,
        product_name,
        product_id,
        strftime('%Y-%m-%d', creation_time ) as day
    FROM product_line_item_sale join order_transaction using(order_transaction_id)
        group by 5, product_name, product_id;


create view click_by_day as 
    select 
        avg(cost_actual) as avg_cost, 
        sum(cost_actual) as total_cost ,
        keyword,
        strftime('%Y-%m-%d', click_time ) as day
    FROM cpc_event 
        group by 4, keyword; 

HERE
