
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# Assuming the data is collected uniformly with time and the input data frame has only two columns (independent,dependent)

class Hyst():

    def __init__(self,data:pd.DataFrame,window_length:int = 30 ,factor:int = 7):
        data.columns = ['x','y']
        self.x = data.x.values
        self.y = data.y.values
        self.window_length = window_length
        self.factor = factor
        self.diff = np.abs(np.diff(data.y.values)) 
        self.change_points = self.detect_change_points() 


    def detect_change_points(self)->list[int]:

        threshold = max(self.diff)/self.factor
        indices = [] 
        for change in self.diff:
            if change >=threshold:
                ind = np.where(self.diff == change)[0]
                window =self.y[ind[0]: ind[0] + self.window_length]
                if np.all(window >= self.y[ind]):
                    if len(indices) !=0:
                      if abs(indices[-1] - ind) > self.window_length:
                          indices.append(ind[0])
                    else:
                        indices.append(ind[0]) 
                elif np.all(window <= self.y[ind]):
                    if len(indices) !=0:
                      if abs(indices[-1] - ind) > self.window_length:
                          indices.append(ind[0])
                    else:
                        indices.append(ind[0])
        return indices 


    def plot_direction_curve(self,plot_change_points:bool,n:int = 20,width = 0.003,headwidth =4,headlength= 6,scale=15,color:str= 'blue'):
        dx = np.gradient(self.x)
        dy = np.gradient(self.y)
        magnitude = np.sqrt(dx**2  + dy**2)
        dx = dx /magnitude
        dy = dy /magnitude
        plt.plot(self.x, self.y, label="Spiral", color='green')
        plt.quiver(self.x[::n], self.y[::n], dx[::n], dy[::n], angles="xy", scale_units="xy", scale=scale, width=width, headwidth=headwidth, headlength=headlength, color=color) 
       
        if plot_change_points:
            for change_point in self.change_points:
                plt.plot(self.x[change_point],self.y[change_point],'ro') 

        plt.title('Graph with direction')
        plt.grid(True)
        plt.show()





    def plot_curve(self,plot_change_points:bool):
        plt.plot(self.x,self.y)
        if plot_change_points:
            for change_point in self.change_points:
                plt.plot(self.x[change_point],self.y[change_point],'ro')
        plt.title("Plane X and Y Plot")
        plt.show()   




if __name__ == "__main__":
    data = pd.read_csv('./data/1 volt 7 cycle.csv')
    df = pd.DataFrame({"A":data.V.values,"B":data.I.values})
    model = Hyst(data=df)
    # model.plot_curve(plot_change_points=True)
    model.plot_direction_curve(plot_change_points=True) 

