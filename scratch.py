def main():
    lst = [0, 1, 2, 3, 4]
    print(lst)

    lst = [x for x in range(5)]
    print(lst)
    print()

    lst_lst = [[y for y in range(x, x+5)] for x in range(5)]
    print(lst_lst)
    print()

    print([x for x in range(10)])
    print([x for x in range(0, 10)])
    print([x for x in range(0, 10, 1)])
    print([x for x in range(10, 0, -1)])
    print([x for x in range(0, 10, 2)])
    print([x for x in range(0, 20, 2)])
    print()

    for x in lst:
        print(x, end=' ')
    print()

    for x in range(len(lst)):
        print(lst[x], end=' ')
    print('\n')

    for x in range(3):
        print(lst[x], end=' ')
    print()

    for x in lst[:3]:
        print(x, end=' ')
    print('\n')

    lst_lst = [[y for y in range(x, x+10, 2)] for x in range(5)]

    for x in lst_lst:
        for y in x:
            print(y, end=' ')
        print('|', end=' ')
    print()

    for x in range(len(lst_lst)):
        for y in range(len(lst_lst[x])):
            print(lst_lst[x][y], end=' ')  # Correct
        print('|', end=' ')
    print()

    for x in range(len(lst_lst)):
        for y in range(len(lst_lst[x])):
            print(lst_lst[y][x], end=' ')  # Incorrect - Wrong indexing order
        print('|', end=' ')
    print('\n')

    lst = [x for x in range(10)]

    from random import shuffle, sample

    print(lst)
    print(sample(lst, 5))
    print(sample(lst, 5))
    print(sample(lst, 5))
    print()
    sub_lst = sample(lst, 5)

    print(sub_lst)
    shuffle(sub_lst)
    print(sub_lst)
    shuffle(sub_lst)
    print(sub_lst)
    shuffle(sub_lst)
    print(sub_lst)
    print(shuffle(sub_lst))
    print()

    print(lst[::-1])
    print(lst[::2])


if __name__ == '__main__':
    main()
