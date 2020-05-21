def elder_age(m,n,l,t):
    if m == 0 or n == 0:
        return 0

    # N should be bigger for this solution
    if m > n:
        m, n = n, m
    
    # losses
    loss_m, loss_n = power_2(m), power_2(n)
    
    # if the loss is greater than the loss in N
    if l > loss_n:
        return 0

    # Final Recursion Step
    if loss_m == loss_n:
        return (sum_terms_in_range(1, loss_n - l - 1) * (m + n - loss_n) + elder_age(loss_n - n, loss_m - m, l, t)) % t
    
    # Recursion rule
    if loss_m < loss_n:
        loss_m = loss_n // 2
        aux = sum_terms_in_range(1, loss_n - l - 1) * m - (loss_n - n) * sum_terms_in_range(max(0, loss_m - l), loss_n - l - 1)
        if l <= loss_m:
            aux += (loss_m - l) * (loss_m - m) * (loss_n - n) + elder_age(loss_m - m, loss_n - n, 0, t)
        else:
            aux += elder_age(loss_m - m, loss_n - n, l - loss_m, t)
        return aux % t


# sum of all terms in a interval
def sum_terms_in_range(l,r):
    return (l+r) * (r-l+1) // 2

def power_2(x):
    time = 1
    # move time 1 bit left
    # until it is bigger than X
    while time < x:
        time <<= 1
    return time


print (elder_age(8,5,1,100), 5)
print (elder_age(8,8,0,100007), 224)
print (elder_age(545,435,342,1000007), 808451)
print(elder_age(28827050410, 35165045587, 7109602, 13719506), 5456283)