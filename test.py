



yes = [(3, 5), (3, 5), (3, 4)]


value_one, values_two, value_three = yes


if value_one[0] == values_two[0] == value_three[0]:
    print("yes")


if value_one[1] == values_two[1] == value_three[1]:
    print("no")

print(value_one[0] == values_two[0] == value_three[0])