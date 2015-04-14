from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
from flask import make_response
from flask import jsonify
from flask import abort
from flask import request
#导入ORM
from sqlalchemy import Column, String, Integer,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

app=Flask(__name__) 
auth = HTTPBasicAuth()
Base = declarative_base()

#MySQL启动
engine = create_engine('mysql+pymysql://root:@localhost:3306/youshi')
DBSession = sessionmaker(bind=engine)

#Model层
class Job(Base):
	__tablename__="ys_job"
	jid = Column(Integer, primary_key=True)
	title=Column(String(20))
	company=Column(String(20))
	job=Column(String(20))
	hire_date=Column(String(20))
	status=Column(Integer)
	money=Column(String(20))
	accept_number=Column(Integer)
	detail=Column(String(20))
	pay_way=Column(String(20))
	start_date=Column(String(20))
	end_date=Column(String(20))
	linkman=Column(String(20))


# class User(Base):
# 	__tablename__ ='ys_user'
# 	uid=Column(Integer,primary_key=True)
# 	username=Column(String(20))
# 	password=Column(String(20))
# 	reg_date=Column(String(20))
# 	reg_ip=Column(String(20))
# 	level=Column(String(20))

#========================================================================================
# /api/v1.0/job   
#            
#========================================================================================

#获取所有jobs
@app.route("/api/v1.0/job",methods=['GET'])
def get_all_jobs():
	session = DBSession()
	jobs=session.query(Job).all()
	d=dict()
	li=list()
	session.commit()	
	total=len(jobs)
	for job in jobs:
		li.append(_job_obj_to_dict_(job))
	return jsonify(dict({'total':total,'result':li}))

#获取指定id的job
@app.route("/api/v1.0/job/<int:job_id>",methods=['GET'])
def get_job(job_id):
	session = DBSession()
	try:
		job=session.query(Job).filter(Job.jid==job_id).one()
	except NoResultFound:
		abort(404)

	session.commit()	
	d=dict()
	if job is not None:
		return jsonify({"result":_job_obj_to_dict_(job)})

#删除指定ID的job
@app.route("/api/v1.0/job/<int:job_id>",methods=['DELETE'])
def del_job(job_id):
	session = DBSession()
	try:
		res=session.query(Job).filter(Job.jid==job_id).delete()
	except Exception:
		res=None
	session.commit()	
	if res is not None:
		if int(res) >0 :
			return jsonify({'result':'Opt Success'})
	return jsonify({'error':'can not delete a job '})	


#创建job
@app.route('/api/v1.0/job',methods=['POST'])
def cre_job():
	session = DBSession()
	#get job params  
	title=request.form.get('title','')
	company=request.form.get('company','')
	job=request.form.get('job','')
	hire_date=request.form.get('hire_date','')
	status=request.form.get('status','')
	money=request.form.get('money','')
	accept_number=request.form.get('accept_number','')
	detail=request.form.get('detail','')	
	pay_way=request.form.get('pay_way','')
	start_date=request.form.get('start_date','')
	end_date=request.form.get('end_date','')
	linkman=request.form.get('linkman','')
	#get a instance
	job=Job(title=title,company=company,job=job,hire_date=hire_date,\
			status=status,money=money,accept_number=accept_number,\
		detail=detail,pay_way=pay_way,start_date=start_date,end_date=end_date,linkman=linkman)
	try:
		session.add(job)
		session.commit()
		res="success"
	except Exception as e:
		# res=str(e)
		res='error'

	return jsonify({'result':res})

#更新job
@app.route('/api/v1.0/job/<int:job_id>',methods=['PUT'])
def upd_job(job_id):
	session = DBSession()

	title=request.form.get('title',None)
	company=request.form.get('company',None)
	job=request.form.get('job','Yeep')
	hire_date=request.form.get('hire_date',None)
	status=request.form.get('status',None)
	money=request.form.get('money',None)
	accept_number=request.form.get('accept_number',None)
	detail=request.form.get('detail',None)	
	pay_way=request.form.get('pay_way',None)
	start_date=request.form.get('start_date',None)
	end_date=request.form.get('end_date',None)
	linkman=request.form.get('linkman',None)
	job_update=dict()

	if title is not None:
		job_update['title']=title
	if company is not None:
		job_update['company']=company
	if job is not None:
		job_update['job']=job

	if 	hire_date is not None:
		job_update['hire_date']=hire_date
	if status is not None:
		job_update['status']=status
	if money is not None:
		job_update['money']=money
	if accept_number is not None:
		job_update['accept_number']=accept_number
	if detail is not None:
		job_update['detail']=detail
	if pay_way is not None:
		job_update['pay_way']=pay_way
	if start_date is not None:
		job_update['start_date']=start_date
	if end_date is not None:
		job_update['end_date']=end_date
	if linkman is not None:
		job_update['linkman']=linkman		
	#map((lamda x : job_update[x]=request.get(x) if x is not None ),request.form)											
	try:
		session.query(Job).filter(Job.jid==job_id).update(job_update)
		session.commit()
		res={"result":'update success'}
	except Exception as e:
		# res=str(e)
		res={"error":'update error'}

	return jsonify(res)

#=======================================Protected=======================================
@auth.get_password
def get_password(username):
    if username == 'ok':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Route Not found'}), 404)
#=======================================Private=======================================
def _job_obj_to_dict_(job):
	d=dict()
	d["jid"]=job.jid
	d["title"]=job.title
	d["company"]=job.company
	d["hire_date"]=job.hire_date
	d["status"]=job.status
	d["money"]=job.money
	d["accept_number"]=job.accept_number
	d["detail"]=job.detail
	d["pay_way"]=job.pay_way
	d["start_date"]=job.start_date
	d["linkman"]=job.linkman
	return d

if  __name__ =='__main__':
	app.run(debug=True)



