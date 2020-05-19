# [Faberge easter eggs crush test](https://www.codewars.com/kata/5976c5a5cd933a7bbd000029/train/python) [linear]

This is the SUPER performance version of [This kata](https://www.codewars.com/kata/faberge-easter-eggs-crush-test).

You task is exactly the same as that kata. But this time, you should output result % 998244353, or otherwise the result would be too large.

### Data Range
    sometimes
    n <= 80000
    m <= 100000
    while sometimes
    n <= 3000
    m <= 2^200


### The previous Kata Task

One man (lets call him Eulampy) has a collection of some almost identical Fabergè eggs. One day his friend Tempter said to him:

>- Do you see that skyscraper? And can you tell me a maximal floor that if you drop your egg from will not crack it?
>- No, - said Eulampy.
>- But if you give me N eggs, - says Tempter - I'l tell you an answer.
>- Deal - said Eulampy. But I have one requirement before we start this: if I will see more than M falls of egg, my heart will be crushed instead of egg. So you have only M trys to throw eggs. Would you tell me an exact floor with this limitation?
#### Task
Your task is to help Tempter - write a function

    height :: Integer -> Integer -> Integer
    height n m = -- see text

that takes 2 arguments - the number of eggs **n** and the number of trys **m** - you should calculate maximum scyscrapper height (in floors), in which it is guaranteed to find an exactly maximal floor from which that an egg won't crack it.

Which means,

1. You can throw an egg from a specific floor every try
2. Every egg has the same, certain durability - if they're thrown from a certain floor or below, they won't crack. Otherwise they crack.
3. You have n eggs and m tries
4. What is the maxmimum height, such that you can always determine which floor the target floor is when the target floor can be any floor between 1 to this maximum height?

#### Examples
    height 0 14 = 0
    height 2 0  = 0
    height 2 14 = 105
    height 7 20 = 137979