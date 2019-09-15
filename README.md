**List Devices**
----
  Returns json data for every device in the network

### Request

  `GET /devices/list`

### Success Response:

  * **Code:** 200 <br />
    **Content:** `{
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
    }`
 
### Error Response:
  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`
    
    
**List Sensors**
----
  Returns json data for every sensor in the network

* **URL**

  /sensors/list

* **Method:**

  `GET`
  
*  **URL Params**

  None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `
    {
        "sensors": [
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
            },
            {
                "<sensor_identifer>": {
                    "devices": [
                        {
                            "<device_identifier>": {
                                "device_name": "Stue Lys"
                            }
                        }
                    ],
                    "sensor_name": "Stue Øst"
                }
            }
        ]
    }`
 
* **Error Response:**
  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`