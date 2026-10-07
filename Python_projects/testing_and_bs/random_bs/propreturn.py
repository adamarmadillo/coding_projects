inflation = 3.97
profit_a = 7.21
profit_b = 40

def real_gain(profit, inflation):
    return 100 * (profit - inflation) / (100 + inflation)

rg_a = real_gain(profit_a, inflation)
#print(f"p_a: {rg_a}")

rg_b = real_gain(profit_b, inflation)
#print(f"p_b: {rg_b}")

percent_diff = profit_b / profit_a
print(f"%d: {percent_diff}")

real_diff = rg_b / rg_a
print(f"rd: {real_diff}")

print(f"rd/%d: {real_diff / percent_diff}")