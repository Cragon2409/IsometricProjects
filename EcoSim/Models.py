#this file contains the models of all entities, stored as an array of duples [rectangular prism argument, colour]
#where a rectangular prism is [x,y,z,width,depth,height]


#colour definitions
brown = [i*0.8 for i in (210,105,30)]
leafgreen = (97,138,61)
grassgreen = (44, 176, 55)
treeBrown = (103,77,49)
foxorange = (231,69,36)#(70,210,90)#
earorange = [i*0.9 for i in foxorange]
white = [255]*3
black = [0]*3

foxLi = [#fox array
([6.5,1,0.5,0.5,1,1],white),#tail white
([5,1,0.5,1.5,1,1],foxorange),#tail
([0,0.3,2,0.5,0.5,0.5],black),#leg 1
([4.5,0.3,2,0.5,0.5,0.5],black),#leg 2
([0,2.2,2,0.5,0.5,0.5],black),#leg 3
([4.5,2.2,2,0.5,0.5,0.5],black),#leg 4
([0, 0.3, 0, 5, 2.4, 2],earorange),#body
([-2,0.5,-1,2,2,1.8],foxorange),#head
([-1.5, 0.5, -1.4, 0.5, 0.5, 0.4],earorange),#ear 1
([-1.5, 0.5, -1.5, 0.5, 0.5, 0.1],white),#ear white 1
([-1.5, 2, -1.4, 0.5, 0.5, 0.4],earorange),#ear 2
([-1.5, 2, -1.5, 0.5, 0.5, 0.1],white),#ear white 2
([-2.5,1.25,0,0.6,0.5,0.5],foxorange),#snout
([-2.6,1.25,0,0.1,0.5,0.5],black),#snout tip
([-2,0.7,-0.5,0,0.5,0.5],black),#eye 1
([-2,1.8,-0.5,0,0.5,0.5],black),#eye 2
]
foxBaseRotation = 0.25#stores the base rotation of the model
foxAltOrder = [13,12, 14,15, 2,3,4,5, 7, 8,9,10,11, 6, 1,0]#stores the alternate ordering of the list viewed from the other side

rabbitLi = [#rabbit array
([2, 0.32, 0.33, 0.6, 1.37, 1.36], [255.0, 255.0, 255.0]),
([0, 1.5, 2, 0.5, 0.5, 0.5], [154.29, 68, 19.29]),
([1.46, 1.5, 2, 0.5, 0.5, 0.5], [154.29, 68, 19.29]),
([1.53, 0, 2, 0.5, 0.5, 0.5], [154.29, 68, 19.29]),
([0, 0, 2, 0.5, 0.5, 0.5], [154.29, 68, 19.29]),
([0, 0, 0, 2.01, 1.96, 2], [229.29, 222.86, 222.86]),
([-1.01, 0.16, -0.48, 0.98, 1.63, 1.6], [255.0, 255.0, 255.0]),
([-1.44, 0.39, -0.21, 0.41, 0.96, 0.91], [255.0, 255.0, 255.0]),
([-0.87, 1.22, -0.88, 0.49, 0.43, 0.37], [255.0, 216.43, 195.0]),
([-0.87, 0.23, -0.86, 0.47, 0.43, 0.37], [255.0, 216.43, 195.0]),
]
rabbitBaseRotation = 0.25#stores the base rotation of the model
rabbitAltOrder = [1,2,3,4,5,6,7,8,9,0]#stores the alternate ordering of the list viewed from the other side

grassLi = [
([2, 2, 0, 0.5, 0.5, 1.0], [60.0, 177.86, 17.14]),
([2, 0, 0.3, 0.5, 0.5, 0.7], [60.0, 130.71, 17.14]),
([0, 2, 0.2, 0.5, 0.5, 0.8], [60.0, 152.14, 17.14]),
([0, 0, 0.1, 0.5, 0.5, 0.9], [60.0, 192.86, 17.14])
]
grassBaseRotation = 0#stores the base rotation of the model
grassAltOrder = None#stores the alternate ordering, which is none

treeLi = [
([1, 0, 4, 3, 1, 1], [154.29, 68, 19.29]),
([3, 0, 3, 1, 1, 1], [23.57, 113.57, 42.86]),
([0, 0, 0, 1, 1, 8], [154.29, 68, 19.29]),
([-2, -2, -1, 5, 5, 1], [23.57, 113.57, 42.86]),
]
treeBaseRotation = 0#stores the base rotation of the model
treeAltOrder = None#stores the alternate ordering, which is none
