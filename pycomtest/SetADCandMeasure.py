import machine
import time

adc = machine.ADC(0)
adc_c = adc.channel(pin='P13',attn=machine.ADC.ATTN_11DB)
adc_c()

while True:
    val = adc_c.value()              # read an analog value
    print("El valor es " + str(val))
    time.sleep(2)
