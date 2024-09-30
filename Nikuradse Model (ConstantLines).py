from Functions import *

#path to excel file with developed status of experiments
path = r'C:\Users\PipeFlow\Desktop\Research\20240830 Nikuradse Diagram\20240830\Fully Developed Experiments (8v).xlsx'
roughness = '8v'

constant = constant_lines(path, roughness)

#reynolds range
num = np.arange(100,31600,100)
num1 = np.arange(1200,31600,100)

#64/re line
lam = pd.DataFrame(num, columns=['Reynolds Number'])
lam['64/re'] = 64/lam['Reynolds Number']
lam = np.log10(lam)
lam = lam.set_index('Reynolds Number')

#Blasius line
tur = pd.DataFrame(num1, columns=['Reynolds Number'])
tur['blasius'] = .316/(tur['Reynolds Number']**.25)
tur = np.log10(tur)
tur = tur.set_index('Reynolds Number')

#adding nikuradse graph to subplot
plt.plot(constant['mean'], color = 'blue')
plt.plot(constant['hist'], color = 'orange')
plt.plot(tur)
plt.plot(lam)
plt.ylabel('Friction Factor')
plt.xlabel('Reynolds Number')
plt.grid()
plt.legend(['Mean', 'Histogram'])
plt.show()