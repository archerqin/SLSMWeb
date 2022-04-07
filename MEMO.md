[git]
git add .
git commit -m '20220313'
git push

[venv]
python -m venv xxxenv

[pip]
pip freeze >requirements.txt
pip install -r requirements.txt


[sqlalchemy]




|类型名	|Python类型	|说 明|
|----- |----- |-----|
Integer	int	普通整数,一般是 32 位
SmallInteger	int	取值范围小的整数,一般是 16 位
BigInteger	int 或 long	不限制精度的整数
Float	float	浮点数
Numeric	decimal.Decimal	定点数
String	str	变长字符串
Text	str	变长字符串,对较长或不限长度的字符串做了优化
Unicode	unicode	变长 Unicode 字符串
UnicodeText	unicode	变长 Unicode 字符串,对较长或不限长度的字符串做了优化
Boolean	bool	布尔值
Date	datetime.date	日期
Time	datetime.time	时间
DateTime	datetime.datetime	日期和时间
Interval	datetime.timedelta	时间间隔
Enum	str	一组字符串
PickleType	任何 Python 对象	自动使用 Pickle 序列化
LargeBinary	str	二进制文件


[config]
https://www.cnblogs.com/lab-zj/p/12612487.html

[sync]
https://www.jianshu.com/p/8f2fa6f10496
https://www.cnblogs.com/liyongsan/p/11039551.html Celery

在form下添加<button>元素，点击会刷新本页

input text关掉记忆autocomplete="off"
不能把click事件直接绑定到a标签上

ajax动态生成的元素无法绑定click，需要将时间委托到body或父元素，等事件冒泡到父元素再处理

ajax获取cookie
$.cookie()

[pandoc]
python模块，将markdown转为doc

[material_icons]
https://fonts.google.com/icons?selected=Material+Icons