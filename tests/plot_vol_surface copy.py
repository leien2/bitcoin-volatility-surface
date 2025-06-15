import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

def plot_volatility_surface(input_file, output_file):

    try:
        # 获取当前日期
        today = pd.Timestamp.now()
        
        # 读取数据
        df = pd.read_csv(input_file)
        
        # 数据预处理：只选择看涨期权
        df = df[df['option_type'] == 'call']
        
        # 转换数据类型
        df['strike'] = pd.to_numeric(df['strike'])
        df['mark_iv'] = pd.to_numeric(df['mark_iv'])
        df['expiry_date'] = pd.to_datetime(df['expiry_date'])
        
        # 计算DTE (Days To Expiry)
        df['dte'] = (df['expiry_date'] - today).dt.days
        
        # 获取所有唯一的 DTE 和 strike 值
        unique_dte = sorted(df['dte'].unique())
        unique_strike = sorted(df['strike'].unique())
        
        # 创建网格数据
        z_data = []
        for strike in unique_strike:
            row = []
            for dte in unique_dte:
                # 获取对应的波动率值
                iv = df[(df['dte'] == dte) & (df['strike'] == strike)]['mark_iv'].values
                if len(iv) > 0:
                    row.append(iv[0])
                else:
                    # 如果没有数据，使用 None 表示
                    row.append(None)
            z_data.append(row)
        
        # 创建 3D 波动率曲面图
        fig = go.Figure(data=[go.Surface(
            z=z_data,
            x=unique_dte,
            y=unique_strike,
            colorscale='Viridis',
            connectgaps=True,  # 连接相邻点
            opacity=0.8
        )])
        
        # 设置图表布局
        fig.update_layout(
            title='比特币期权波动率曲面',
            scene=dict(
                xaxis_title='到期天数 (DTE)',
                yaxis_title='行权价 (Strike)',
                zaxis_title='隐含波动率 (IV)',
            ),
            width=900,
            height=700,
            margin=dict(l=65, r=50, b=65, t=90),
        )
        
        # 保存图表
        fig.write_html(output_file)
        
        print(f"波动率曲面图已保存至: {output_file}")
        return True

    except Exception as e:
        print(f"绘制波动率曲面时出错: {e}")
        return False

if __name__ == "__main__":
    # 设置输入输出文件路径
    input_file = '../data/data/options_iv_data.csv'
    output_file = 'volatility_surface_lines.html'
    
    # 绘制波动率曲面
    plot_volatility_surface(input_file, output_file)