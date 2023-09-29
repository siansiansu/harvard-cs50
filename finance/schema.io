Table users {
  id integer [primary key]
  username text
  hash text
  cash numeric
}

Table holdings {
  orderid integer [primary key]
  username text
  symbol text
  name text
  shares text
  price numeric
  transacted datetime
}

Ref: users.username > holdings.username