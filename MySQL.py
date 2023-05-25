import pymysql
import os

#判断车辆类型
def car_type(ple_color,ple_license):
    if ple_color == '蓝色':
        p_type = '小汽车'
    elif ple_color == '绿色':
        p_type = '新能源汽车'
    elif ple_color == '黄色':
        if ple_license[-1] == '学':
            p_type = '教练车'
        else:
            p_type = '工程车'
    elif ple_color == '黑色':
        if ple_license[-1] == '港':
            p_type = '香港车辆'
        elif ple_license[-1] == '澳':
            p_type = '澳门车辆'
        elif ple_license[0]== "使":
            p_type = '使馆车辆'
        else:
             p_tupe = '领馆车辆'
    elif ple_color == '白色':
        if ple_license[0] == 'W':
            p_type = '武警车辆'
        else:
            p_type = '警车'
    else:
        p_type = '其他车辆'
    return p_type

# 制作字典
def make_ori(path):
    with open(file=path, mode='r', encoding='utf-8') as j:
        imfo = j.read().split()
    temp = []
    a = int(len(imfo) / 2)
    for i in range(a):
        result_ori = {}
        ple_color = imfo[(2 * i + 1)]
        ple_license = imfo[(2 * i)]
        result_ori['车牌'] = f"{ple_license}"
        result_ori['类型'] = f"{car_type(ple_color,ple_license)}"
        result_ori['颜色'] = f"{ple_color}"
        result_ori['车牌归属地']= f'{place(ple_license)}'
        temp.append(result_ori)
    # 删除重复的车牌数据
    result_list = list({dictionary['车牌']: dictionary for dictionary in temp }.values())

    return result_list

# 判断车辆归属地
def place(license):
    t = license[0]
    if t =="W":
        t= license[2]

    car_dict = {'京': '北京', '津': '天津', '沪': '上海', '渝': '重庆',
                 '蒙': '内蒙古', '新': '新疆', '藏': '西藏', '宁': '宁夏',
                 '桂': '广西', '港': '香港', '澳': '澳门', '黑': '黑龙江',
                 '吉': '吉林', '辽': '辽宁', '晋': '山西', '冀': '河北',
                 '青': '青海', '鲁': '山东', '豫': '河南', '苏': '江苏',
                 '皖': '安徽', '浙': '浙江', '闽': '福建', '赣': '江西',
                 '湘': '湖南', '鄂': '湖北', '粤': '广东', '琼': '海南',
                 '甘': '甘肃', '陕': '陕西', '贵': '贵林', '云': '云南',
                 '川': '四川','危':'危险品运输车','航':'机场专用车辆'}
    return car_dict[t]

# 查询数据库有多少条数据
def select_count():
    cur.execute("select count(*) from data")
    count_result = cur.fetchall()
    data.commit()
    return count_result

# 获取最大 id
def max_id():
    cur.execute("select max(id) from data")
    max_id = cur.fetchall()
    data.commit()
    a = max_id[0][0]
    if a :
        max_id=a
    else:
        max_id=0
    return max_id

# 向数据库插入数据
def insert(lit):
    for i in lit:
        count = max_id()+1
        car_license = i["车牌"]
        car_type = i["类型"]
        car_color = i['颜色']
        car_place = i['车牌归属地']
        sql = "insert into data values (%s,%s,%s,%s,%s)"
        param = (count, car_license, car_type, car_color,car_place)
        sql2 = "insert into temp values (%s,%s,%s,%s,%s)"
        param2 = (car_license, car_type, car_place,car_color,count)
        cur.execute(sql, param)
        cur.execute(sql2, param2)
        data.commit()
        count += 1


if __name__=='__main__':
    # 连接数据库
    data = pymysql.connect(host='localhost', user='root', password='164820', charset='utf8mb4', database='mydatabase')
    cur = data.cursor()  # 创建游标

    cur.execute('truncate table temp')
    data.commit()

    lit = make_ori('Temp2.txt')
    insert(lit)
    print(f'最大的id为: {max_id()}')

    # 删除所有表格数据。！！！写代码的时候用的，注意平时要注释掉这行代码！！！
    # cur.execute('truncate table data')
    # data.commit()

    # 执行 MySQL数据库代码，从数据库中删除重复项
    cur.execute('delete  FROM data WHERE id not IN ( SELECT tmp.mid FROM (select min(id) mid from data group by license) tmp );')
    cur.execute('delete  FROM temp WHERE id not IN ( SELECT tmp.mid FROM (select min(id) mid from temp group by license) tmp );')

    data.commit()

    # 查询数据库更新后有多少条数据
    last_count = select_count()[0][0]
    print(f'更新数据库后共有：{last_count} 条数据')

    cur.close()
    data.close()

