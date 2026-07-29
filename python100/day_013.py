"""
xinhua={
    '麓': '山脚下',
    '路': '道，往来通行的地方；方面，地区：南～货，外～货；种类：他俩是一～人',
    '蕗': '甘草的别名',
    '潞': '潞水，水名，即今山西省的浊漳河；潞江，水名，即云南省的怒江'
}
print(xinhua)
person={
    'name':'王大锤',
    '身高':180,
    '体重':120,
    '性别':'男',
    '年龄':30,
    'addr': '成都市武侯区科华北路62号1栋101', 
    'tel': '13122334455',
    'emergence contact': '13800998877'
}
print(person)

person=dict(name='王大锤',age=18,height=180,weight=60,addr='成都市武侯区科华北路62号1栋101')
print(person)
items1=dict(zip('ABCDE','12345'))
print(items1)
items2=dict(zip('ABCDE',range(1,10)))
print(items2)
items3={x:x**3 for x in range(1,6)}
print(items3)
print(len(person))
for key in person:
    print(key)

person={
    'name':'王大锤',
    'car':{
        'maxspeed':'250',
        'height':'1835'
    }
}
print(person)

person = {'name': '王大锤', 'age': 55, 'height': 168, 'weight': 60, 'addr': '成都市武侯区科华北路62号1栋101'}
print('name' in person)
print('tel' in person)
print(person['name'])
print(person['addr'])
person['age']=25
person['height']=180
person['tel']='13122334455'
person['signature'] = '你的男朋友是一个盖世垃圾，他会踏着五彩祥云去迎娶你的闺蜜'
print(person)
for key in person:
    print(f'{key}:\t{person[key]}')

person = {'name': '王大锤', 'age': 55, 'height': 168, 'weight': 60, 'addr': '成都市武侯区科华北路62号1栋101'}
print(person.get('name'))
print(person.get('sex'))
print(person.get('sex',True))  

person = {'name': '王大锤', 'age': 55, 'height': 168, 'weight': 60, 'addr': '成都市武侯区科华北路62号1栋101'}
print(person.keys())
print(person.values())
print(person.items())
for key,value in person.items():
    print(f'{key}\t{value}')

person1 = {'name': '王大锤', 'age': 55, 'height': 178}
person2 = {'age': 25, 'addr': '成都市武侯区科华北路62号1栋101'}
person1.update(person2)
print(person1)

person1 = {'name': '王大锤', 'age': 55, 'height': 178}
person2 = {'age': 25, 'addr': '成都市武侯区科华北路62号1栋101'}
person1 |= person2
print(person2)

person = {'name': '王大锤', 'age': 25, 'height': 178, 'addr': '成都市武侯区科华北路62号1栋101'}
print(person.pop('age'))
print(person)
print(person.popitem())
print(person)
person.clear()
print(person)

person = {'name': '王大锤', 'age': 25, 'height': 178, 'addr': '成都市武侯区科华北路62号1栋101'}
del person['age']
del person['addr']
print(person)
"""
sentence=input('请输入一段话：')
counter={}
for ch in sentence:
    if 'A' <=ch <='Z' or 'a'<=ch <='z':
        counter[ch]=counter.get(ch,0)+1
sorted_keys=sorted(counter,key=counter.get,reverse=True)
for key in sorted_keys:
    print(f'{key}出现了{counter[key]}次.')