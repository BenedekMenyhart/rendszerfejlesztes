# Raktár

## User

- username

- password

## Customer

- user_id

- phone

- email

- address

## Order

- (items)

- customer_id

- status: Enum
  
  - recieved
  
  - processing (Pl ha nincs minden raktáron és rendelni kell)
  
  - processed (Ha minden van raktáron, de még nincs futárnak átadva)
  
  - assigned_to_courier
  
  - delivery_started
  
  - delivered
  
  - recipient_confirmed

- courier_id

- created_at

## OrderItem

- order_id

- stored_item_id

- quantity

- (shipment**s**)

## OrderFeedback

- content

- order_id

## Supplier

- user_id

## StoredItem

- name

- quantity_available

- quantity_reserved (Kimenő rendelésekre lefoglalt termékek)

- quantity_requested (Ez jelzi, hogy hány darab termék kell még az összes rendelés teljesítéséhez)

## Shipment

- supplier_id

- expected_at

- received

## ShipmentItem

- stored_item_id

- quantity

## Courier

- user_id

## Storekeeper

- user_id

-