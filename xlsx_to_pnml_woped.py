import pandas as pd
import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import hashlib

# id 规范化：只用英文、数字、下划线
def normalize_id(s):
    s = str(s)
    s = re.sub(r'[^a-zA-Z0-9_]', '_', s)
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', s):
        return s
    # fallback: hash
    return 'id_' + hashlib.md5(s.encode()).hexdigest()[:8]

# 读取 Excel
def read_excel():
    nodes_df = pd.read_excel('input.xlsx', sheet_name='节点输入')
    edges_df = pd.read_excel('input.xlsx', sheet_name='连边输入')
    demands_df = pd.read_excel('input.xlsx', sheet_name='需求输入')
    return nodes_df, edges_df, demands_df

# 创建 Woped 兼容的 PNML 根节点
def create_pnml_root():
    pnml = ET.Element('pnml')
    net = ET.SubElement(pnml, 'net', id='net1', type='http://www.pnml.org/version-2009/grammar/ptnet')
    return pnml, net

# 分层布局参数
LEVELS = ['三级', '二级', '一级', '用户']
LEVEL_X = {lvl: 100 + i*300 for i, lvl in enumerate(LEVELS)}
TRANSITION_X = LEVEL_X['用户'] + 300
Y_START = 100
Y_STEP = 120

# place分层布局
def add_places(net, nodes_df):
    level_nodes = {lvl: [] for lvl in LEVELS}
    for _, row in nodes_df.iterrows():
        lvl = str(row['等级']).strip()
        if lvl in level_nodes:
            level_nodes[lvl].append(row)
    place_y_map = {}
    place_x_map = {}
    node_pos_map = {}  # id -> (x, y)
    for lvl in LEVELS:
        nodes = level_nodes[lvl]
        for i, row in enumerate(nodes):
            pid = normalize_id(row['仓库名称'])
            x = LEVEL_X[lvl]
            y = Y_START + i * Y_STEP
            place_y_map[pid] = y
            place_x_map[pid] = x
            node_pos_map[pid] = (x, y)
            place = ET.SubElement(net, 'place', id=pid)
            name = ET.SubElement(place, 'name')
            text = ET.SubElement(name, 'text')
            text.text = str(row['仓库名称'])
            # 初始标记
            initial = str(row['存储数量']) if '存储数量' in row else '0'
            if initial and initial != 'nan':
                marking = ET.SubElement(place, 'initialMarking')
                text2 = ET.SubElement(marking, 'text')
                text2.text = initial
            # graphics
            graphics = ET.SubElement(place, 'graphics')
            ET.SubElement(graphics, 'position', x=str(x), y=str(y))
            # 新增：写入经度、纬度为自定义属性
            longitude = str(row['经度']) if '经度' in row else ''
            latitude = str(row['纬度']) if '纬度' in row else ''
            if longitude or latitude:
                attr = ET.SubElement(place, 'attribute', name='location')
                if longitude:
                    ET.SubElement(attr, 'longitude').text = longitude
                if latitude:
                    ET.SubElement(attr, 'latitude').text = latitude
    return place_y_map, place_x_map, node_pos_map

# transition放在用户层右侧，y与其用户仓库对齐
def add_transitions(net, demands_df, place_y_map, node_pos_map):
    for _, row in demands_df.iterrows():
        tid = normalize_id(row['任务名称'])
        user = normalize_id(row['仓库名称\n（用户）'])
        y = place_y_map.get(user, Y_START)
        x = TRANSITION_X
        node_pos_map[tid] = (x, y)
        transition = ET.SubElement(net, 'transition', id=tid)
        name = ET.SubElement(transition, 'name')
        text = ET.SubElement(name, 'text')
        text.text = str(row['任务名称'])
        # graphics
        graphics = ET.SubElement(transition, 'graphics')
        ET.SubElement(graphics, 'position', x=str(x), y=str(y))

# 修正：连边输入每条插入一个transition，生成两条arc
def add_edge_transitions_and_arcs(net, edges_df, place_y_map, place_x_map, node_pos_map):
    for idx, row in edges_df.iterrows():
        out_name = str(row['（出）仓库名称'])
        in_name = str(row['（入）仓库名称'])
        out_id = normalize_id(out_name)
        in_id = normalize_id(in_name)
        # transition id & name
        tid = f"trans_{out_id}_{in_id}"
        tlabel = f"运输_{out_name}_{in_name}"
        # transition 坐标：横向居中，纵坐标与出仓库一致
        x = (place_x_map.get(out_id, 100) + place_x_map.get(in_id, 100)) // 2
        y = place_y_map.get(out_id, Y_START)
        if out_id not in place_x_map or in_id not in place_x_map:
            print(f"[警告] 仓库名未找到: {out_name}({out_id}) 或 {in_name}({in_id})，transition坐标使用默认值")
        node_pos_map[tid] = (x, y)
        transition = ET.SubElement(net, 'transition', id=tid)
        name = ET.SubElement(transition, 'name')
        text = ET.SubElement(name, 'text')
        text.text = tlabel
        graphics = ET.SubElement(transition, 'graphics')
        ET.SubElement(graphics, 'position', x=str(x), y=str(y))
        # arc1: 出仓库→transition
        arc1 = ET.SubElement(net, 'arc', id=f"arc_{out_id}_{tid}", source=out_id, target=tid)
        add_arc_graphics(arc1, out_id, tid, node_pos_map)
        # arc2: transition→入仓库
        arc2 = ET.SubElement(net, 'arc', id=f"arc_{tid}_{in_id}", source=tid, target=in_id)
        add_arc_graphics(arc2, tid, in_id, node_pos_map)
        # inscription（可选）
        if '运输时间' in row:
            ins = ET.SubElement(arc2, 'inscription')
            text = ET.SubElement(ins, 'text')
            text.text = str(row['运输时间'])

# 需求输入的arc不变
def add_demand_arcs(net, demands_df, node_pos_map):
    for _, row in demands_df.iterrows():
        tid = normalize_id(row['任务名称'])
        user = normalize_id(row['仓库名称\n（用户）'])
        arc = ET.SubElement(net, 'arc', id=f"arc_{tid}_{user}", source=tid, target=user)
        add_arc_graphics(arc, tid, user, node_pos_map)
        # inscription（可选）
        if '糖豆数量' in row:
            ins = ET.SubElement(arc, 'inscription')
            text = ET.SubElement(ins, 'text')
            text.text = str(row['糖豆数量'])

def add_arc_graphics(arc, source_id, target_id, node_pos_map):
    graphics = ET.SubElement(arc, 'graphics')
    src = node_pos_map.get(source_id, (0, 0))
    tgt = node_pos_map.get(target_id, (0, 0))
    if source_id not in node_pos_map or target_id not in node_pos_map:
        print(f"[警告] arc端点未找到: {source_id} 或 {target_id}，使用(0,0)")
    ET.SubElement(graphics, 'position', x=str(src[0]), y=str(src[1]))
    ET.SubElement(graphics, 'position', x=str(tgt[0]), y=str(tgt[1]))

if __name__ == '__main__':
    nodes_df, edges_df, demands_df = read_excel()
    pnml, net = create_pnml_root()
    place_y_map, place_x_map, node_pos_map = add_places(net, nodes_df)
    add_transitions(net, demands_df, place_y_map, node_pos_map)
    add_edge_transitions_and_arcs(net, edges_df, place_y_map, place_x_map, node_pos_map)
    add_demand_arcs(net, demands_df, node_pos_map)
    # 格式化输出
    xml_str = ET.tostring(pnml, encoding='utf-8')
    dom = xml.dom.minidom.parseString(xml_str)
    with open('input_woped.pnml', 'w', encoding='utf-8') as f:
        f.write(dom.toprettyxml(indent='  '))
    print('已生成 input_woped.pnml (分层布局+标准Petri结构+正确连线，Woped 兼容)') 