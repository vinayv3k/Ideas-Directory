from pymongo import MongoClient
from flask import Flask,render_template,request, session
import smtplib
from bson import ObjectId
import random,math

dbclient=MongoClient('mongodb+srv://krishnareddy:reddy123@ideas.mpxy2kv.mongodb.net/?retryWrites=true&w=majority')

db=dbclient['mongodb']
c=db['ideas']
s=db['submissions']
ad=db['admin']
ac=db['accept']
fa=db['favourites']

app=Flask(__name__)
app.secret_key='50000'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/adhome',methods=['get','post'])
def adminhome():
    return render_template('admin.html')

@app.route('/logout',methods=['get','post'])
def home3():
    return render_template('home.html')

@app.route('/home1',methods=['get','post'])
def home1():
    return render_template('home1.html')

@app.route('/reg',methods=['get','post'])
def register():
    return render_template('register.html')

@app.route('/log',methods=['get','post'])
def log():
    return render_template('login.html')

@app.route('/admin',methods=['get','post'])
def re():
    return render_template('adlog.html')

@app.route('/uhome',methods=['get','post'])
def uhome():
    return render_template('uhome.html',name=session['name'])


@app.route('/adlog',methods=['get','post'])
def adlog():
    name=request.form['name']
    password=request.form['password']
    key=request.form['key']
    res=ad.find()
    for i in res:
        x=dict(i)
        if(name==x['name'] and password==x['password'] and key==x['key']):
            return render_template('admin.html')
    else:
        return render_template('adlog.html',status='credentials are incorrect😥')

@app.route('/home',methods=['post','get'])
def hom():
    return render_template('home.html')

@app.route('/uhome',methods=['get','post'])
def userhome():
    return render_template('uhome.html')

@app.route('/idea',methods=['get','post'])
def idea():
    return render_template('ideassub.html')

@app.route('/id',methods=['post','get'])
def id():
    name=session['name']
    title=request.form['title']
    domain=request.form['domain']
    desc=request.form['desc']
    k={}
    k['name']=name
    k['title']=title
    k['domain']=domain
    k['desc']=desc

    res=c.find()
    for i in res:
        x=dict(i)
        if(name==x['users']):
            email=x['email']
            server =smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login('krish79939@gmail.com','cjcjsxjelypwchwi')
            server.sendmail('krishna reddy',email,'Congratulations your idea has been successfully submitted.Kindly wait for the return mail for the status of acceptance of your idea.Thankyou')
    s.insert_one(k)
    return render_template('ideassub.html',status='Your idea has been submitted.Please check your  mail for further details')

@app.route('/register',methods=['post','get'])
def reg():
    usernam=request.form['username']
    college=request.form['college']
    year=request.form['year']
    password=request.form['password']
    rpass=request.form['rpass']
    number=request.form['number']
    email=request.form['email']
    k={}
    k['users']=usernam
    k['college']=college
    k['year']=year
    k['password']=password
    k['number']=number
    k['email']=email   
    res=c.find()
    for data in res:
        x=dict(data)
        if(x['users']==usernam):
            return render_template('register.html',res='Username already exists😐')
        if(x['email']==email):
         return render_template('register.html',res='Email already exists😐')
        if(password!=rpass):
            return render_template('register.html',res='Passwords do not match😫')
        if(len(password)<8):
            return render_template('register.html',res='Password should have atlest 8 characters😐')           
    else:
        c.insert_one(k)
        return render_template('register.html',reg='Registration successful😀')

@app.route('/login',methods=['post','get'])
def login():
    user=request.form['reddy']
    password=request.form['password']
    flag=0
    res=c.find()
    for x in res:
        i=dict(x)
        if(user==i['users'] and password==i['password']):
            session['name']=user
            flag=1
            break
    if(flag==1):
        print(session['name'])
        return render_template('uhome.html')
    else:
        return render_template('login.html',status='User does not exist or wrong password😥')


@app.route('/adreg',methods=['get','post'])
def adreg():
    return render_template('adreg.html')

@app.route('/regi',methods=['get','post'])
def regi():
    name=request.form['name']
    password=request.form['password']
    key=request.form['key']
    r={}
    r['name']=name
    r['password']=password
    r['key']=key
    ad.insert_one(r)
    return render_template('adreg.html')

@app.route('/submit',methods=['get','post'])
def submit():
    res=s.find()
    for i in res:
        x=dict(i)
        print(x)
        return render_template('adlog.html',title=x['title'],domain=x['domain'],desc=x['desc'])

@app.route('/ideas',methods=['get','post'])
def ideas():
    data1=s.find()
    data2=c.find()
    data2=list(data2)
    return render_template('submissions.html',data=data1,data2=data2)

@app.route('/iaccept',methods=['get','post'])
def accept():
    i={}
    i['_id']=ObjectId( request.args.get('id'))
    data2=s.find_one(i)
    data2=dict(data2)
    data2['likes']=0
    data2['liked']=[]
    data2['liked'].append('krishna')
    ac.insert_one(data2)
    s.delete_one(i)
    print(data2)
    data2=dict(data2)
    print(data2['name'])
    res=c.find()
    for i in res:
        x=dict(i)
        if(x['users']==data2['name']):
            mail=x['email']
            print(mail)
            server =smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login('krish79939@gmail.com','cjcjsxjelypwchwi')
            server.sendmail('krishna reddy',mail,'Congratulations your idea has been successfully accepted.')
    data1=s.find()  
    data2=c.find()
    data2=list(data2)
    return render_template('submissions.html',data=data1,data2=data2)


@app.route('/cancel',methods=['get','post'])
def cancel():
      i={}
      i['_id']=ObjectId( request.args.get('id'))
      data3=s.find_one(i)
      s.delete_one(i)
      find=dict(data3)
      print(find['name'])
      res=c.find()
      for j in res:
        x=dict(j)
        if(x['users']==find['name']):
            gmail=x['email']
            server =smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login('krish79939@gmail.com','cjcjsxjelypwchwi')
            server.sendmail('krishna reddy',gmail,'Sorry,your idea has been denied by us.come up up woth a better idea next time')
      data=s.find()
      data2=c.find()
      data2=list(data2)
      return render_template('submissions.html',data=data,data2=data2)

@app.route('/myideas',methods=['get','post'])
def myideas():
    res=ac.find()
    myid=[]
    for i in res:
        x=dict(i)
        myideas={}
        if(x['name']==session['name']):
            myideas['name']=x['name']
            myideas['title']=x['title']
            myideas['domain']=x['domain']
            myideas['desc']=x['desc']
            myid.append(myideas)
    return render_template('myidea.html',data=myid)


@app.route('/succ',methods=['get','post'])
def accepted():
    data=ac.find()
    data=list(data)
    data2=c.find()
    data2=list(data2)
    return render_template('ideas.html',data=data,data2=data2)

@app.route('/succ1',methods=['get','post'])
def accepted1():
    data=ac.find()    
    data=list(data)
    data2=c.find()
    data2=list(data2)
    return render_template('uideas.html',data=data,data2=data2)

@app.route('/succ2',methods=['get','post'])
def accepted2():
    data=ac.find()    
    data2=c.find()
    data2=list(data2)
    return render_template('adideas.html',data=data,data2=data2)

@app.route('/filter',methods=['get','post'])
def filter():
    dom=request.form['dom']
    res=s.find()
    myid=[]
    for i in res:
        x=dict(i)
        if(x['domain']==dom):
            myid.append(i)
    data2=c.find()
    data2=list(data2)
    return render_template('submissions.html',data=myid,data2=data2) 

@app.route('/ifilter',methods=['get','post'])
def ifilter():
    dom=request.form['dom']
    res=ac.find()
    myid=[]
    for i in res:
        x=dict(i)
        if(x['domain']==dom):
            myid.append(i)
    
    data2=c.find()
    data2=list(data2)
    return render_template('ideas.html',data=myid,data2=data2)

@app.route('/forgot',methods=['get','post'])
def otphome():
    return render_template('forgot1.html')

@app.route('/forgot1',methods=['get','post'])
def otpver():
    mail=request.form['email']
    session['gmail']=mail
    digits="0123456789"
    OTP=""
    for i in range(6):
        OTP+=digits[math.floor(random.random()*10)]
    msg='Your OTP Verification for app is '+OTP+' Note..  Please enter otp within 2 minutes and 3 attempts, otherwise it becomes invalid'
    session['otp']=OTP
    msg='Your OTP Verification for app is '+OTP+' Note..  Please enter otp within 2 minutes and 3 attempts, otherwise it becomes invalid'
    server =smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('krish79939@gmail.com','cjcjsxjelypwchwi')
    server.sendmail('krishna reddy',mail,msg)
    return render_template('otp.html')
 
@app.route('/forget',methods=['get','post'])    
def forgot():
    otp1=request.form['otp']
    if(otp1!=session['otp']):
        return render_template('otp.html',status='Please enter correct otp😐')
    else:
        return render_template('forget2.html')

@app.route('/newpass',methods=['get','post'])
def newpass():
    passwor=request.form['pass']
    rpass=request.form['rpass']
    if(passwor!=rpass):
        return render_template('forget2.html',status='passwords do not match😥')
    else:
        res=c.find()
        for z in res:
            y=dict(z)
            if(y['email']==session['gmail']):
                o=y['password']
                old={"password":o}
                new={ "$set": {"password":passwor}}
                c.update_one(old,new)
    return render_template('login.html',status='Your password has been successfully updated')

@app.route('/fav',methods=['get','post'])
def fav():
    data2={}
    i={}
    i['_id']=ObjectId( request.args.get('id'))
    data1=ac.find_one(i)
    print(data1)
    data2['user']=session['name']
    digits="0123456789"
    OTP=""
    for i in range(6):
        OTP+=digits[math.floor(random.random()*10)]
    data2['_id']=OTP
    data2['title']=data1['title']
    data2['domain']=data1['domain']
    data2['desc']=data1['desc']
    data2['name']=data1['name']
    print(OTP)
    print(data2)
    res=fa.find()
    for x in res:
        v=dict(x)
        if(v['user']==session['name'] and v['title']==data2['title']):
            data=ac.find()
            return render_template('uideas.html',data=data,status="Already added to favourites")
    fa.insert_one(data2)
    data=ac.find()
    return render_template('uideas.html',data=data,status="Added to favourites❤")

@app.route('/favs',methods=['get','post'])
def favs():
    data1=[]
    data=fa.find()
    print(data)
    for i in data:
        x=dict(i)
        if(x['user']==session['name']):
            data1.append(x)
    print(data1)
    data=ac.find()
    data=list(data)
    data2=c.find()
    data2=list(data2)
    return render_template('favourites.html',data=data1,data2=data2)

@app.route('/ufilter',methods=['get','post'])
def ufilter():
    dom=request.form['dom']
    res=ac.find()
    myid=[]
    for i in res:
        x=dict(i)
        if(x['domain']==dom):
            myid.append(i)
    data2=c.find()
    data2=list(data2)
    return render_template('uideas1.html',data=myid,data2=data2)

@app.route('/myfilter',methods=['get','post'])
def myfilter():
    dom=request.form['dom']
    res=fa.find()
    myid=[]
    for i in res:
        x=dict(i)
        if(x['domain']==dom and x['name']==session['name']):
            myid.append(i)
    return render_template('myidea.html',data=myid)

@app.route('/like',methods=['get','post'])
def like():
    a={}
    a['_id']=ObjectId(request.args.get('id'))
    z=a['_id']
    data1=ac.find_one(a)
    print(data1,'hii')
    x=data1['liked']
    print(x)
    flag=0
    for i in x:
        if(i==session['name']):
            flag=1
            break
    if flag==0:
        ac.update_one({"_id":z} ,{"$push": { "liked": session['name'] }} )
        ac.update_one({'_id':z},{"$inc":{'likes':+1}})
    else:
        ac.update_one({"_id":z} ,{"$pull": { "liked": session['name'] }} )
        ac.update_one({'_id':z},{"$inc":{'likes':-1}})            
    data=ac.find()
    data=list(data)
    data2=c.find()
    data2=list(data2)
    return render_template('uideas.html',data=data,data2=data2)



if __name__=="__main__":
    app.run(debug=True)

    

