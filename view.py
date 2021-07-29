import eel
import desktop
from pos import PosSystem
import pos

app_name="html"
end_point="index.html"
size=(700,600)

EXP_CSV_PATH = "./menu.csv"

@eel.expose
def add_item_order(cord,count):
    global system
    if system.order == None:
        system.init_order()
    res = system.order.add_item_order(cord,int(count))
    if not res:
        eel.alertJs(f"『{cord}』は商品マスターに登録されていません")
    else:
        res_text = system.order.get_order_items()
        print(res_text)
        eel.view_order_js(res_text)

@eel.expose
def input_and_change_money(input_money):
    global system
    sum_price = system.order.calculate_money()
    change = int(input_money) - sum_price
    if change >= 0:
        eel.view_change_js("お釣り：￥{}".format(change))
        print("お釣り：￥{}".format(change))
    else:
        eel.view_change_js("お金が足りません、再度入力をお願いします")
        print("お金が足りません、再度入力をお願いします")
        


def init_pos_system():
    '''
    POSシステムの初期化処理
    '''
    global system # グローバル変数を使用する場合の宣言
    
    # POSシステムに商品マスタを登録
    system = PosSystem(EXP_CSV_PATH)
    system.add_item_master_by_csv() # CSVからマスタへ登録
    system.init_order()

init_pos_system()
desktop.start(app_name,end_point,size)

#@ eel.expose
#def kimetsu_search(word,csv_name):
#    search.kimetsu_search(word,csv_name)
    

#desktop.start(size=size,appName=app_name,endPoint=end_point)