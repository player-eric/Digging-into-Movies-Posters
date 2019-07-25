import numpy as np

hist = np.loadtxt("C:/Users/X1 Yoga/Desktop/sim.txt")
cnn = np.loadtxt("C:/Users/X1 Yoga/Desktop/cnn.txt")

max1 = np.max(hist)
min1 = np.min([h for h in hist.reshape((-1,)) if h > 0])

max2 = np.max(cnn)
min2 = np.min([c for c in cnn.reshape((-1,)) if c > 0])

print(hist)
print("MAX = %f" % max1)
print("MIN = %f" % min1)

print(cnn)
print("MAX = %f" % max2)
print("MIN = %f" % min2)

min1_ = min1 - 0.001
min2_ = min2 - 0.001
np.fill_diagonal(hist, min1_)
np.fill_diagonal(cnn, min2_)
hist = (hist-min1_)/(max1-min1_)
cnn = (cnn-min2_)/(max2-min2_)

labels2=open("C:/Users/X1 Yoga/Desktop/labels.txt",'r')
labels = labels2
labels2=labels2.read().split('\n')

mat2=hist


mat=cnn

alpha=0.5 #color*(1-alpha)+figure*alpha
mat=np.array(mat)
# mat=(mat-np.min(mat))/(np.max(mat)-np.min(mat))
# mat2=(mat2-np.min(mat2))/(np.max(mat2)-np.min(mat2))
labels_=labels
labels2_=labels2

mat_new=mat.copy()

print(np.sum(mat_new==mat))

i=0
for name2 in labels2:
  for name1 in labels:
    if name2==name1.replace(".jpg",""):
      for name2_ in labels2_:
        for name1_ in labels_:
          if name2_==name1_.replace(".jpg",""):
            i=i+1
            #print('a:',mat_new[labels.index(name1),labels.index(name1_)])
            mat_new[labels.index(name1),labels.index(name1_)]=mat_new[labels.index(name1),labels.index(name1_)]*alpha+mat2[labels2.index(name2),labels2_.index(name2_)]*(1-alpha)
            mat_new[labels.index(name1_),labels.index(name1)]=mat_new[labels.index(name1_),labels.index(name1)]*alpha+mat2[labels2.index(name2_),labels2_.index(name2)]*(1-alpha)
            #print('b:',mat_new[labels.index(name1),labels.index(name1_)])

# print(i)
print(np.sum(mat_new==mat))
print(mat_new)
print("MAX = %f" % np.max(mat_new))
print("MIN = %f" % np.min([n for n in mat_new.reshape((-1,)) if n > 0]))
