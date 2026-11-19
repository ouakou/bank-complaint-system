# get money information

money_owed = float(input('How much money do you owe?'))

apr = float(input('what is your yearly average intreset rate?'))

payement = float(input('what is your monthly payement?'))

months = float(input('how many months do you want ot see the results for?'))


monthly_rate = apr/100/12 

interest_paid = payement * monthly_rate
