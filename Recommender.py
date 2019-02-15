import numpy as np
#import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import os.path

class CollaborativeFiltRecs:

    def __init__(self,K=12):
        self.K=K
    
    def user_user_filter(self,user,arr):
        corr_mat = np.corrcoef(np.concatenate((user,arr),axis = 1).T)[0:1,1:]
        corr_copy = np.nan_to_num(corr_mat,True)
        max_sim =[]
        best_n = 30
        
        for i in range(best_n):
            ind = np.argmax(corr_mat)
            if corr_mat[0,ind]<=0:
                break
            max_sim.append(ind)
            corr_mat[0,ind]  = float('-inf')

        preds = np.sum(arr[:,max_sim]*corr_copy[:,max_sim],axis=-1,keepdims=True)
        watch_filter = np.ones(preds.shape)
        watch_filter[user>0]=0
        preds = preds*watch_filter

        recommendations = []
        
        for i in range(self.K):
            ind = np.argmax(preds)
            recommendations.append(ind)
            preds[ind]  = 0
        
        return recommendations

    def item_item_filter(self,user,arr):
        corr_mat = np.nan_to_num(cosine_similarity(arr),False)
        user_rated_movies = []
        for i in range(user.shape[0]):
            if user[i,0]>0:
                user_rated_movies.append(i)
        preds = np.matmul(corr_mat[:,user_rated_movies],user[user_rated_movies,0:1])
        np.nan_to_num(preds,False)
        
        preds[user_rated_movies] = 0
        recommendations = []
        
        for i in range(self.K):
            ind = np.argmax(preds)
            recommendations.append(ind)
            preds[ind]  = 0
            
        return recommendations
    

class MatFactRecs:

    def __init__(self,arr,K=12,lf=19,iterations=150,alpha=0.03,gamma=0.009):
        self.arr = arr.T
        self.lf = lf
        self.K = K
        self.alpha = alpha
        self.gamma = gamma
        self.movies,self.users = arr.shape
        self.P = np.random.rand(self.users,self.lf)
        self.Q = np.random.rand(self.movies,self.lf)
        self.iterations = iterations
        self.P_copy = self.P
        self.Q_copy = self.Q
        self.arr_copy = self.arr
        self.online = False
        self.online_alpha = 0.3*self.alpha
        self.online_gamma = 0.3*self.gamma
        self.train_log = []
        self.online_log = []

    def offline_logs(self):
        for iteration, err in self.train_log:
            print("Iteration  = "+str(iteration)+"    Error = "+str(err))

    def online_logs(self):
        for iteration, err in self.online_log:
            print("Iteration  = "+str(iteration)+"    Error = "+str(err))

    def train(self):
        if( os.path.isfile('chkpt_P.csv.csv') and os.path.isfile('chkpt_Q.csv.csv') ):
            self.P = np.genfromtxt('chkpt_P.csv', delimiter=',')
            self.Q = np.genfromtxt('chkpt_Q.csv', delimiter=',')
        else:
            positive_samples = [(self.arr[i,j],i,j)
                                for i in range(self.users)
                                for j in range(self.movies)
                                if(self.arr[i,j]>0)]
            np.random.shuffle(positive_samples)
            self.train_log = []
            for i in range(self.iterations):
                self.grad_desc(positive_samples)
                if((i+1)%10==0):
                    self.train_log.append((i+1,self.get_mse()))
            np.savetxt("chkpt_P.csv", self.P, delimiter=",")
            np.savetxt("chkpt_Q.csv", self.Q, delimiter=",")            

    def grad_desc(self,samples):
        for rating,i,j in samples:
            pred = self.get_pred(i,j)
            e = rating - pred
            if self.online==False:
                self.P[i,:] += self.alpha*(self.Q[j,:]*e - self.gamma*np.absolute(self.P[i,:]))
                self.Q[j,:] += self.alpha*(self.P[i,:]*e - self.gamma*np.absolute(self.Q[j,:]))
            else:
                self.P_copy[i,:] += self.online_alpha*(self.Q_copy[j,:]*e - self.online_gamma*np.absolute(self.P_copy[i,:]))
                self.Q_copy[j,:] += self.online_alpha*(self.P_copy[i,:]*e - self.online_gamma*np.absolute(self.Q_copy[j,:]))

    def get_pred(self,i,j):
        if self.online==False:
            pred = np.matmul(self.P[i,:],self.Q[j,:].T)
            return pred
        else:
            pred = np.matmul(self.P_copy[i,:],self.Q_copy[j,:].T)
            return pred                

    def get_pred_mat(self):
        if self.online==False:
            pred = np.matmul(self.P,self.Q.T)
            return pred
        else:
            pred = np.matmul(self.P_copy,self.Q_copy.T)
            return pred

    def get_mse(self):
        if self.online == False:
            positives =  [(i,j) for i in range(self.users)
                                for j in range(self.movies)
                                if(self.arr[i,j]>0)]
            preds = self.get_pred_mat()
            error = 0
            for i,j in positives:
                error += (self.arr[i,j]-preds[i,j])**2
            return error
        else:
            positives =  [(i,j) for i in range(self.users+1)
                                for j in range(self.movies)
                                if(self.arr_copy[i,j]>0)]
            preds = self.get_pred_mat()
            error = 0
            for i,j in positives:
                error += (self.arr_copy[i,j]-preds[i,j])**2
            return error

    def get_recs(self,user_marked):
        preds = self.get_pred_mat()
        recs = []
        inds = np.argsort(preds[0,:])[::-1]
        for i in inds:
            if i not in user_marked:
                recs.append(i)
            if len(recs)==self.K:
                break
        return recs

    def get_user_pred(self,user):
        self.arr_copy = np.concatenate((user.T,self.arr),axis = 0)
        self.P_copy = np.concatenate((np.mean(self.P,axis=0,keepdims=True),self.P),axis=0)
        self.Q_copy  = self.Q
        self.online = True
        ind  = np.argmax(user)
        user_favs = np.argsort(user,axis=0)[self.movies-self.K:]
        train_samples =  [(self.arr_copy[i,j],i,int(j))
                            for j in range(self.movies)
                            for i in range(self.users+1)
                            if(self.arr_copy[i,j]>0)]
        np.random.shuffle(train_samples)
        for i in range(int(len(train_samples)*.3)):
            if train_samples[i][1]!=0:
                del train_samples[i]
        self.online_log=[]
        for i in range(int(self.iterations*(4/15.))):
            self.grad_desc(train_samples)
            if((i+1)%10==0):
                self.online_log.append((i+1,self.get_mse()))
        recs = self.get_recs(user_favs)
        self.online = False
        return recs
        
##if __name__ == '__main__':
##    dbcon = MongoCon()
##    mat = dbcon.build_matrix()
##    a = dbcon.get_k_random()
##    print dbcon.fetch_records(a)
##    collabFilt = CollaborativeFiltRecs()
##    factRec = MatFactRecs(mat[:,1:])
##    recs_u  = collabFilt.user_user_filter(mat[:,0:1],mat[:,1:])
##    recs_i = collabFilt.item_item_filter(mat[:,0:1],mat[:,1:])
##    factRec.train()
##    recs_mf = factRec.get_user_pred(mat[:,0:1])
##    for i in range(12):
##        print str(recs_mf[i])+":::"+str(recs_i[i])+":::"+str(recs_u[i])
##    #factRec.offline_logs()
##    #factRec.online_logs()
    












        
