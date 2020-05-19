MOD = 998244353

def height(n, m):
    m %= MOD
    inv = [0] * (n + 1)
    last = 1
    ans = 0
    for i in range(1, n+1):
        inv[i] = -(MOD // i) * inv[MOD % i] % MOD if i > 1 else 1
        last = last * (m - i + 1) * inv[i] % MOD
        ans = (ans + last) % MOD
    return ans    


print('n', 1, 'm', 51, 'my_ans', height(1,51), 51)
print('n', 2, 'm', 1, 'my_ans', height(2,1), 1)
print('n', 4, 'm', 17, 'my_ans', height(4,17), 3213)
print('n', 16, 'm', 19, 'my_ans', height(16,19), 524096)
print('n', 23, 'm', 19, 'my_ans', height(23,19), 524287)
print('n', 13, 'm', 550, 'my_ans', height(13,550), 621773656)
print('n', 3000, 'm', 2 ** 200, 'my_ans', height(3000,2 ** 200), 141903106)
print('n', 8*10 ** 4, 'm', 10 ** 5, 'my_ans', height(8*10 ** 4,10 ** 5), 805097588)