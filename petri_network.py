# petri_network.py
# 用于构建和可视化Petri网络的模块

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

class PetriNet:
    def __init__(self, nodes_df, edges_df, params_df=None):
        """初始化Petri网络
        
        参数:
            nodes_df: 节点数据DataFrame
            edges_df: 连边数据DataFrame
            params_df: 参数数据DataFrame
        """
        self.nodes = nodes_df
        self.edges = edges_df
        self.params = params_df
        self.graph = nx.DiGraph()
        self.build_network()
    
    def build_network(self):
        """构建网络图"""
        # 添加节点
        for _, node in self.nodes.iterrows():
            node_id = node.iloc[0]  # 假设第一列是节点ID
            node_type = node.iloc[1] if len(node) > 1 else 'unknown'  # 假设第二列是节点类型
            node_attrs = {}
            
            # 添加其他节点属性
            for i, col in enumerate(self.nodes.columns[2:], 2):
                if i < len(node):
                    node_attrs[col] = node.iloc[i]
            
            self.graph.add_node(node_id, type=node_type, **node_attrs)
        
        # 添加边
        for _, edge in self.edges.iterrows():
            source = edge.iloc[0]  # 假设第一列是源节点
            target = edge.iloc[1]  # 假设第二列是目标节点
            edge_attrs = {}
            
            # 添加边属性
            for i, col in enumerate(self.edges.columns[2:], 2):
                if i < len(edge):
                    edge_attrs[col] = edge.iloc[i]
            
            self.graph.add_edge(source, target, **edge_attrs)
    
    def visualize(self, title="Petri网络可视化"):
        """可视化Petri网络
        
        参数:
            title: 图表标题
        """
        plt.figure(figsize=(15, 10))
        
        # 创建自定义节点位置布局，按照层级从左到右排列
        pos = {}
        
        # 获取节点层级信息
        level_3_nodes = []
        level_2_nodes = []
        level_1_nodes = []
        user_nodes = []
        
        for node, attrs in self.graph.nodes(data=True):
            # 根据节点属性确定层级
            # 假设节点有一个'level'属性，或者根据节点名称前缀判断
            node_name = str(node).lower()
            if '三级' in node_name or 'level3' in node_name or '3级' in node_name:
                level_3_nodes.append(node)
            elif '二级' in node_name or 'level2' in node_name or '2级' in node_name:
                level_2_nodes.append(node)
            elif '一级' in node_name or 'level1' in node_name or '1级' in node_name:
                level_1_nodes.append(node)
            elif '用户' in node_name or 'user' in node_name or 'customer' in node_name:
                user_nodes.append(node)
            # 如果没有明确标识，尝试根据连接关系判断
            else:
                # 默认放入一级节点，后续可以根据实际情况调整
                level_1_nodes.append(node)
        
        # 设置每个层级的x坐标
        x_level_3 = 0.1
        x_level_2 = 0.35
        x_level_1 = 0.6
        x_user = 0.85
        
        # 为每个层级的节点分配y坐标
        for i, node in enumerate(level_3_nodes):
            pos[node] = (x_level_3, 0.1 + 0.8 * i / max(1, len(level_3_nodes) - 1))
        
        for i, node in enumerate(level_2_nodes):
            pos[node] = (x_level_2, 0.1 + 0.8 * i / max(1, len(level_2_nodes) - 1))
        
        for i, node in enumerate(level_1_nodes):
            pos[node] = (x_level_1, 0.1 + 0.8 * i / max(1, len(level_1_nodes) - 1))
        
        for i, node in enumerate(user_nodes):
            pos[node] = (x_user, 0.1 + 0.8 * i / max(1, len(user_nodes) - 1))
        
        # 如果有节点没有被分配位置，使用spring_layout为它们分配位置
        unpositioned_nodes = [n for n in self.graph.nodes() if n not in pos]
        if unpositioned_nodes:
            temp_pos = nx.spring_layout(self.graph.subgraph(unpositioned_nodes), seed=42)
            for node, (x, y) in temp_pos.items():
                # 将这些节点放在中间位置
                pos[node] = (0.5, 0.1 + 0.8 * y)
        
        # 根据节点类型设置不同颜色
        node_colors = []
        node_types = []
        
        for node in self.graph.nodes():
            node_type = self.graph.nodes[node].get('type', 'unknown')
            if node_type == 'place':
                node_colors.append('skyblue')
                node_types.append('place')
            elif node_type == 'transition':
                node_colors.append('salmon')
                node_types.append('transition')
            else:
                node_colors.append('lightgray')
                node_types.append('unknown')
        
        # 绘制节点
        nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors, node_size=500)
        
        # 绘制边
        nx.draw_networkx_edges(self.graph, pos, arrows=True, arrowsize=15, width=1.5)
        
        # 添加边标签（运输时间）
        edge_labels = {}
        for u, v, data in self.graph.edges(data=True):
            if 'time' in data and data['time'] is not None:
                edge_labels[(u, v)] = f"{data['time']}h"
            else:
                edge_labels[(u, v)] = ""
        
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=8, font_family='SimHei')
        
        # 添加节点标签
        nx.draw_networkx_labels(self.graph, pos, font_size=10, font_family='SimHei')
        
        # 添加图例
        place_patch = mpatches.Patch(color='skyblue', label='库所(Place)')
        transition_patch = mpatches.Patch(color='salmon', label='变迁(Transition)')
        level_3_patch = mpatches.Patch(color='white', label='三级仓库')
        level_2_patch = mpatches.Patch(color='white', label='二级仓库')
        level_1_patch = mpatches.Patch(color='white', label='一级仓库')
        user_patch = mpatches.Patch(color='white', label='用户')
        
        plt.legend(handles=[place_patch, transition_patch, level_3_patch, level_2_patch, level_1_patch, user_patch])
        
        # 添加层级标签
        plt.text(x_level_3, 0.02, '三级仓库', fontsize=12, ha='center', fontfamily='SimHei')
        plt.text(x_level_2, 0.02, '二级仓库', fontsize=12, ha='center', fontfamily='SimHei')
        plt.text(x_level_1, 0.02, '一级仓库', fontsize=12, ha='center', fontfamily='SimHei')
        plt.text(x_user, 0.02, '用户', fontsize=12, ha='center', fontfamily='SimHei')
        
        plt.title(title, fontsize=15, fontfamily='SimHei')
        plt.axis('off')
        plt.tight_layout()
        plt.show()