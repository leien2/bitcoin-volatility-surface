import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

def plot_volatility_surface(input_file, output_file):
    """
    绘制波动率三维曲面图，直接连接相邻数据点
    """
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
        
        # 创建图表对象
        fig = go.Figure()
        
        # 添加原始数据点
        fig.add_trace(go.Scatter3d(
            x=df['strike'],
            y=df['dte'],
            z=df['mark_iv'],
            mode='markers',
            marker=dict(size=4, color='red', opacity=0.8),
            name='Data Point'
        ))
        
        # 按到期日分组，连接相同到期日的不同行权价的点
        for dte, group in df.groupby('dte'):
            # 按行权价排序
            group = group.sort_values('strike')
            fig.add_trace(go.Scatter3d(
                x=group['strike'],
                y=group['dte'],
                z=group['mark_iv'],
                mode='lines',
                line=dict(color='blue', width=2),
                opacity=0.6,
                name=f'DTE={dte}days'
            ))
        
        # 按行权价分组，连接相同行权价的不同到期日的点
        for strike, group in df.groupby('strike'):
            # 按到期日排序
            group = group.sort_values('dte')
            fig.add_trace(go.Scatter3d(
                x=group['strike'],
                y=group['dte'],
                z=group['mark_iv'],
                mode='lines',
                line=dict(color='green', width=2),
                opacity=0.6,
                name=f'K={strike}'
            ))
        
        # 更新布局
        fig.update_layout(
            title='Bitcoin Options Volatility Surface (Point-line connection)',
            scene=dict(
                xaxis_title='Strike Price',
                yaxis_title='DTE',
                zaxis_title='IV',
                camera=dict(
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=2, y=2, z=1.5)
                )
            ),
            width=1200,
            height=900,
            showlegend=False  # 隐藏图例以避免过多条目
        )

        # 保存和显示图表
        fig.write_html(output_file)
        fig.show()
        
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