#!/bin/bash

number_of_images=2
filter_type="aden"
jwt_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im5qa2R1bW15MUBvdXRsb29rLmNvbSIsImV4cCI6MTcwODM0MDI4MywiaWF0IjoxNzA4MjUzODgzLCJhZG1pbiI6dHJ1ZX0.8pP94XSuwTs_Yf8gXhS5d_X2La72ERz4AP-PfxRd5EQ"
for (( c=1; c<=$number_of_images; c++ ))
do  
    curl -X POST -F "file$c=@./picture$c.jpg" -H "Authorization: Bearer $jwt_token" http://editimage.com/upload?filter_type=$filter_type
done