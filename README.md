REST API
===
Devices
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
    "devices": {
        "<identifier>": {
            "device_name": "Device 1"
        },
        "<identifier>": {
            "device_name": "Device 2"
        }
    }
}
``` 

**Get Device by Identifier**
----
Returns json data for the specified device in the network
  
### Request

  `GET /device/<identifier>`
  
### Required Parameters
  - `identifier`: An unique identification string used to identify each device

### Response

  `200 OK - on success`\
  `404 NOT FOUND - on device not found`
```json
{
    "<identifier>": {
        "device_name": "Device"
    }
}
```

**Add Device**
----
Creates a new Device
  
### Request

  `POST /device/<identifier>`
  
### Required Parameters
  - `class_name`: The name of the Device Class or Subclass of the added device

### Optional Parameters
  - `name`: The display name of the device, defaults to `class_name` if not specified

### Response

  `201 OK - on success`\
  `400 BAD REQUEST - on not unique identifier or required parameters not supplied`
```json
{
    "<identifier>": {
        "device_name": "Device"
    }
}
```

**Remove Device**
----
Removes the specified device and returns it's information

### Request

  `Delete /device/<identifier>`
  
### Required Parameters
  - `identifier`: An unique identification string used to identify each device

### Response

  `200 OK - on success`\
  `404 NOT FOUND - on device not found`
  
```json
{
    "<identifier>": {
        "device_name": "Device"
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
    "sensors": {
        "<sensor_identifier>": {
            "devices": {
                "<device_identifier>": {
                    "device_name": "Device 1"
                }
            },
            "sensor_name": "Sensor 1"
        },
        "<sensor_identifier>": {
            "devices": {
                "<device_identifier>": {
                    "device_name": "Device 2"
                }
            },
            "sensor_name": "Sensor 2"
        }
    }
}
```

**Get Sensor By Identifier**
----
Returns json data for the specified sensor in the network
  
### Request

  `GET /sensor/<identifier>`
  
### Required Parameters
  - `identifier`: An unique identification string used to identify each sensor

### Response

  `200 OK - on success`\
  `404 NOT FOUND - on sensor not found`
```json
{
    "<sensor_identifier>": {
        "devices": {
            "<device_identifier>": {
                "device_name": "Device"
            }
        },
        "sensor_name": "Sensor"
    }
}
```

**Add Sensor**
----
Creates a new Sensor
  
### Request

  `POST /sensor/<identifier>`  
  
### Required Parameters
  - `class_name`: The name of the Sensor Class or Subclass of the added device

### Optional Parameters
  - `name`: The display name of the device, defaults to `class_name` if not specified

### Response

  `201 OK - on success`\
  `400 BAD REQUEST - on not unique identifier or required parameters not supplied`
```json
{
    "<identifier>": {
        "devices": {},
        "sensor_name": "Sensor"
    }
}
```

**Remove Sensor**
----
Removes the specified sensor and returns it's information

### Request

  `Delete /sensor/<identifier>`
  
### Required Parameters
  - `identifier`: An unique identification string used to identify each sensor

### Response

  `200 OK - on success`\
  `404 NOT FOUND - on sensor not found`
  
```json
{
    "<sensor_identifier>": {
        "devices": {
            "<device_identifier>": {
                "device_name": "Device"
            }
        },
        "sensor_name": "Sensor"
    }
}
``` 

**Pair Sensor with Device**
----
Creates connection between Sensor and Device
  
### Request

  `POST /sensor/pair/<sensor_identifier>`  
  
### Required Parameters
  - `device_identifier`: The identifier of the device to be paired
  
### Response

  `200 OK - on success`\
  `404 NOT FOUND - on either the sensor or the device not being found`
```json
{
    "<sensor_identifier>": {
        "devices": {
            "<device_identifier>": {
                "device_name": "Device 1"
            },
            "<device_identifier>": {
                "device_name": "Device 2"
            }
        },
        "sensor_name": "Sensor"
    }
}
```