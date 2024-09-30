from Functions import *


#Calculating Values for the Stricklers Empirical Scaling Grapg
#----------------------------------------------------------2v
#path to excel file with developed status of experiments
path1 = r'C:\Users\PipeFlow\Desktop\Research\20240830 Nikuradse Diagram\20240913\Fully Developed Lists\Fully Developed Experiments (2v).xlsx'
roughness1 = '2v'
# Calculating Value for constant line
constantline1 = constant_lines(path1, roughness1)
constant1 = constantline1['Constant Mean']
rover1 = np.log10(2)
#----------------------------------------------------------2v
#path to excel file with developed status of experiments
path2 = r'C:\Users\PipeFlow\Desktop\Research\20240830 Nikuradse Diagram\20240913\Fully Developed Lists\Fully Developed Experiments (4v).xlsx'
roughness2 = '4v'
# Calculating Value for constant line
constantline2 = constant_lines(path2, roughness2)
constant2 = constantline2['Constant Mean']
rover2 = np.log10(4)
#----------------------------------------------------------2v
#path to excel file with developed status of experiments
path3 = r'C:\Users\PipeFlow\Desktop\Research\20240830 Nikuradse Diagram\20240913\Fully Developed Lists\Fully Developed Experiments (8v).xlsx'
roughness3 = '8v'
# Calculating Value for constant line
constantline3 = constant_lines(path3, roughness3)
constant3 = constantline3['Constant Mean']
rover3 = np.log10(8)


#Creating the dataframes for the roughness elements and Empirical line
Strickler = pd.DataFrame([{'Log(R/r)': rover1, 'Log(f)': constant1}, {'Log(R/r)': rover2, 'Log(f)': constant2}, {'Log(R/r)': rover3, 'Log(f)': constant3}]).set_index('Log(R/r)')
#Empirical = pd.DataFrame([{'Log(R/r)': rover3, 'Log(f)': constant3}, {'Log(R/r)': rover3-3, 'Log(f)': constant3+1}]).set_index('Log(R/r)')
Empirical = pd.DataFrame([{'Log(R/r)': rover1, 'Log(f)': constant1}, {'Log(R/r)': rover3+3, 'Log(f)': constant3-1}]).set_index('Log(R/r)')
print(Strickler)


#Calculating the slope for the roughness elements
x = Strickler.index
y = Strickler
slope_intercept = np.polyfit(x,y,1)
print(slope_intercept[0])



#graphing the constant values for the different roughnesses as well as the Strickler Imperical Scaling line
plt.scatter(Strickler.index[0], Strickler.iloc[0], label = 'R/r = 2v', color = 'cornflowerblue')
plt.scatter(Strickler.index[1], Strickler.iloc[1], label = 'R/r = 4v', color = 'blue')
plt.scatter(Strickler.index[2], Strickler.iloc[2], label = 'R/r = 8v', color = 'midnightblue')
plt.plot(Empirical, label = "m = -1/3", color = 'black')
plt.legend()
plt.grid()
plt.xlabel('Log(R/r)')
plt.ylabel('Log(f)')
plt.title("Stickler's Imperical Scaling")
plt.xlim(0, 1)
plt.ylim(-1.3, -1)
plt.show()
