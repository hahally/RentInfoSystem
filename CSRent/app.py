from flask import Flask, render_template
from flask_socketio import SocketIO
from scripts import draw
from scripts import rent_analyse
from scripts import rentspider,rentspiderdemo


def run_spider():
    print("开始总程序")
    Filename = "./data/rent_info.csv"
    socketio.emit('analyse', {'data':"开始运行爬虫，请等待..."})
    rentspiderdemo.run()
    socketio.emit('analyse', {'data': "结束爬虫"})
    socketio.emit('analyse', {'data': "开始分析数据，请等待..."})
    all_list = rent_analyse.spark_analyse(Filename)
    socketio.emit('analyse', {'data': "结束分析数据"})
    socketio.emit('analyse', {'data': "开始绘图，请等待..."})
    draw.draw_bar(all_list)
    socketio.emit('analyse', {'data': "绘图结束"})
    print("结束总程序")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'xmudblab'
socketio = SocketIO(app)


# 客户端访问 http://127.0.0.1:5000/，可以看到index界面
@app.route("/")
def handle_mes():
    return render_template("index.html")


# 对客户端发来的start_spider事件作出相应
@socketio.on("start_spider")
def start_spider(message):
    print(message)
    run_spider()
    socketio.emit('get_result', {'data': "请获取最后结果"})


# 对客户端发来的/Get_result事件作出相应
@app.route("/Get_result")
def Get_result():
    return render_template("result.html")


if __name__ == '__main__':
    socketio.run(app, debug=True)
