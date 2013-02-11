#Problem 0

#dob = raw_input('Please Enter your dat of birth MM/DD/YY: \n**')
#user = raw_input('Please enter your last name: \n**')
#print user, dob

###Problem 1
##
##balance = float(raw_input("Please enter the balance on your credit card: "))
##interest_rate = float(raw_input("Please enter the annual interest rate as a decimal: "))
##monthly_pay_rate = float(raw_input("Please enter the monthly payment rate as a decimal: "))
##total_paid = 0.0
##
##for i in range(1,13):
##    monthly_payment = monthly_pay_rate * balance
##    interest_paid = interest_rate/12.0 * balance
##    principle_paid = monthly_payment - interest_paid
##    balance = balance - principle_paid
##    total_paid = total_paid + monthly_payment
##    print "Month", i
##    print "Minimum monthly payment: $%.2f" % monthly_payment
##    print "Principle paid: $%.2f" % principle_paid
##    print "Remaining balance: $%.2f" % balance
##
##print "RESULT"
##print "Total amount paid: $%.2f" % total_paid
##print "Remaining balance: $%.2f" % balance

#Problem 2

##balance = float(raw_input("Please enter your outstanding balance: "))
##interest = float(raw_input("Please enter your annual interest rate as a decimal: "))
##monthly_interest = interest/12
##remaining_balance = balance
##monthly_payment = 0
##i = 0
##
##while remaining_balance > 0:
##    i = i+1
##    monthly_payment = monthly_payment + 10
##    months = 0
##    remaining_balance = balance
##    while months < 12 and remaining_balance > 0:
##        months = months + 1
##        remaining_balance = remaining_balance * (1 + monthly_interest) - monthly_payment
##        
##    #year_payment = monthly_payment * 12
##    #remaining_balance = (balance * (1 + interest)) - year_payment
##
##print "Monthly: ", monthly_payment
##print "Balance: ", remaining_balance
##print " months: ", months
##print "iterations: ", i

#Problem 3

balance = float(raw_input("Please enter your outstanding balance: "))
interest = float(raw_input("Please enter your annual interest rate as a decimal: "))
monthly_interest = interest/12.0
upper = (balance * (1 + (interest/12))**12)/12
lower = balance/12
monthly_payment = (upper + lower)/2
months = 0
remaining_balance = balance
j =0
while upper - lower > 0.005:
    j = j + 1
    remaining_balance = balance
    monthly_payment = (upper + lower)/2
    print "Monthly Payment: ", monthly_payment
    for i in range(1,13):
        remaining_balance = remaining_balance * (1 + monthly_interest) - monthly_payment
    if remaining_balance < 0:
        upper = monthly_payment
    else:
        lower = monthly_payment

        
##    if months < 12:
##        upper = monthly_payment
##    if months > 12:
##        lower = monthly_payment
        
print "Monthly: ", monthly_payment
print "Balance: ", remaining_balance
#print "Months: ", months
print "iterations: ", j


