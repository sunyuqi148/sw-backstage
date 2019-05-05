# ShareDDL - A Shared Deadline Manager (Backend)

### 简介

本仓库用于ShareDDL的后台服务器开发，以及部分产品开发计划及使用文档。

相关项目：

​	[ShareDDL总仓库](https://github.com/ktxlh/sw-gp4)

​	ShareDDL前端代码(undefined)	



### 用况图

**子系统1**：单人使用ShareDDL的主要用况

![use case1](https://github.com/sunyuqi148/sw-backstage/tree/master/data/image/UseCase1.jpg)

**子系统2**：团队DDL管理用况图

![use case2](https://github.com/sunyuqi148/sw-backstage/tree/master/data/image/UseCase2.jpg)

### 前后端API

前后端使用HTTP协议进行交互。具体地，前端提交POST请求，将请求数据以form形式发送给后端，并接收后端返回的JSON格式数据（content_type='application/json'）。

若需启动server进行测试，登录服务器，执行以下命令即可：
'''
$ cd sw-backstage/
$ git checkout master
$ sudo python3 app.py
'''


#### 账号管理子系统

##### register (tested):

	route: http://222.29.159.164:10006/register
	
	request: username, password
	
	response: 
	
		1. 若注册成功，返回信息: valid(=true)
	
		2. 若用户名或密码不合法，返回错误信息: valid(=false), info(字符串，错误信息)

##### login (tested)：

​	route: http://222.29.159.164:10006/login

​	request: username, password

​	response: 

​		1. 若登录成功，返回信息包含: valid(=true), list[task(id, owner_id, title, deadline, ...), ...]

​		2. 若登录失败，返回错误信息: valid(=false), info(字符串，错误信息)

##### logout (tested):

​	route: http://222.29.159.164:10006/logout

​	method: GET

​	response: 返回退出成功, valid(=true)

#### 任务管理子系统：

##### get_tasklist:

​	route: http://222.29.159.164:10006/get_tasklist

​	method: GET

​	response: valid(=True), list[task(id, owner_id, title, deadline, ...), ...]

##### add_task:

​	route: http://222.29.159.164:10006/addtask

​	request: title, deadline, description

​	response: valid, task_id

##### modify_task:

​	route: http://222.29.159.164:10006/modifytask

​	request: task_id, title(optional), deadline(optional), description(optional)

​	response: 若当前用户有权限修改此task, valid = true

​			 否则valid=false, info='Invalid task id'

##### delete_task:

​	route: http://222.29.159.164:10006/deletetask

​	request: task_id

​	response: 若当前用户有权限删除此task, valid=true

​			否则valid=false, info='Invalid task id'

##### finish_task:

​	route: http://222.29.159.164:10006/finishtask

​	request: task_id

​	response: 若当前用户有权限完成此task, valid=true

​			否则valid=false, info='Invalid task id'