#-*-coding:utf-8-*-
def guess_num():
    import os
    from random import randint
    name = input('Please input your name:') #user_name input
    if not os.path.isfile('game.txt'):
        f = open('game.txt','w+')
    else:
        f = open('game.txt','r')
    lines = f.readlines()
    f.close()

    scores = {}
    for l in lines:
        s = l.split()
        scores[s[0]] = s[1:]
    score = scores.get(name)
    if score is None:
        score = [0,0,0]

    game_times = int(score[0])
    min_times = int(score[1])
    total_times = int(score[2])
    if game_times > 0:
        avg_times = float(total_times)/game_times
    else:
        avg_times = 0

    print("%s,你已经玩了%d次,最少%d轮猜出答案,平均%.2f轮猜出答案"%(name,game_times,min_times,avg_times))
    num = randint(1,100)
    times = 0
    print("Guess what I think?")
    bingo = False
    while bingo == False:
        answer = int(input())
        if answer > num:
            print('too big!')
        elif answer < num:
            print('too small!')
        else:
            print('Bingo,%d is my number!'%num)
            bingo = True
        times += 1

    game_times += 1
    total_times += times
    if times < min_times or min_times == 0:
        min_times = times
    scores[name] = [str(game_times),str(min_times),str(total_times)]
    results = ''
    f = open('game.txt','w')
    for name in sorted(list(scores)):
        result ='\t\t'.join([name,'\t'.join(scores[name]),'\n'])
        results +=result
    f.write(results)
    f.close()

if __name__ == '__main__':
    try:
        while True:
            guess_num()
            print(">"*60,end='')
            print()
    except KeyboardInterrupt:
        print('\nYou exit!')

