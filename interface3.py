
# coding: utf-8

# In[22]:


from tkinter import *
from tkinter.ttk import Combobox
import pandas as pd
import numpy as np
import networkx as nx
from math import*
from sklearn.cluster import SpectralClustering
class MyWindow:
    def __init__(self, win):
        self.lbl1=Label(win, text='Enter complex number')
        
        self.lbl3=Label(win, text='Result')
        self.t1=Entry(bd=3)
        
        self.var = StringVar()
        self.var.set("one")
        self.data=('Biogrid','Collins', 'DIP', 'Krogan14K','Krogan2006core')
        self.cb=Combobox(win, values=self.data)
        self.cb.place(x=60, y=150)

        self.t3=Entry()
        self.btn1 = Button(win, text='process')
        
        self.lbl1.place(x=70, y=50)
        self.t1.place(x=200, y=50)
        
        self.b1=Button(win, text='Compute', command=self.add)#.grid(row = 40, column = 1)
        
        self.b1.place(x=300, y=150)
        
        self.lbl3.place(x=100, y=200)
        self.t3.place(x=200, y=200)
    def add(self):
        
        num1=int(self.t1.get())
        
        data_path = self.cb.get()
        embs = pd.read_csv('database/'+data_path+'/'+data_path+'_tadw.csv').set_index('id')
        emb_np = embs.to_numpy()
   
        network = nx.Graph()
        with open('database/'+data_path+'/'+data_path+'.txt') as f:
          edges = f.readlines()
        for line in edges:
          x,y = line.split()
          network.add_edge(x,y)
        print(len(network.edges))


        id_to_pro = {}
        pro_to_id = {}
        i = 0
        for n in network.nodes:
            pro_to_id[n] = i
            id_to_pro[i] = n
            i= i+1



        def square_rooted(x):

           return round((sum([a*a for a in x])),3)

        def cosine_similarity(x,y):

         numerator = sum(a*b for a,b in zip(x,y))
         denominator = square_rooted(x)*square_rooted(y)
         return round(numerator/float(denominator),3)

        sim_matrix = np.zeros((len(network.nodes),len(network.nodes)))
        for n1 in network.nodes:
            for n2 in network.nodes:
                sim_matrix[pro_to_id[n1]][pro_to_id[n2]] = cosine_similarity(emb_np[pro_to_id[n1]],emb_np[pro_to_id[n2]])

        clustering = SpectralClustering(n_clusters = num1,random_state=0).fit(sim_matrix)#assign_labels="discretize",
        labels = clustering.labels_
        predicted_complex = []
        for i in range(num1):
            predicted_complex.append([])
        for i in range(len(labels)):
            predicted_complex[labels[i]].append(i)
        new_complex = []
        for i in range(10):
            if len(predicted_complex[i])>= 3:
                new_complex.append(predicted_complex[i])


        new_complex2 = []
        for nc in new_complex:
            nc2 = []
            for j in nc:
                nc2.append(id_to_pro[j])
            new_complex2.append(nc2)

        with open(data_path+'Complex.txt', 'w') as f:
            for item in new_complex2:
                f.write("%s\n" % item)
            
        result = 'process completed'
        self.t3.insert(END, str(result))
    
window=Tk()
mywin=MyWindow(window)
window.title('SC_TADW')
window.geometry("400x300+10+10")
window.mainloop()

