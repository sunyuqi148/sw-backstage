wget https://222.29.159.164:10014/register --post-data="username=anny1&password=anny1&email_addr=gxlyxps@163.com" --no-check-certificate
wget https://222.29.159.164:10014/login --post-data="username=anny1&password=anny1" --no-check-certificate --save-cookies cookie-000
wget https://222.29.159.164:10014/create_task --no-check-certificate --load-cookies cookie-000 --post-data="title=task1&deadline='0001-02-03 04:05:06'"
wget https://222.29.159.164:10014/get_tasklist --no-check-certificate --load-cookies cookie-000

