import Image
import numpy as np
import math
import sys

def load_image(fileName):
	img=Image.open(fileName)
	img.load()
	data=np.asarray(img,dtype="int32")
	return data

def save_image(data,fileName):
	outputFileName=fileName.split(".")[0]+"_blur.jpg"
	img=Image.fromarray(np.asarray(np.clip(data,0,255),dtype="uint8"),"L")
	img.save(outputFileName)

def findGuassianValues(standardDeviation):
	x=[0 for i in range(5)]
	y=[0 for i in range(5)]
	for i in range(0,len(x)/2+1):
		guassian=(-1)*(i+1)**2
		guassian=guassian/float(2*standardDeviation**2)
		guassian=math.exp(guassian)
		guassian=guassian/math.sqrt(2.0*math.pi*standardDeviation**2)

		x[len(x)/2-i]=guassian
		x[len(x)/2+i]=guassian
		y[len(y)/2-i]=guassian
		y[len(y)/2+i]=guassian

	return [x,y]

def convolveHorizontal(data,x):
	total=sum(x)
	for j in range(0,len(data)):
		row=data[j]
		#print row
		row_list=[0 for i in range(len(row))]
		for i in range(0,len(row)):
			if i < len(x)/2 or i>len(row)-1 - len(x)/2:
				row_list[i]=row[i]
				continue
			# print row[i-len(x)/2:i+len(x)/2+1]
			row_list[i]=int(np.asscalar(np.correlate(np.array(x),row[i-len(x)/2:i+len(x)/2+1]))/float(total))
		#print row_list
		data[j]=np.array(row_list)

def convolveVertical(data,y):
	total=sum(y)
	data_copy=np.zeros(data.shape)
	
	columnLength=data.shape[0]
	for j in range(0,columnLength):
		if j < len(y)/2 or j > columnLength-1-len(y)/2:
			data_copy[j]=data[j]
			continue
		rows=data[j-len(y)/2:j+len(y)/2+1]
		row=np.zeros(rows.shape[1])
			
		for i in range(0,len(row)):
			mat=[A[i] for A in rows ]
			row[i]=np.asscalar(np.correlate(np.array(y),mat)/float(total))
		data_copy[j]=row
	data=data_copy

fileName="indiagate.jpg"
data=load_image(fileName)
if len(data.shape) > 2 :
	print " error : unable to process colour image "
	sys.exit(1)
standardDeviation=3.0
g_x,g_y=findGuassianValues(standardDeviation)

convolveHorizontal(data,g_x)
convolveVertical(data,g_y)
save_image(data,fileName)