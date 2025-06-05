

##Buttons
##IO_L20N_T3_34
set_property PACKAGE_PIN R18 [get_ports {BTN}]
set_property IOSTANDARD LVCMOS33 [get_ports {BTN}]


##LEDs
##IO_L23P_T3_35
set_property PACKAGE_PIN M14 [get_ports {LEDs[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {LEDs[0]}]

##IO_L23N_T3_35
set_property PACKAGE_PIN M15 [get_ports {LEDs[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {LEDs[1]}]

##IO_0_35
set_property PACKAGE_PIN G14 [get_ports {LEDs[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {LEDs[2]}]

##IO_L3N_T0_DQS_AD1N_35
set_property PACKAGE_PIN D18 [get_ports {LEDs[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {LEDs[3]}]


##Clock signal
##IO_L11P_T1_SRCC_35	
set_property PACKAGE_PIN L16 [get_ports Clk]
set_property IOSTANDARD LVCMOS33 [get_ports Clk]
create_clock -add -name sys_clk_pin -period 20.00 -waveform {0 8} [get_ports Clk]
