--- USE SENSOR DATA --
'POST /sensorData'

## RESPONSE ##
- '200 OK' if successful

return:
    json = {
        'return': 'success'
    }


--- LIST ALL DEVICES ---

'GET /devices/list'

## RESPONSE ##
- '200 OK' if successful

return:
    json =
    {
        "devices": {
            "5049830": {
                "name": "Stue Lys",
                "sensors": [
                    "projects/blpso805uuabl6lgd3cg/devices/bja0082e27fg00a7fing",
                    "projects/blpso805uuabl6lgd3cg/devices/bja00677cdlg00ba0epg"
                ]
            },
            "5049845": {
                "name": "Test",
                "sensors": [
                    "projects/blpso805uuabl6lgd3cg/devices/bja0abj1or1g00e49m7g"
                ]
            }
        }
    }


--- REGISTER NEW SOCKET ---

'POST /devices'

## ARGUMENTS ##

- 'device_type':str
- 'identifier':str
- 'name':str
- 'socket_type':str

## RESPONSE ##
- '201 CREATED' if successfully created

return:
    json = {
        'identifier': 'stuelys_dimmer'
        'name': 'Stuelys'
        'socket_type': 'dimmer'
        'encoding': 100111
    }


--- ADD SENSOR TO DEVICE ---

- 'POST /device/<identifier>/addSensor'

## ARGUMENTS ##

- 'sensor_id':str

--- GET SOCKET ---

'GET /device/<identifier>'

## RESPONSE ##
- '404 NOT FOUND' if no socket was found
- '200 OK' if successfully returned


--- REMOVE SOCKET ---

'DELETE /device/<identifier>'

## RESPONSE ##
- '404 NOT FOUND' if no socket was found
- '200 OK' if successfully removed