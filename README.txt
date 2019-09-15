**List Devices**
----
  Returns json data every device in the network

* **URL**

  /devices/list

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `id=[integer]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
        "devices": [
            {
                "5049852": {
                    "name": "Stue Lys"
                }
            },
            {
                "5049845": {
                    "name": "Test"
                }
            }
        ]
    }`
 
* **Error Response:**
  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`