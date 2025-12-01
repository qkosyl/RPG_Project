'''
Funkcja Lambda w Pythonie
1. Co to jest?
Funkcja lambda to funkcja anonimowa, która:
jest tworzona inline (w miejscu użycia),
składa się z jednego wyrażenia,
zwraca wynik automatycznie po jego obliczeniu.
Stosuje się ją, gdy potrzebujemy jednorazowej funkcji, używanej w jednym miejscu w programie.
2. Składnia
Z argumentami:
lambda arg1, arg2, ... : wyrażenie
Bez argumentów:
lambda: wyrażenie
Lambda przyjmuje argumenty jak zwykła funkcja.
Wyrażenie (wyrażenie) jest obliczane i jego wynik jest automatycznie zwracany.
3. Przykład – funkcja zwykła vs lambda
Funkcja zwykła:
def sum_number(a, b):
    return a + b
print(sum_number(1, 3))  # 4
Funkcja lambda:
sum_number_lambda = lambda a, b: a + b
print(sum_number_lambda(1, 3))  # 4
Lambda działa tak samo jak zwykła funkcja.
Można ją przypisać do zmiennej i wywoływać jak funkcję.
4. Zastosowania
Sortowanie listy po niestandardowym kluczu (key=lambda x: x[1]).
Funkcje jednorazowe w map(), filter(), reduce().
Proste operacje matematyczne lub logiczne, które nie wymagają pełnej funkcji.




1. Podstawowe użycie
list.sort() sortuje listę na miejscu (modyfikuje oryginalną listę) i zwraca None.
pairs = [(1, 'one'), (3, 'three'), (2, 'two'), (4, 'four')]
pairs.sort()
print(pairs)
Wynik:
[(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
Domyślnie sortowanie odbywa się rosnąco.
W przypadku listy krotek sortowanie odbywa się po pierwszym elemencie krotki.
Sortowanie jest stabilne – zachowuje kolejność elementów o tej samej wartości.
2. Parametr key
Pozwala określić funkcję, która zwraca wartość używaną do porównania elementów listy.
pairs = [(1, 'one'), (3, 'three'), (2, 'two'), (4, 'four')]
pairs.sort(key=lambda pair_item: pair_item[1])
print(pairs)
Wynik:

[(4, 'four'), (1, 'one'), (3, 'three'), (2, 'two')]
lambda pair_item: pair_item[1] – sortowanie odbywa się po drugim elemencie krotki (napisie).
Nadal sortowanie jest rosnące domyślnie (alfabetycznie dla napisów).
3. Parametr reverse
Jeśli chcemy sortować malejąco, używamy reverse=True:
pairs.sort(key=lambda pair_item: pair_item[1], reverse=True)
print(pairs)
Wynik:
[(2, 'two'), (3, 'three'), (1, 'one'), (4, 'four')]

Podsumowanie:
list.sort() – sortuje listę na miejscu.
key – funkcja określająca kryterium sortowania.
reverse=True – sortowanie malejące.
Sortowanie jest stabilne – elementy o tej samej wartości zachowują pierwotną kolejność.


map(function, iterable)
Zwraca iterator, który stosuje funkcję do każdego elementu iterowalnego obiektu.
Nie modyfikuje oryginalnej listy.
Przykład – kwadraty elementów:
nums = [48, 6, 9, 21, 1]
square_all = map(lambda num: num ** 2, nums)
print(list(square_all)) # [2304, 36, 81, 441, 1]

filter(function, iterable)
Zwraca iterator, który zawiera tylko te elementy, dla których funkcja zwraca True.
Jeśli funkcja jest None, usuwane są elementy "fałszywe" (False, 0, None, '', itd.).
Przykład – liczby parzyste:
nums = [48, 6, 9, 21, 1, 35, 16, 12, 0, -1]
print(list(filter(lambda num: num % 2 == 0, nums))) # [48, 6, 16, 12, 0]
Przykład – filtr z None:
print(list(filter(None, nums))) # [48, 6, 9, 21, 1, 35, 16, 12, -1]

0 zostało usunięte, bo jest "falsy"

functools.reduce(function, iterable[, initializer])
Stosuje funkcję dwóch argumentów do wszystkich elementów iterowalnego obiektu, od lewej do prawej.
Zmniejsza listę do jednej wartości.
Przykład – suma elementów:
from functools import reduce
nums = [1, 2, 3, 4, 5]
result = reduce(lambda x, y: x + y, nums)
print(result) # 15
Jak działa krok po kroku:
iterable = [1, 2, 3, 4, 5]
1+2 = 3
3+3 = 6
6+4 = 10
10+5 = 15
Inne przypadki:
Jeden element → wynik to ten element:
reduce(lambda x, y: x+y, [9]) # 9
Pusta lista z initializer → zwraca wartość initializer:
reduce(lambda x, y: x+y, [], -1) # -1
Podsumowanie różnic
Funkcja Co robi Zwraca
map Zastosowanie funkcji do każdego elementu Iterator z wynikami
filter Zwraca elementy spełniające warunek Iterator z wybranymi elementami
reduce Redukuje listę do jednej wartości Pojedyncza wartość

'''