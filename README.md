REST API
===

**List Devices**
----
  Returns json data for every device in the network

### Request

  `GET /devices/list`

### Response

  `200 OK - on success`\
  `401 UNAUTHORIZED - on failed authorization`

  
  ```json
    {
        "devices": [
            {
                "<device_identifier>": {
                    "device_name": "Stue Lys"
                }
            },
            {
                "<device_identifier>": {
                    "device_name": "Test"
                }
            }
        ]
    }
```    
    
**List Sensors**
----
  Returns json data for every sensor in the network

### Request

  `GET /sensors/list`

### Response

  `200 OK - on success`\
  `401 UNAUTHORIZED - on failed authorization`

  
  ```json
    {
       "sensors":[
          {
             "<sensor_identifier>":{
                "devices":[
                   {
                      "<device_identifier>":{
                         "device_name":"Stue Lys"
                      }
                   }
                ],
                "sensor_name":"Stue Vest"
             }
          },
          {
             "<sensor_identifer>":{
                "devices":[
                   {
                      "<device_identifier>":{
                         "device_name":"Stue Lys"
                      }
                   }
                ],
                "sensor_name":"Stue Øst"
             }
          }
       ]
    }
```    