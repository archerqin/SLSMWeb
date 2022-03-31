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
        - [] 作者（测试-跟进人）
        - 修改人
        - [] 版本
        - 严重程度
        - 影响范围
        - [] 进度（发布-待观察-关闭-修复）
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
- [x] 蓝云机配置pip的host
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

- [] bug信息基础显示
    - [] 列表显示
    - [] 分页
    - [] 信息同步到群组
    - [] 增加程序优化、策划修改等分类
    - [] 添加热更版本分组显示
    - [] 同步到redmine
    - [] 详情页可能需要处理为不可编辑的modal
- [] 增加任务系统
    - [] 主要功能为显示个人任务
    - [] 可以汇总bug、测试用例、checklist等

- [] 网页执行脚本
    - [] 队列
    - [] 输入、输出
    - [] 多线程
    - 
    - 
- [] checklist
    - [] 临时的检查列表,主要内容为配置、代码等
    - 
- [] 后续从配置拓展开始逐步增加测试用例的记录与生成

#问题
- [x] redirect无法跳转
    - ajax返回数据后将执行sucess部分，所以应该在success中执行重定向
- [] 增加pagination后footer移位重叠到最上方的原因
- [] form布局
- [] modal右侧滑轨
- [] modal出现位置调整
- 
- [x] $(this)总是获取到最后那个的问题
    - [] 可能是scripts.html内加载caseCommon.js导致的
    - [x] 先用$(event.target)替代
- [] 完成tab切换页面
- [x] db migrate Target database is not up to date
    - [x] 之前删除migration时没有同事删除db.sqlite3，导致version没有写入
- [x] deploy插入superadmin
- [] 增加case type选项
    - [x] modal
    - [] view
    - [] 前端
        - [x] 重新布局
        - [] 获取选中值$
         $("#select_yx").find("option:selected") 
- [] 设置case必须有内容validator
- [] 默认now的时间显示不对
- 
- 系统设置相关
- [] 人员
    - [x] 人员增加
        - [x] user-role 一对多关系
        - [x] modal
            - [x] 帐号名（gz0000）
            - [x] 姓名
            - [x] 默认密码
            - [x] 角色（多选）
            - [] 必填检查
    - [] 人员信息编辑
    - [x] 人员列表模版（根据角色分类）
- [] 增加版本号
- 
- [] 增加
- 
- [] 多数据库支持 --暂不考虑
    - [x] 方案1：不同项目不同数据库
    - [] 方案2：不同功能不同数据库
    - [] 多数据库如何分开init
    - 
    - flask db init --multidb
    - sqlalchemy.exc.InvalidRequestError: Mapper properties (i.e. deferred,column_property(), relationship(), etc.) must be declared as @declared_attr callables on declarative mixin classes.  For dataclass field() objects, use a lambda
- [] 分离model
- [] 新增wikiapp