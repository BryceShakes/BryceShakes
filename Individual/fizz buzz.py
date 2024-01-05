
#   fizzbuzzbang

Dict = {
        'Fizz' : 3,
        'Buzz' : 5,
        'Bang' : 7}

for i in range(200):
    a = ''
    for key in Dict.keys():
        a += key if i%Dict[key] == 0 else ''
    b = i if a == '' else a
    print(i ,b)
