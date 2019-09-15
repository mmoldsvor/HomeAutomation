REST API
===

**List Devices**
----
  Returns json data for every device in the network

### Request

  `GET /devices/list`

### Response

  `200 OK - on success`
  
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

**Get Device By Identifier**
----
  Returns json data for the specified device in the network
  
### Required Parameters
  - identifier:  

### Request

  `GET /device/<identifier>`

### Response

  `200 OK - on success`\
  `404 NOT FOUND - on device not found`
```json
{
  "<device_identifier>": {
    "device_name": "Stue Lys"
  }
}
```

Sensors
===   
    
**List Sensors**
----
  Returns json data for every sensor in the network

### Request

  `GET /sensors/list`

### Response

  `200 OK - on success`
  
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

**Get Sensor By Identifier**
----
  Returns json data for the specified sensor in the network
  
### Required Parameters
  - identifier:  

### Request

  `GET /sensor/<identifier>`

### Response

  `200 OK - on success`\
  `404 NOT FOUND - on sensor not found`
```json
{
  "<sensor_identifier>": {
    "devices": [
      {
        "<device_identifier>": {
          "device_name": "Stue Lys"
        }
      }
    ],
    "sensor_name": "Stue Vest"
  }
}
```