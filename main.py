from gfishnar import *
#------------------------------READ--------------------------------------------

yaml = YAML("input.yaml") #objet yaml qui contient comme attribut les parametres
Gcode = Gcode() #objet de la classe Gcode
gcode=Gcode.read(yaml.gcodepath) #methode qui lit le Gcode sort un str

#-----------------------------EXTRACT------------------------------------------

extract=extract()

X=extract.X(gcode)

Y=extract.Y(gcode)

layers=extract.layers(gcode)

G=extract.G(gcode)

sublayers=extract.sublayers(gcode)

end_index=extract.end(gcode)
#-----------------------------GENERATE-----------------------------------------
generate= Gen()

mod_G=generate.modG(G,sublayers,end_index)

Z=generate.Zcoord(X,Y,layers,end_index)

Coordinates=generate.coordinates(X,Y,Z)

min_dist=0.1 # A FAIRE SUR LE YAML
checked_coordinates=generate.distance(Coordinates,min_dist)

Fishnar_status=generate.status(mod_G)

#-----------------------------CALIBRATE----------------------------------------
calibrate=Calibrate()
X_init=60 #A FAIRE SUR LE YAML
Y_init=140
Z_init=40
X_trans=45
Y_trans=65
fishnar_coord=calibrate.fishcoord(checked_coordinates,mod_G,X_init,Y_init,Z_init,
                              X_trans,Y_trans)


