import machine

adc = machine.ADC()
# Output Vref of P13
adc.vref_to_pin('P22')
# # Set calibration - see note above
adc.vref(1100)
# # Check calibration by reading a known voltage
adc_c = adc.channel(pin='P13', attn=machine.ADC.ATTN_11DB)
while True:
    apin = adc.channel(pin='P13')   # create an analog pin on P16
    val = apin()                    # read an analog value
    print("El valor es " + str(val))
