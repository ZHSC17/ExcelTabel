import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib
import matplotlib.font_manager as fm
from itertools import cycle
import os



font_path = os.path.join(os.path.dirname(__file__), "站酷文艺体.TTF")
if not os.path.exists(font_path):
    st.warning("⚠️ 中文字体文件未找到，图表可能无法正确显示中文")
else:
    my_font = fm.FontProperties(fname=font_path)
# 设置支持中文的字体
matplotlib.rcParams['font.family'] = my_font.get_name()
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题

# 读取Excel文件
def load_data(file):
    try:
        data = pd.read_excel(file)
        return data
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# 绘制带有多个Y轴的图表
def plot_multiple_y_axes(data, x_column, y_columns, chart_type):
    fig, host = plt.subplots(figsize=(10, 6))
    colors = plt.cm.tab10.colors
    color_cycle = cycle(colors)

    axes = [host]
    host.set_xlabel(x_column)
    host.set_ylabel(y_columns[0], color=colors[0])
    host.tick_params(axis='y', labelcolor=colors[0])

    # 画第一个Y轴
    color = next(color_cycle)
    if chart_type == "折线图":
        host.plot(data[x_column], data[y_columns[0]], color=color, label=y_columns[0])
    elif chart_type == "柱状图":
        host.bar(data[x_column], data[y_columns[0]], color=color, label=y_columns[0])
    elif chart_type == "散点图":
        host.scatter(data[x_column], data[y_columns[0]], color=color, label=y_columns[0])

    # 创建其他 Y 轴
    for i in range(1, len(y_columns)):
        ax_new = host.twinx()
        ax_new.spines["right"].set_position(("outward", 60 * (i - 1)))  # 右边依次错开
        axes.append(ax_new)

        color = next(color_cycle)
        if chart_type == "折线图":
            ax_new.plot(data[x_column], data[y_columns[i]], color=color, label=y_columns[i])
        elif chart_type == "柱状图":
            ax_new.bar(data[x_column], data[y_columns[i]], color=color, label=y_columns[i])
        elif chart_type == "散点图":
            ax_new.scatter(data[x_column], data[y_columns[i]], color=color, label=y_columns[i])

        ax_new.set_ylabel(y_columns[i], color=color)
        ax_new.tick_params(axis='y', labelcolor=color)

    # 设置图表标题和布局
    plt.title(f'多Y轴图表: {x_column} vs ' + ' & '.join(y_columns) )
    plt.xticks(rotation=90, ha='right')
    fig.autofmt_xdate(rotation=90)
    plt.subplots_adjust(right=0.2 + 0.05 * (len(y_columns)-2))  # 自动调宽图表，避免轴标签被遮挡
    fig.tight_layout()
    st.pyplot(fig)

# Streamlit UI
def main():
    st.title("Excel 数据分析工具 - 多Y轴图表")
    st.text(f"已加载字体: {my_font.get_name()}")
    # 上传文件
    uploaded_file = st.file_uploader("上传你的Excel文件", type="xlsx")
    
    if uploaded_file is not None:
        # 加载数据
        data = load_data(uploaded_file)

        if data is not None:
            st.write("数据预览:", data.head())

            # 选择 X 轴列
            columns = data.columns.tolist()
            x_column = st.selectbox("选择X轴列", columns)

            # 选择多个 Y 轴列
            y_columns = st.multiselect("选择多个Y轴列", columns)

            # 选择图表类型
            chart_type = st.selectbox("选择图表类型", ["折线图", "柱状图", "散点图"])

            if len(y_columns) > 0 and st.button("生成图表"):
                plot_multiple_y_axes(data, x_column, y_columns, chart_type)

if __name__ == "__main__":
    main()
