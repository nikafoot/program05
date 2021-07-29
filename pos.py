import pandas as pd
import sys
import datetime
import eel

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price    

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_order_count=[]
        self.item_master=item_master

    def add_item_order(self,item_code,count):
        if self.get_item_data(item_code)[0]:
            self.item_order_list.append(item_code)
            self.item_order_count.append(count)
            return True
        else:
            return False
            
    #商品のコードから個数の確認
    def get_item_data(self,item_code):
        for s in self.item_master:
            if item_code == s.item_code:
                return s.item_name,s.price
        return None,None

    #合計金額の計算、会計
    def calculate_money(self):
        sum_price = 0
        for item_code,count in zip(self.item_order_list,self.item_order_count):
            for item in self.item_master:
                if item_code == item.item_code:
                    sum_price += item.price * count
        return sum_price

    def get_order_items(self):
        '''
        オーダーの全情報をテキストをして取得する
        '''
        res = ""
        num = 1
        total_price = 0
        total_count = 0
        for item_code,count in zip(self.item_order_list,self.item_order_count):
            for item in self.item_master:
                if item.item_code == item_code:
                    res += f"{num} | {item_code} {item.item_name} | ￥{item.price}円 × {count} 個\n"
                    num += 1
                    total_price += item.price * count
                    total_count += count
                    break   
        res += "---------------------------------------------\n"
        res += f"合計: ￥{total_price}円 | {total_count}個\n"
        
        return res

class PosSystem():
    def __init__(self,csv_path):
        self.item_master = []
        self.csv_path = csv_path
        self.order = None

#マスタ登録
    def add_item_master_by_csv(self):
        print("------- マスタ登録開始 ---------")
        count=0
        try:
            item_master_df=pd.read_csv(self.csv_path,dtype={"code":object}) # CSVでは先頭の0が削除されるためこれを保持するための設定
            for item_code,item_name,price in zip(list(item_master_df["code"]),list(item_master_df["name"]),list(item_master_df["price"])):
                self.item_master.append(Item(item_code,item_name,price))
                print("{}({}):{}円".format(item_name,item_code,price))
                count+=1
            print("{}品の登録を完了しました。".format(count))
            print("------- マスタ登録完了 ---------")
            return True
        except:
            print("マスタ登録が失敗しました")
            print("------- マスタ登録完了 ---------")
            return False

    def init_order(self):
        self.order = Order(self.item_master)