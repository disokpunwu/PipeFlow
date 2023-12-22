# from Functions import *

# breakdown = pd.read_csv(r'C:\Users\PipeFlow\Desktop\Experiments\New\Valley\4v\ReScan1\PressureDropBreakdown.csv')
# print(breakdown)
# breakdown['experiment'] = breakdown['experiment'].astype('category')
# breakdown.describe(include='category')

# ax = sns.lmplot(x='reynolds', y='pdrop', hue='experiment', data=breakdown)
# ax.set_titles('Reynolds to Total Pressure Drop Relationship')
# ax.set_xlabels('Reynolds Number (Re)')
# ax.set_ylabels('Total Pressure Drop (mBar)')

# ax = sns.lmplot(x='reynolds', y='during', hue='experiment', data=breakdown)
# ax.set_titles('Reynolds to Pressure Drop Accross The Pipe')
# ax.set_xlabels('Reynolds Number (Re)')
# ax.set_ylabels('Pressure Drop In The Pipe (mBar)')

# ax = sns.lmplot(x='reynolds', y='before', hue='experiment', data=breakdown)
# ax.set_titles('Reynolds to Pressure Before the Entrance')
# ax.set_xlabels('Reynolds Number (Re)')
# ax.set_ylabels('Pressure Drop Before The Pipe (mBar)')

# ax = sns.lmplot(x='reynolds', y='after', hue='experiment', data=breakdown)
# ax.set_titles('Reynolds to Pressure After the Exit')
# ax.set_xlabels('Reynolds Number (Re)')
# ax.set_ylabels('Pressure Drop After The Pipe (mBar)')

# breakdown1 = breakdown.drop('experiment', axis='columns')
# corr = breakdown1.corr()
# print(corr)

# x = breakdown.reynolds.to_numpy() 
# y = breakdown.pdrop.to_numpy() 
# n = np.size(x) 
  
# x_mean = np.mean(x) 
# y_mean = np.mean(y) 
# x_mean,y_mean 
  
# Sxy = np.sum(x*y)- n*x_mean*y_mean 
# Sxx = np.sum(x*x)-n*x_mean*x_mean 
  
# b1 = (Sxy/Sxx) 
# b0 = y_mean-(b1)*x_mean 
# print( 'pdrop equation is y=', b1, b0)

# x = breakdown.reynolds.to_numpy() 
# y = breakdown.before.to_numpy() 
# n = np.size(x) 
  
# x_mean = np.mean(x) 
# y_mean = np.mean(y) 
# x_mean,y_mean 
  
# Sxy = np.sum(x*y)- n*x_mean*y_mean 
# Sxx = np.sum(x*x)-n*x_mean*x_mean 
  
# b1 = (Sxy/Sxx) 
# b0 = y_mean-(b1)*x_mean 
# print( 'before equation is y=', b1, b0)

# a = breakdown.reynolds.to_numpy() 
# b = breakdown.during.to_numpy() 
# c = np.size(a) 
  
# a_mean = np.mean(a) 
# b_mean = np.mean(b) 
# a_mean,b_mean 
  
# Sab = np.sum(a*b)- c*a_mean*b_mean 
# Saa = np.sum(a*a)-c*a_mean*a_mean 
  
# q1 = (Sab/Saa) 
# q0 = b_mean-(q1)*a_mean 
# print( 'during equation is y=', q1, q0)

# d = breakdown.reynolds.to_numpy() 
# e = breakdown.after.to_numpy() 
# f = np.size(d) 
  
# d_mean = np.mean(d) 
# e_mean = np.mean(e) 
# d_mean,e_mean 
  
# Sde = np.sum(d*e)- f*d_mean*e_mean 
# Sdd = np.sum(d*d)-f*d_mean*e_mean 
  
# d1 = (Sde/Sdd) 
# d0 = e_mean-(d1)*d_mean 
# print( 'after equation is y=', d1, d0)

# print('resistance = ',((breakdown.pdrop.mean()/breakdown.reynolds.mean())))

# plt.show()


from Functions import *

breakdown = pd.read_csv(r'C:\Users\PipeFlow\Desktop\Experiments\New\Valley\4v\ReScan2\PressureDropBreakdown.csv')
print(breakdown)


ax = sns.lmplot(x='reynolds', y='pdrop', data=breakdown)
ax.set_titles('Reynolds to Total Pressure Drop Relationship')
ax.set_xlabels('Reynolds Number (Re)')
ax.set_ylabels('Total Pressure Drop (mBar)')

ax = sns.lmplot(x='reynolds', y='during', data=breakdown)
ax.set_titles('Reynolds to Pressure Drop Accross The Pipe')
ax.set_xlabels('Reynolds Number (Re)')
ax.set_ylabels('Pressure Drop In The Pipe (mBar)')

ax = sns.lmplot(x='reynolds', y='before', data=breakdown)
ax.set_titles('Reynolds to Pressure Before the Entrance')
ax.set_xlabels('Reynolds Number (Re)')
ax.set_ylabels('Pressure Drop Before The Pipe (mBar)')

ax = sns.lmplot(x='reynolds', y='after', data=breakdown)
ax.set_titles('Reynolds to Pressure After the Exit')
ax.set_xlabels('Reynolds Number (Re)')
ax.set_ylabels('Pressure Drop After The Pipe (mBar)')

corr = breakdown.corr()
print(corr)

x = breakdown.reynolds.to_numpy() 
y = breakdown.pdrop.to_numpy() 
n = np.size(x) 
  
x_mean = np.mean(x) 
y_mean = np.mean(y) 
x_mean,y_mean 
  
Sxy = np.sum(x*y)- n*x_mean*y_mean 
Sxx = np.sum(x*x)-n*x_mean*x_mean 
  
b1 = (Sxy/Sxx) 
b0 = y_mean-(b1)*x_mean 
print( 'pdrop equation is y=', b1, b0)

x = breakdown.reynolds.to_numpy() 
y = breakdown.before.to_numpy() 
n = np.size(x) 
  
x_mean = np.mean(x) 
y_mean = np.mean(y) 
x_mean,y_mean 
  
Sxy = np.sum(x*y)- n*x_mean*y_mean 
Sxx = np.sum(x*x)-n*x_mean*x_mean 
  
b1 = (Sxy/Sxx) 
b0 = y_mean-(b1)*x_mean 
print( 'before equation is y=', b1, b0)

a = breakdown.reynolds.to_numpy() 
b = breakdown.during.to_numpy() 
c = np.size(a) 
  
a_mean = np.mean(a) 
b_mean = np.mean(b) 
a_mean,b_mean 
  
Sab = np.sum(a*b)- c*a_mean*b_mean 
Saa = np.sum(a*a)-c*a_mean*a_mean 
  
q1 = (Sab/Saa) 
q0 = b_mean-(q1)*a_mean 
print( 'during equation is y=', q1, q0)

d = breakdown.reynolds.to_numpy() 
e = breakdown.after.to_numpy() 
f = np.size(d) 
  
d_mean = np.mean(d) 
e_mean = np.mean(e) 
d_mean,e_mean 
  
Sde = np.sum(d*e)- f*d_mean*e_mean 
Sdd = np.sum(d*d)-f*d_mean*e_mean 
  
d1 = (Sde/Sdd) 
d0 = e_mean-(d1)*d_mean 
print( 'after equation is y=', d1, d0)

print('resistance = ',((breakdown.pdrop.mean()/breakdown.reynolds.mean())))

plt.show()