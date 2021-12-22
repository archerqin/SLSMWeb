## 需求

0. 帐号
    - User
        - username
        - password
        - authority(与position联动,但可以独立增删)
            - super admin
            - admin
        - position

1. 线上版本bug统计
    - bug分类
        - 时间（周、月）
        - 系统
        - 发现人（看下是否必要）
        - 作者（测试-跟进人）
        - 修改人
        - 版本
        - 严重程度
        - 影响范围
        - 进度（发布-待观察-关闭-修复）
    - 图表
2. 更新日志
    - bug内容可导入
    - 生成可复制的内容（或者复制链接）
<!-- 3. 策划占用配置表格功能 -->

3. 用例规则
    - 层级
        - 0级 总纲 superclass 
        - 1级 具体系统 system
        - 2级 具体功能 function
        - 3级 详细条目 step
    - 其他
        - 配置 config
        - 
    - 数据库
        - step
            - id 唯一
            - class_id 根据不同层级（0~2）的id进行组合，用于精确定位
            - precondition 前置条件
            - operation
            - result
            - pass/fail
            - relation
            - author
            - description
        - function
            - id 唯一
            - relation
            - summary
            - 
        - system
            - id 唯一
            - summary
        - superclass
            - id 唯一
            - summary

    - ID 系统id_序列id
    - 系统名称 系统_二级系统
    - 

[20210907]
- [x] 插入bug信息modal框git
- [] 服务器写入modal中的数据
- [] bug信息列表页
- ? modal框出现在遮罩下方
    - 临时解决办法，先不显示backdrop遮罩
- ? modal框没有显示title和content
- ? modal框位置与重定位
[20210908]
- [x] modal title与body字体为白色
    - navbar字体白色，不能嵌套在其下
- [x] centos7蓝云机安装python3.8.11，附带pip3
- [] 蓝云机配置pip的host
- [] 脚本执行
    - [] 异步方式
    - [] 输出重定向
    - [] 动态增加的页签，可手动关闭
    - [] 执行完成后自动存盘并列出列表
[20211124]
- [] 测试用例wiki
    - [] 通过tag归类
    - [] 通过tag联想检索

## 最优先需求
DL20211209
- [] bug信息基础显示
    - [] 列表显示
    - [] 动态顶部插入
    - [] 分页
DL20211212
- [] 网页执行脚本
    - [] 队列
    - [] 输入、输出
    - [] 多线程
- 
- 

#问题
- [x] redirect无法跳转
    - ajax返回数据后将执行sucess部分，所以应该在sucess中执行重定向
- [] 增加pagination后footer移位重叠到最上方的原因
