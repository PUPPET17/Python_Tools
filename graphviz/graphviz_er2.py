from graphviz import Digraph

# 指定支持中文的字体
font_name = 'Microsoft YaHei'

# SQL 语句
sql = """
CREATE TABLE `chat` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `yonghu_id` int(11) DEFAULT NULL COMMENT '提问用户',
  `chat_issue` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '问题',
  `issue_time` timestamp NULL DEFAULT NULL COMMENT '问题时间',
  `chat_reply` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '回复',
  `reply_time` timestamp NULL DEFAULT NULL COMMENT '回复时间',
  `zhuangtai_types` int(11) DEFAULT NULL COMMENT '状态',
  `chat_types` int(11) DEFAULT NULL COMMENT '数据类型',
  `insert_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='客服聊天'
"""

# 创建 Digraph 对象，使用 neato 布局引擎
dot = Digraph('ER', filename='er_diagram', engine='neato', comment='ER diagram of chat table')
dot.attr('node', fontname=font_name)
dot.attr('edge', arrowhead='normal', len='1.0')  # 尝试设置边的长度
dot.attr(overlap='false', sep='0.1')  # 尝试减少节点重叠和增加节点间距

# 添加表名节点，位于中心
dot.node('chat', 'chat', shape='box', fontname=font_name, fixedsize='true', width='1.5', height='0.5')

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
    dot.node(field_name, f'{field_name}\n{comment}', shape='ellipse', fontname=font_name)
    dot.edge('chat', field_name)

# 设置输出图像格式为PNG
dot.format = 'png'
# 渲染图形到文件（PNG格式），不自动打开查看
dot.render(view=False)