#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Grid
from pyecharts.charts import Scatter
from pyecharts.charts import Line
from pyecharts.charts import Map
from pyecharts.charts import EffectScatter
from pyecharts.globals import SymbolType
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('hurun.csv', encoding='gbk')
df_z = pd.read_csv('clear.csv', encoding='gbk')
df_zr = pd.read_csv('deal.csv', encoding='gbk')
df_s = pd.read_csv('with.csv', encoding='gbk')
df_st = pd.read_csv('way.csv', encoding='gbk')
regions_available_loaded = list(df.区域.dropna().unique())


# 2018年中国各省生活垃圾清运量
def bar_base() -> Bar:
    CO = (
        Bar()
            .add_xaxis(list(df.地区))
            .add_yaxis("生活垃圾清运量（万吨）", list(zip(list(df.地区), list(df.生活垃圾清运量))))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="2018年中国各省生活垃圾清运量", subtitle=""),
            toolbox_opts=opts.ToolboxOpts(),
            datazoom_opts=opts.DataZoomOpts(), )
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),

        )
    )
    return CO


bar_base().render('生活垃圾清运量.html')


# 2018年中国生活垃圾无害化处理量
def effectscatter_base() -> EffectScatter:
    c = (
        EffectScatter()
            .add_xaxis(list(df.地区))
            .add_yaxis("生活垃圾无害化处理量（万吨）", list(df.生活垃圾无害化处理量))
            .set_global_opts(title_opts=opts.TitleOpts(title="2018年中国各省生活垃圾无害化处理量"))
    )

    return c


effectscatter_base().render('生活垃圾无害化处理量.html')


# 2018年中国生活垃圾无害化处理率
def map_visualmap() -> Map:
    i = (
        Map()
            .add("生活垃圾无害化处理率（%）", zip(list(df.地区), list(df.生活垃圾无害化处理率)), "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title=" 2018年中国各省生活垃圾无害化处理率"),
            visualmap_opts=opts.VisualMapOpts(max_=100.0, min_=86.9, is_piecewise=True),
        )
    )
    return i


you = map_visualmap()
you.render('生活垃圾无害化处理率.html')


# 焚烧与填埋两种方式处理量对比
def line_base() -> Line:
   
    line = (
        Line()
        .add_xaxis(list(df.地区))
        .add_yaxis("填埋无害化处理量(万吨)", 
                   list(df.生活垃圾卫生填埋无害化处理量),
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),)
        .add_yaxis("焚烧无害化处理量(万吨)", 
                   list(df.生活垃圾卫生焚烧无害化处理量),
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="填埋和焚烧对比图"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-55)),
        )
           )
    
    return line
geting = line_base()
geting.render('焚烧与填埋两种方式对比图.html')


@app.route('/', methods=['GET'])
def get_out():
    data_str = df.to_html()

    regions_available = regions_available_loaded  # 下拉选单有内容
    title = '中国各省城市生活垃圾清运和处理情况分析'
    return render_template('view.html',
                           the_res=data_str,  # 表
                           the_title=title,
                           the_select_region=regions_available)


@app.route('/hurun', methods=['POST'])
def get_in() -> 'html':
    the_region = request.form["the_region_selected"]  ## 取得用户交互输入
    print(the_region)  ## 检查用户输入, 在后台

    dfs = df.query("区域=='{}'".format(the_region))  ## 使用df.query()方法. 按用户交互输入the_region过滤

    data_str = dfs.to_html()  # 数据产出dfs, 完成互动过滤呢

    regions_available = regions_available_loaded  # 下拉选单有内容
    title = '中国各省城市生活垃圾清运和处理情况分析'
    return render_template('view6.html',
                           the_res=data_str,
                           the_title=title,
                           the_select_region=regions_available,
                           )


@app.route('/clear', methods=['POST'])
def get_mo() -> 'html':
    with open("生活垃圾清运量.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())

    interactive_controls = ['生活垃圾清运量可视化']
    title = '中国各省城市生活垃圾清运和处理情况分析'
    data_str = df_z.to_html()
    return render_template('view2.html',
                           the_plot_all=plot_all,
                           the_title=title,
                           the_res=data_str,
                           the_select_region=interactive_controls,
                           )


@app.route('/deal', methods=['POST'])
def get_you() -> 'html':
    with open("生活垃圾无害化处理量.html", encoding="utf8", mode="r") as g:
        plot_all_1 = "".join(g.readlines())

    interactive_controls = ['生活垃圾无害化处理量可视化']
    title = '中国各省城市生活垃圾清运和处理情况分析'
    data_str = df_zr.to_html()
    return render_template('view3.html',
                           the_plot_all_1=plot_all_1,
                           the_title=title,
                           the_res=data_str,
                           the_select_region=interactive_controls,
                           )


@app.route('/with', methods=['POST'])
def get_xi() -> 'html':
    with open("生活垃圾无害化处理率.html", encoding="utf8", mode="r") as b:
        plot_all_2 = "".join(b.readlines())

    interactive_controls = ['生活垃圾无害化处理率可视化']
    title = '中国各省城市生活垃圾清运和处理情况分析'
    data_str = df_s.to_html()
    return render_template('view4.html',
                           the_plot_all_2=plot_all_2,
                           the_title=title,
                           the_res=data_str,
                           the_select_region=interactive_controls,
                           )


@app.route('/way', methods=['POST'])
def get_on() -> 'html':
    with open("焚烧与填埋两种方式对比图.html", encoding="utf8", mode="r") as k:
        plot_all_3 = "".join(k.readlines())

    interactive_controls = ['填埋和焚烧两种方式对比可视化']
    title = '中国各省城市生活垃圾清运和处理情况分析'
    data_str = df_st.to_html()
    return render_template('view5.html',
                           the_plot_all_3=plot_all_3,
                           the_title=title,
                           the_res=data_str,
                           the_select_region=interactive_controls,
                           )

if __name__ == '__main__':
    app.run(port = 1889)   # debug=True, 在py使用, 在ipynb不使用


# In[ ]:




