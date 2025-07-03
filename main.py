import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib
import matplotlib.font_manager as fm



font_path = "站酷文艺体.TTF"
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
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 绘制第一个Y轴的数据
    if chart_type == "折线图":
        ax1.plot(data[x_column], data[y_columns[0]], color='tab:blue', label=y_columns[0])
    elif chart_type == "柱状图":
        ax1.bar(data[x_column], data[y_columns[0]], color='tab:blue', label=y_columns[0])
    elif chart_type == "散点图":
        ax1.scatter(data[x_column], data[y_columns[0]], color='tab:blue', label=y_columns[0])

    ax1.set_xlabel(x_column)
    ax1.set_ylabel(y_columns[0], color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # 创建第二个Y轴
    ax2 = ax1.twinx()
    if chart_type == "折线图":
        ax2.plot(data[x_column], data[y_columns[1]], color='tab:orange', label=y_columns[1])
    elif chart_type == "柱状图":
        ax2.bar(data[x_column], data[y_columns[1]], color='tab:orange', label=y_columns[1])
    elif chart_type == "散点图":
        ax2.scatter(data[x_column], data[y_columns[1]], color='tab:orange', label=y_columns[1])

    ax2.set_ylabel(y_columns[1], color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # 如果有更多Y轴
    if len(y_columns) > 2:
        ax3 = ax1.twinx()
        ax3.spines['right'].set_position(('outward', 60))  # 偏移第三个Y轴
        if chart_type == "折线图":
            ax3.plot(data[x_column], data[y_columns[2]], color='tab:green', label=y_columns[2])
        elif chart_type == "柱状图":
            ax3.bar(data[x_column], data[y_columns[2]], color='tab:green', label=y_columns[2])
        elif chart_type == "散点图":
            ax3.scatter(data[x_column], data[y_columns[2]], color='tab:green', label=y_columns[2])

        ax3.set_ylabel(y_columns[2], color='tab:green')
        ax3.tick_params(axis='y', labelcolor='tab:green')

    # 设置图表标题
    plt.title(f'多Y轴图表: {x_column} vs ' + ' & '.join(y_columns))

    # 竖向显示X轴标签并调整对齐方式
    plt.xticks(rotation=90, ha='right')

    # 使用 fig.autofmt_xdate() 来确保日期或标签格式正确
    fig.autofmt_xdate(rotation=90)

    # 调整布局以避免标签被遮挡
    plt.subplots_adjust(bottom=0.15)

    fig.tight_layout()  # 防止Y轴标签重叠
    st.pyplot(fig)

# Streamlit UI
def main():
    st.title("Excel 数据分析工具 - 多Y轴图表")

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
