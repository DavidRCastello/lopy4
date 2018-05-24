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
    broker_address ="127.0.0.1" #Set localhost as broker address
    client = ""
    clientName = "serverPycom"
    topic = "pycom"
    def main(self):
        #Connect the code with the database and instantiates the vars conn and cur
        self.connectDB(self.database_name, self.user, self.password)
        #Connect the code with the MQTT broker
        self.connectMQTTBroker()

        self.cur.close()

    def connectMQTTBroker(self):
        #Create the connection with the MQTT broker and subscribe to the desired topic
        self.client =mqtt.Client(self.clientName)
        self.client.connect(self.broker_address)
        self.client.subscribe(self.topic)
        #Set the callback when a message is published in the topic we are subscribed
        self.client.on_message=self.on_message

        #Starts the infinite loop
        while(True):
            self.client.loop_start()

        self.client.loop_stop()

    def on_message(self, client, userdata, message):
        #When a message is published in the MQTT broker, the system get the data
        print("message received " ,str(message.payload.decode("utf-8")))
        msg = str(message.payload.decode("utf-8"))
        #Converts the string (JSON-like) raw data to a JSON
        msgDic = json.loads(msg)
        #The system gets data for each required attribute declared in attr dictionary
        for key in self.attr:
            self.attr[key] = msgDic[key]

        #Insert the data in the "Data" database table
        self.insertRow("Data",self.attr["timestamp"],self.attr["sensor"],self.attr["measurement"])


    def connectDB(self, db,user,password):
        #Create the connection and cursor used for the database communication
        self.conn = psycopg2.connect("dbname="+db+" user="+user+" password="+password)
        self.cur = self.conn.cursor()

    def insertRow(self,table, ts,sens,meas):
        #Create the SQL query in order to insert a new row
        sql= "INSERT INTO public.\""+table+"\" (timestamp, sensor, measurement) VALUES (\'"+ts+"\', \'"+sens+"\', "+str(meas)+");"
        self.cur.execute(sql)
        self.conn.commit()

if __name__ == "__main__":
    listener().main()
