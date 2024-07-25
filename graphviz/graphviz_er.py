from graphviz import Digraph

# 指定支持中文的字体
font_name = 'Microsoft YaHei'
font_size = '20'

# SQL 语句
sql = """
CREATE TABLE `yonghu` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '账户',
  `password` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '密码',
  `yonghu_name` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '用户姓名',
  `yonghu_photo` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '头像',
  `sex_types` int(11) DEFAULT NULL COMMENT '性别',
  `yonghu_phone` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '联系方式',
  `yonghu_id_number` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '身份证号 ',
  `yonghu_email` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '邮箱',
  `yonghu_delete` int(11) DEFAULT '1' COMMENT '逻辑删除',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='用户'
"""

# 创建 Digraph 对象，使用 circo 布局引擎
dot = Digraph('ER', filename='er_diagram', engine='circo', comment='ER diagram of chat table')
dot.attr('node', fontname=font_name)
dot.attr('edge', arrowhead='normal')

# 添加表名节点，位于中心
dot.node('yonghu', 'yonghu', shape='box', fontname=font_name ,fontSize=font_size )

# 解析 SQL 语句并添加字段节点
for line in sql.splitlines():
    line = line.strip().strip(',').strip(')').strip('(')
    if not line or line.upper().startswith('CREATE') or line.upper().startswith('PRIMARY KEY') or line.upper().startswith(') ENGINE'):
        continue
    
    parts = line.split("`")
    if len(parts) < 2:
        continue  # 跳过无法正确解析的行
    
    field_name = parts[1]  # 使用反引号分割以准确提取字段名
    comment_index = line.upper().find('COMMENT')
    if comment_index == -1:
        continue  # 如果没有 COMMENT 关键字，则跳过
    
    comment = line[comment_index:].split("COMMENT")[1].strip().strip("'").strip('"')
    
    # 添加字段节点和连接到表的边，指定字体
    dot.node(field_name, f'{field_name}\n{comment}', shape='ellipse', fontname=font_name,fontSize=font_size)
    # 确保箭头从表节点指向字段节点
    dot.edge('yonghu', field_name)

# 设置输出图像格式为PNG
dot.format = 'png'
# 渲染图形到文件（PNG格式），不自动打开查看
dot.render(view=False)