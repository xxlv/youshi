#!/usr/bin/env python3
# -*- coding:utf-8 -*-

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

class User(Base):
	__tablename__ ='ys_user'
	uid=Column(Integer,primary_key=True)
	username=Column(String(20))
	password=Column(String(20))
	reg_date=Column(String(20))
	reg_ip=Column(String(20))
	level=Column(String(20))

#========================================================================================
# /api/v1.0/user   
#            
#========================================================================================

#获取所有users
@app.route("/api/v1.0/user",methods=['GET'])
def get_all_users():
	session = DBSession()
	users=session.query(User).all()
	d=dict()
	li=list()
	session.commit()	
	total=len(users)
	for user in users:
		li.append(_user_obj_to_dict_(user))
	return jsonify(dict({'total':total,'result':li}))


#获取指定id的user
@app.route("/api/v1.0/user/<int:user_id>",methods=['GET'])
def get_user(user_id):
	session = DBSession()
	try:
		user=session.query(User).filter(User.uid==user_id).one()
	except NoResultFound:
		abort(404)
	session.commit()

	d=dict()
	if user is not None:
		return jsonify({"result":_user_obj_to_dict_(user)})

#删除指定ID的user
@app.route("/api/v1.0/user/<int:user_id>",methods=['DELETE'])
def del_user(user_id):
	session = DBSession()
	try:
		res=session.query(User).filter(User.uid==user_id).delete()
	except Exception:
		res=None
	session.commit()	
	if res is not None:
		if int(res) >0 :
			return jsonify({'result':'Opt Success'})
	return jsonify({'error':'can not delete a user '})	


#创建user
@app.route('/api/v1.0/user',methods=['POST'])
def cre_user():
	session = DBSession()
	#get user params  
	username=request.form.get('username','')
	password=request.form.get('password','')
	reg_date=request.form.get('reg_date','')
	reg_ip=request.form.get('reg_ip','')
	level=request.form.get('level',1)
	#get a instance 
	user=User(username=username,password=password,reg_ip=reg_ip,reg_date=reg_date,level=level)
	try:
		session.add(user)
		session.commit()
		res="success"
	except Exception as e:
		# res=str(e)
		res='error'
	return jsonify({'result':res})

#更新user
@app.route('/api/v1.0/user/<int:user_id>',methods=['PUT'])
def upd_user(user_id):
	session = DBSession()
	username=request.form.get('username',None)
	password=request.form.get('password',None)
	reg_date=request.form.get('reg_date',None)
	reg_ip=request.form.get('reg_ip',None)
	level=request.form.get('level',None)
	
	#TEST
	return str(password)+str(level)
	user_update=dict()

	if username is not None:
		user_update['username']=username
	if password is not None:
		user_update['password']=password
	if reg_date is not None:
		user_update['reg_date']=reg_date
	if 	reg_ip is not None:
		user_update['reg_ip']=reg_ip
	if level is not None:
		user_update['level']=level

	if all(user_update):
		try:
			session.query(User).filter(User.uid==user_id).update(user_update)
			session.commit()
			res={"result":'update success'}
		except Exception as e:
			# res=str(e)
			res={"error":'update error'+str(e)}
	else:
		res={'error':'Null give in!'}		

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
def _user_obj_to_dict_(user):
	d=dict()
	d["uid"]=user.uid
	d["username"]=user.username
	d["password"]=user.password
	d["reg_date"]=user.reg_date
	d["reg_ip"]=user.reg_ip
	d["level"]=user.level
	return d

if  __name__ =='__main__':
	app.run(debug=True)



