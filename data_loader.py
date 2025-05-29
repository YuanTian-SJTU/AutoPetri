# data_loader.py
# 用于加载和处理Excel数据的模块

import pandas as pd
import numpy as np
import matplotlib

# 设置matplotlib支持中文显示
def setup_chinese_font():
    """设置matplotlib支持中文显示"""
    try:
        # 尝试设置中文字体
        matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        print("已设置中文字体支持")
    except Exception as e:
        print(f"设置中文字体时出错: {e}")
        print("将使用默认字体，中文可能无法正确显示")

def load_data(file_path):
    """从Excel文件加载数据
    
    参数:
        file_path: Excel文件路径
        
    返回:
        nodes_df: 节点数据DataFrame
        edges_df: 连边数据DataFrame
        params_df: 参数数据DataFrame
    """
    print("正在读取Excel文件...")
    try:
        # 读取三个表格数据
        nodes_df = pd.read_excel(file_path, sheet_name=0)  # 第一个表格：节点数据
        edges_df = pd.read_excel(file_path, sheet_name=1)  # 第二个表格：连边数据
        params_df = pd.read_excel(file_path, sheet_name=2)  # 第三个表格：参数数据
        
        print("数据读取成功！")
        print(f"节点表格形状: {nodes_df.shape}")
        print(f"连边表格形状: {edges_df.shape}")
        print(f"参数表格形状: {params_df.shape}")
        
        # 显示表格的前几行数据
        print("\n节点表格前5行:")
        print(nodes_df.head())
        
        print("\n连边表格前5行:")
        print(edges_df.head())
        
        print("\n参数表格前5行:")
        print(params_df.head())
        
        return nodes_df, edges_df, params_df
        
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")
        return None, None, None