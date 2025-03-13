def calculate(data, expense_month):

    result = {}

    month_number_map = {
        "April": 1, "May": 2, "June": 3, "July": 4, "August": 5, "September": 6,
        "October": 7, "November": 8, "December": 9, "January": 10, "February": 11, "March": 12
    }

    month_number = month_number_map.get(expense_month, 1)

    code_name_map = {
        '1640': 'फुटकर प्रभार / Sundry Charges',
        '1610': 'मरम्मत और रखरखाव / Repairs & Maintenance',
        '1460': 'स्टेशनरी व्यय खाता / Stationary Expenses a/c',
        '1650': 'कम्प्यूटर संबंधित प्रभार खाता / Computer related Charges a/c',
        '1660': 'यातायात व्यय / Travelling Expenses',
        '1630': 'इंटरटेन्मेंट व्यय खाता / Entertainment Expenses a/c',
        '1430': 'पोस्टेज/कोरियर प्रभार खाता / Postages/ Couriers Charges a/c',
        '1550': 'विद्युत प्रभार खाता / Electricity Charges a/c',
        '1580': 'टेलीफोन खाता / Telephone a/c'
    }

    for index, code in enumerate(code_name_map.keys(), start=1):
        prev_to_prev_cb = float(data.get(f'{code}_cb_prev_to_prev_year', 0))
        prev_year_cb = float(data.get(f'{code}_cb_prev_year', 0))
        current_month_ob = float(data.get(f"{code}_ob_cur_month", 0))
        current_month_cb = float(data.get(f"{code}_cb_cur_month", 0))

        prev_to_prev_yr_os = round(prev_to_prev_cb / 100000.0, 2)
        prev_yr_os = round(prev_year_cb / 100000.0, 2)
        prev_yr_avg = round((prev_year_cb / 12.0) / 100000.0, 2)
        curr_mon_expense = round((current_month_cb - current_month_ob) / 100000.0, 2)

        percentage_change = 0
        if prev_yr_avg != 0:
            percentage_change = round(
                ((current_month_cb - current_month_ob) - (prev_year_cb / 12.0)) / (prev_year_cb / 12.0) * 100.0, 2)

        cum_till_prev_month = round(current_month_ob / 100000.0, 2)
        cum_till_cur_month = round(current_month_cb / 100000.0, 2)
        cumm_avg = round(cum_till_cur_month / month_number, 2)

        result[code] = {
            'number': index,
            'name': code_name_map[code],
            'prev_to_prev_yr_os': prev_to_prev_yr_os,
            'prev_yr_os': prev_yr_os,
            'prev_yr_avg': prev_yr_avg,
            'curr_mon_expense': curr_mon_expense,
            'percentage_change': percentage_change,
            'cum_till_prev_month': cum_till_prev_month,
            'cum_till_cur_month': cum_till_cur_month,
            'cumm_avg': cumm_avg
        }

    return result
