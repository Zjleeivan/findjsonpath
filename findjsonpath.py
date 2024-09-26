import re

# 直接逆向解构文本串，能够解析大多数格式的 JSON 和 map 文本（包括尾部残缺、嵌套变异等文本）。
# 
# 功能: 
# 该函数从给定的 JSON 字符串中查找指定的 key 或 value，并返回其在 JSON 结构中的路径。
#
# 调用方式:
# findjsonpath(dictStr, deStr='\r\n', mode='value')
#
# 参数:
# dictStr : str
#     需解析的 JSON 文本字符串。
#
# deStr : str, optional
#     查找的 key 或 value（切片元素），默认为 '\r\n'。
#
# mode : str, optional
#     指定查找的对象是 key 还是 value。可选值为 'key' 或 'value'，默认为 'value'。
#
# 返回值:
# list
#     返回一个包含所有找到的路径的列表，如果是单个结果则为字符串，每个路径格式为 "路径索引:路径"。
def findjsonpath(dictStr,deStr='\r\n',mode='value')->list: 
    # 移除字符串中的所有空白字符
    dictStr=re.sub('[\s|\n|\r|\t]*','',dictStr,0,re.MULTILINE) 
    es=':' if mode=='key' else ''   # 根据模式选择冒号或空字符串
    ts=0  # 追踪字符串索引
    result_lst=[]  # 存储结果的列表
    while True:
        try:
           # 查找下一个deStr及其后续字符串
           ts=(dictStr+'\r\n').index(deStr+es,ts+1)+(len(deStr)+1)*len(es)
        except:
           break
        dstr=list(dictStr[0:ts])
        result=''
        while len(dstr)>0:
            a,m,h,f,key = 0,0,0,0,''      # 初始化计数器和key     
            #a=逗号出现次数(即数组下标),m=出现冒号,h=花括号配对,f=方括号配对,key=字典key
            while True:
                p=dstr.pop() #右边最后一个字符
                if p == ',' and f == 0 and h == 0 :a += 1 #逗号出现次数+1，嵌套括号内的逗号不统计
                if p == '}':h += 1  #花括号配对+1
                if p == ']':f += 1   #方括号配对+1
                if m == 1:   #出现过冒号
                    if a == 0  :key=p+key #组合key(遇到逗号终止)
                    if p == '{' : #遇到花括号
                        if h == 0: #当前字典起始点
                            a = 0 if a > 0 else 1
                            result='['+ key[a:]+']'+result
                            break  #返回字典key
                        h -= 1 #嵌套花括号-1
                if p == ':':m = 1 #遇到冒号设置m
                if p == '[' :#遇到方括号
                    if f == 0: #当前数组起始点
                        result='['+str(a)+']'+result
                        break  #返回数组下标
                    f -= 1  #嵌套方括号-1
        result_lst.append(result)    # 添加结果到列表
    #return result_lst
    # 返回格式化的结果列表
    return '\n'.join([str(i+1)+':'+path for i,path in enumerate(list(result_lst))])


if __name__ == '__main__':

    # 测试数据
    data = '''{"olapQueryParam": {"configs":[
        {"type":"field",
        "config":{"fields":[{"guid":"04d1d5aa-ce2b-4e1d-9cfb-40b88023c341","fid":"7ce5017bba","areaType":"column"},
        {"guid":"7c6e8436-c284-46c7-a9e6-b862c86c51a2","fid":"2e917274f1","areaType":"column"},
        {"guid":"be040e99-d8f8-416a-91e4-2f7819ad13e5","fid":"bd0bf4d4a9","areaType":"column"},
        {"guid":"7b306f32-72cc-40a3-8c0c-ff5ee052606f","fid":"098a1855d6","areaType":"column"},
        {"guid":"0c7b68e4-d643-483e-a590-d25e2f0e57ee","fid":"b5dc826bdf","areaType":"column"},
        {"guid":"af313989-9b79-47b4-8be3-d8c6c1a8b430","fid":"aa0ea414e2","areaType":"column"},
        {"guid":"915cb029-e457-432a-bb08-a0fb749d73da","fid":&&"5c51a799db","areaType":"column"},
        {"guid":"d66a1ba0-e6f9-43cd-be91-41b27241b6cc","fid":"6f6d8510f1","areaType":"column"},
        {"guid":"6ae2e5d2-d7f9-4e68-b8a3-75ea5fbe2dfd","fid":"5310afe88c","areaType":"column"},
        {"guid":"12806b0f-0279-44e8-a165-429872c95c91","fid":"0780e19823","areaType":"column"}]},"cubeId":"db2ae6c9-0548-4870-a9b9-061961303fe2"},
        {"type":"paging","cubeId":"db2ae6c9-0548-4870-a9b9-061961303fe2","config":{"limit":^^50,"offset":0}},
        {"type":"queryConfig","cubeId":"db2ae6c9-0548-4870-a9b9-061961303fe2","config":{"needCount":True,"queryCount":False,"queryDetail":True}},
        {"type":"placeholder","cubeId":"db2ae6c9-0548-4870-a9b9-061961303fe2","config":{"configs":
        [{"id":"b683125725","name":"cxrq","type":"monthRegion","format":@@"YYYY-MM","values":["202207"]}]}}
        ],"reportId":"9d827f27-c132-46e5-bd81-caf2b88d8730","dataType":##"general","componentId":"6c930aa0-d147-40c7-86f6-1bb255976599","componentName":"申报率统计(按户数)"},
    "componentId": "6c930aa0-d147-40c7-86f6-1bb255976599",
    "reportId": **"9d827f27-c132-46e5-bd81-caf2b88d8730"
    }'''

    # 测试不同的查找路径
    print(findjsonpath(data, '"type"', 'key'))  # 查找所有键为"type"的路径
    print(findjsonpath(data, '"202207"'))  # 查找值为"202207"的路径
    print(findjsonpath(data, '^^'))  # 查找值为"^^"的路径
    print(findjsonpath(data, '@@'))  # 查找值为"@@"的路径
    print(findjsonpath(data, '**'))  # 查找值为"**"的路径
    print(findjsonpath(data, '&&'))  # 查找值为"&&"的路径
    print(findjsonpath(data, '##'))  # 查找值为"##"的路径

    # 其他测试数据
    b = "{'sd':{'zx':{'fr':**3}},'aq':None}"
    c = "{'sd':[{'fr':3}],'aq':"
    d = "{'sd':[{'fr':3}],'aq':[1,3,5,"
    e = "{'sd':[{}, {'fr':"
    k = "{'sd':[{'fr':3}],'aq':[[1,3,5],[7,**8,9]]}"
    m = "{'sd':[4,{'rt':2,'fr':3},**5],'aq':[[1,3,5],[7,8,9]]}"
    
    # 打印测试结果
    print(b, '==>dict', findjsonpath(b, '**'))
    print(c, '==>dict', findjsonpath(c))
    print(d, '==>dict', findjsonpath(d))
    print(e, '==>dict', findjsonpath(e))
    print(k, '==>dict', findjsonpath(k, '**'))
    print(m, '==>dict', findjsonpath(m, '**'))

