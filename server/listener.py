import psycopg2
import json
import time
import paho.mqtt.client as mqtt
class listener:
    database_name = "pycom"
    user = "postgres"
    password = "postgres"
    conn =""
    cur = ""
    attr = {"timestamp":"","sensor":"","measurement":""}
    broker_address ="127.0.0.1"
    client = ""
    clientName = "serverPycom"
    topic = "pycom"
    def main(self):
        self.connectDB(self.database_name, self.user, self.password)
        self.connectMQTTBroker()
        #id, timestamp, sensor, me()asurement
        #the id is autogenerated by postgresql as it is used as primary key

        #self.insertRow("Data",'1971-07-13',1,2.1)
        #self.insertRow()
        self.connectMQTTBroker()
        self.cur.close()

    def connectMQTTBroker(self):
        self.client =mqtt.Client(self.clientName)
        self.client.connect(self.broker_address)
        self.client.subscribe(self.topic)
        self.client.on_message=self.on_message

        while(True):
            self.client.loop_start()

        self.client.loop_stop()

    def on_message(self, client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        msg = str(message.payload.decode("utf-8"))
        msgDic = json.loads(msg)

        for key in self.attr:
            self.attr[key] = msgDic[key]
            if key in "timestamp":
                print(self.attr[key])
        self.insertRow("Data",self.attr["timestamp"],self.attr["sensor"],self.attr["measurement"])

        #mosquitto_pub -t 'pycom' -m '{"timestamp":"1971-07-13","sensor":1,"measurement":2.1}'

        #print("message topic=",message.topic)
        #print("message qos=",message.qos)
        #print("message retain flag=",message.retain)


    def connectDB(self, db,user,password):
        self.conn = psycopg2.connect("dbname="+db+" user="+user+" password="+password)
        self.cur = self.conn.cursor()

    def insertRow(self,table, ts,sens,meas):
        sql= "INSERT INTO public.\""+table+"\" (timestamp, sensor, measurement) VALUES (\'"+ts+"\', \'"+sens+"\', "+str(meas)+");"
        print sql
        self.cur.execute(sql)
        self.conn.commit()

if __name__ == "__main__":
    #listener().main()
    listener().main()
