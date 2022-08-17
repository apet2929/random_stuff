from time import time


def simple_interest(principal, rate_percent, time_years):
    return principal * (rate_percent / 100) * time_years

def compound_interest(principal, real_interest_percent, time_years, compound_duration_years):
    num_iters = time_years / compound_duration_years
    current_total = principal
    # num_iters = math.floor(num_iters)
    for i in range(num_iters):
        current_total += simple_interest(current_total, real_interest_percent, compound_duration_years)
    return current_total - principal

def nominal_interest(principal, real_interest_percent, time_years):
    return compound_interest(principal, real_interest_percent, time_years, 1/12)

principal = 1000
rate = 0.07
time = 3
interest = nominal_interest(principal, rate, time)
print(principal + interest)
