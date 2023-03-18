curl -X POST -H "Content-Type: application/json" \
    -d  '{"image_src": "https://www.foodbev.com/wp-content/gallery/food-new-releases-june-2018/Pringles-Nashville-hot-chicken.jpg",
"price": 5,"title": "Chips"}' \
    http://localhost:8000/products/


curl -X POST -H "Content-Type: application/json" \
    -d  '{"image_src": "https://www.tasteofhome.com/wp-content/uploads/2022/09/oreo-snickerdoodle-flavor-courtesy-oreo.jpg","price": 7,"title": "Oreo","quantity": 25}' \
    http://localhost:8000/products/


curl -X GET  http://localhost:8000/products/4

curl -X DELETE  http://localhost:8000/products/3


curl -X PUT -H "Content-Type: application/json" \
    -d  '{"price": 777,"title": "Oreoss"}' \
    http://localhost:8000/products/1


 curl -X PUT -H "Content-Type: application/json" \
     -d  '{"price": 777,"title": "Oreoss"}' \
    http://localhost:8000/products/4


curl -X GET  http://localhost:8000/products/4/buy


curl  -sS 'http://localhost:8000/products?limit=2&offset=2'

curl -X POST -H "Content-Type: application/json" \
    -d  '{"first_name": "John", "last_name": "Doe", "address": "Example st, 123", "email": "example@mail.com", "phone_number": "+1234567890"}' \
    http://localhost:8000/users/

curl -X GET  http://localhost:8000/products/1/buy?email=example@mail.com
