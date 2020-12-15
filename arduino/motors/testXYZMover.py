from xyzMover import XYZMover
import time

print ("++++ Testing XYZMover +++++")

aMover=XYZMover(8820)
print (aMover.estimatedPosition())
print (aMover.status())

#print ("++++ Moving to 20,25 +++++")
#print (aMover.moveAbsolute(-1,'x'))
#print (aMover.moveAbsolute(175,'y'))
#print (aMover.moveAbsolute(-1,'z'))
#print (aMover.estimatedPosition())
#print (aMover.moveAbsolute(295,'x'))
#print (aMover.moveAbsolute(175,'y'))
#print (aMover.moveAbsolute(10,'z'))
#print (aMover.estimatedPosition())
#print (aMover.status())
#print ("++++ Done +++++")
#
#print ("++++ Moving 100,30 out of bounds +++++")
#print (aMover.moveAbsoluteXYZ(20,30,10))
#print (aMover.estimatedPosition())
#print ("++++ Done +++++")


