# Raktár

## User -> Beni

- username

- password

## Customer -> Beni

- user_id

- phone

- email

- address

## Order -> Beni

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

## OrderItem -> Domi

- order_id

- stored_item_id

- quantity

- (shipment**s**)

## OrderFeedback -> Geri

- content

- order_id

## Supplier -> Dani

- user_id

## StoredItem -> Geri

- name

- quantity_available

- quantity_reserved (Kimenő rendelésekre lefoglalt termékek)

- quantity_requested (Ez jelzi, hogy hány darab termék kell még az összes rendelés teljesítéséhez)

## Shipment -> Domi

- supplier_id

- expected_at

- received

## ShipmentItem -> Dani

- stored_item_id

- quantity

## Courier -> Dani

- user_id
- order_id

## Storekeeper -> Dani

- user_id

Névkonvenciók:
ilenames = csupakicsiegybe.py -> pl.: storeditem.py

class names = KicsiEsNagy -> ÉS EGYES SZÁM!! -> pl.:  StoredItem

table names and variable names = csupa_kicsi_es_alahuzas -> táblánál többesszám!! -> pl. : stored_items
