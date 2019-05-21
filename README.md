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

	route: https://222.29.159.164:10006/register
	
	request: username, password
	
	response: 
	
		1. 若注册成功，返回信息: valid(=true)
	
		2. 若用户名或密码不合法，返回错误信息: valid(=false), info(字符串，错误信息)

##### login (tested)：

​	route: https://222.29.159.164:10006/login

​	request: username, password

​	response: 

​		1. 若登录成功，返回信息包含: valid(=true), list[task(id, owner_id, title, deadline, ...), ...]

​		2. 若登录失败，返回错误信息: valid(=false), info(字符串，错误信息)

##### logout (tested):

​	route: https://222.29.159.164:10006/logout

​	method: GET

​	response: 返回退出成功, valid(=true)

##### update_user:

	route: https://222.29.159.164:10006/update_user

​	request: username, password, name, info

​	response: valid(=True)


#### 任务管理子系统：

##### get_task:

​	route: https://222.29.159.164:10006/get_task

​	method: GET

​	response: 若获取成功，{valid: true, task_id, title, create_time, finish_time, status, publicity, info}

			若获取失败，{valid: false, info}

##### get_tasklist:

​	route: https://222.29.159.164:10006/get_tasklist

​	method: GET

​	response: valid(=True), list[task(id, owner_id, title, deadline, ...), ...]

##### create_task:

​	route: https://222.29.159.164:10006/create_task

​	request: title, deadline, status(optional), publicity(optional), group_id(optional), info(optional)

​	response: {valid: true, task_id, title, create_time, finish_time, status, publicity, info}

##### update_task:

​	route: https://222.29.159.164:10006/update_task

​	request: task_id, title(optional), finish_time(optional), status(optional), publicity(optional), 

​	response: 若当前用户有权限修改此task, valid = true

​			 否则valid=false, info='Invalid task id'

##### delete_task:

​	route: https://222.29.159.164:10006/deletetask

​	request: task_id

​	response: 若当前用户有权限删除此task, valid=true

​			否则valid=false, info='Invalid task id'

##### finish_task:

​	route: https://222.29.159.164:10006/finishtask

​	request: task_id

​	response: 若当前用户有权限完成此task, valid=true

​			否则valid=false, info='Invalid task id'

##### get_friend_tasklist:

	route: https://222.29.159.164:10006/get_friend_tasklist

​	method: GET

​	response: {valid: true, friend task list: [task(task_id, title, create_time, finish_time, status, publicity, info), ...]}

##### get_group_tasklist:

	route: https://222.29.159.164:10006/get_group_tasklist

​	method: GET

​	response: {valid: true, group task list: [task(task_id, title, create_time, finish_time, status, publicity, info), ...]}


#### 小组管理子系统

##### get_group:

	route: https://222.29.159.164:10006/get_group
	
	method: GET
	
	response: 若获取成功，{valid: true, group_id, name, owner_id, info}
	
			若获取失败，{valid: false, info: 'Invalid group id'}

##### create_group:

	route: https://222.29.159.164:10006/create_group
	
	request: name, info(optional)
	
	response: {valid: true, group: group(group_id, name, owner_id, info)}
	
##### update_group:

	route: https://222.29.159.164:10006/update_group
	
	request: group_id, name(optional), owner_id(optional), info(optional)
	
	response: 若更新成功，{valid: true, group: group(group_id, name, owner_id, info)}
	
			否则valid=false, info

##### join_group:

	route: https://222.29.159.164:10006/join_group
	
	request: group_id
	
	response: 若加入成功，{valid: true}
	
			否则valid=false, info

##### quit_group:

	route: https://222.29.159.164:10006/quit_group
	
	request: group_id
	
	response: 若加入成功，{valid: true}
	
			否则valid=false, info
			
##### get_group_member:

	route: https://222.29.159.164:10006/get_group_member

​	method: GET

​	response: 若获取成功，{valid: true, member list: [user(username, name, info), ...]}

			若获取失败，{valid: false, info}
			
##### add_member:

	route: https://222.29.159.164:10006/add_member
	
	request: group_id, user_id
	
	response: 若添加成功，valid=true
			
			否则valid, info
	
##### delete_member:

	route: https://222.29.159.164:10006/delete_member
	
	request: group_id, user_id
	
	response: 若删除成功, valid=true
	
			否则valid, info

##### get_group_task:

	route: https://222.29.159.164:10006/get_group_task

​	method: GET

​	response: 若获取成功，{valid: true, task list: [task(task_id, title, create_time, finish_time, status, publicity, info), ...]}

			若获取失败，{valid: false, info}

##### get_group_tasklist:

	route: https://222.29.159.164:10006/get_group_tasklist
	
	method: GET
	
	response: {valid: true, 
			group task list: [task(task_id, title, create_time, finish_time, status, publicity, info), ...]}

##### create_group_task:

​	route: https://222.29.159.164:10006/create_group_task

​	request: title, deadline, status(optional), publicity(optional), group_id(optional), info(optional)

​	response: 若创建成功，{valid: true, task_id, title, create_time, finish_time, status, publicity, info}

			若创建失败，{valid: false, info}
			
##### update_group_task:

​	route: https://222.29.159.164:10006/update_group_task

​	request: task_id, group_id, title(optional), finish_time(optional),
			status(optional), publicity(optional), group_id(optional), info(optional)

​	response: 若创建成功，{valid: true}

			若创建失败，{valid: false, info}			
			
	备注：在本方法中，若当前用户为小组成员，则仅对status具有有效修改权限；
			若当前用户为组长，则对所有信息都有修改权限。
			
##### delete_group_task:

​	route: https://222.29.159.164:10006/delete_group_task

​	request: group_id, task_id

​	response: 若创建成功，{valid: true}

			若创建失败，{valid: false, info}
			
##### check_ownership:

	route: https://222.29.159.164:10006/check_ownership
	
	method: GET
	
	response: 若当前用户是组长，valid=true
	
			否则，valid=false
			
			
#### 好友管理子系统

##### add_friend:

	route: https://222.29.159.164:10006/add_friend
	
	request: friend_id
	
	response: valid=true
	
##### delete_friend:

	route: https://222.29.159.164:10006/delete_friend
	
	request: friend_id
	
	response: valid=true
	
##### get_friendlist:

	route: https://222.29.159.164:10006/get_friendlist
	
	method: GET
	
	response: {valid: true, friend list: [User(username, name, info), ...]}
	
##### get_friend_tasklist:

	route: https://222.29.159.164:10006/get_friend_tasklist

​	method: GET

​	response: {valid: true, friend task list: [task(task_id, title, create_time, finish_time, status, publicity, info), ...]}
