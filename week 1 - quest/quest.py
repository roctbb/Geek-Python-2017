import random

people = 3
place = 1
have_knife = 0
have_flash = 0
have_rope = 0
have_boots = 0
while True:
    if place == 1:
        print("Вы услышали крик в лесу. Останетесь ли вы в палатке или пойдете проверите? (Пойти проверить/Остаться)")
        deed = input()
        chance = random.randint(1, 3)
        if deed == "Пойти проверить":
            place = 3
            if chance == 1:
                print("Ваш лучший друг Вася не согласился с вами и решил остаться в палатке")
                people = 2
        else:
            place = 2

    if place == 2:
        print("Итак, команда крайне храбрых сычей решила зарыться в страхе в единственном безопасном месте. Однако вскоре кто-то набрался смелости и решил проверить...")
        print("Один человек покинул группу.")
        people = people - 1
        print("Он ушел, но всё, что вы могли сделать, это лишь сидеть и ждать.")
        print(
        "Наступило утро, от вашего друга до сих пор ни слуху ни духу, но оставшиеся в лагере не горят желанием дальше здесь оставаться")
        print("Что вы сделаете?")
        print("Выберите одно из двух: пойти искать ИЛИ уехать")
        desicion2 = input()
        if desicion2 == "пойти искать":
            place = 7
            have_boots = 1
            have_rope = 1
            print("Вы взяли, что у вас было под руками и ногами и пошли в путь.")
            print("Но даже Богам неизвестно, с чем вы можете столкнуться в этом путешествии...")
            print(
            "...и вы это понимали тоже. Отойдя на метров пятьдесят от лагеря, вы опомнились и начали молча собирать свои вещи.")
        else:
            print(
            "Вы решили не проявлять беспокойство за своего товарища и впервую очередь начали думать о своей безопасности.")
            print(
            "Проверив наличие сладкого рулета, вы как можно быстрее собрали все вещи и, никого не предупредив, задали стрекача.")
            place = 8
    if place == 3:
        answer = input("берете ли вы мутного типа?")
        if answer == "да":
            have_knife = 1
            people = people + 1
            place = 4
            print ("???")
        else:
            have_knife = 0
            people = 3
            place = 9

