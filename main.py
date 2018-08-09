from gfishnar import *
#------------------------------READ--------------------------------------------
yaml = YAML("input.yaml")
Gcode = Gcode() 
gcode=Gcode.read(yaml.gcodepath)
#-----------------------------EXTRACT------------------------------------------
extract=extract(gcode)  
#-----------------------------GENERATE-----------------------------------------
generate= Gen(extract.deck,yaml.deck)
#-----------------------------CALIBRATE----------------------------------------
calibrate=Calibrate(generate.deck,yaml.deck)
#-----------------------------WRITE--------------------------------------------
writer=write(generate.deck,calibrate.coord)

