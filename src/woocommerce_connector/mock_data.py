ORDERS = [
    {"id":1001,"status":"processing","currency":"INR","total":"1499.00","billing":{"email":"maya@example.test","first_name":"Maya","last_name":"Shah"},"line_items":[{"product_id":501,"name":"Everyday Backpack","quantity":1,"total":"1499.00"}]},
    {"id":1002,"status":"completed","currency":"INR","total":"2499.00","billing":{"email":"arun@example.test","first_name":"Arun","last_name":"Mehta"},"line_items":[{"product_id":502,"name":"Travel Bottle","quantity":2,"total":"2499.00"}]},
    {"id":1003,"status":"on-hold","currency":"INR","total":"799.00","billing":{"email":"maya@example.test","first_name":"Maya","last_name":"Shah"},"line_items":[{"product_id":503,"name":"Desk Cable Kit","quantity":1,"total":"799.00"}]},
]

PRODUCTS = [
    {"id":501,"name":"Everyday Backpack","sku":"BAG-001","price":"1499.00","stock_status":"instock"},
    {"id":502,"name":"Travel Bottle","sku":"BOT-002","price":"1249.50","stock_status":"instock"},
    {"id":503,"name":"Desk Cable Kit","sku":"CAB-003","price":"799.00","stock_status":"outofstock"},
]
