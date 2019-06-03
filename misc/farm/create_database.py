from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086)
print(client.get_list_database())

dbname = 'raspberrypi'
if not any(db['name'] == dbname for db in client.get_list_database()):
    client.create_database(dbname)

print(client.get_list_database())
#client.drop_database(dbname)
#print(client.get_list_database())
