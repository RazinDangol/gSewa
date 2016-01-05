from gsewa import db
from models import Payment, Cashback

from parse import * 
import xlrd as x

# Defining the excel cell data info
  # Description column
deb_col = 11  # Debit column
cre_col = 12  # Credit column
bal_col = 13  # Balance Column
stat_col = 14  # Status Column


db.drop_all()
# Create the tables 
db.create_all()

# insert data

def populate(doc_name):
    workbook = x.open_workbook(doc_name)
    sheet = workbook.sheet_by_index(0)
    row = 7
    des_col = 5
    deb_col = 11  # Debit column
    cre_col = 12  # Credit column
    bal_col = 13  # Balance Column
    while parse(sheet,row,des_col):
        desc=parse(sheet,row,des_col)   
        try:
            credit = float(parse(sheet, row, cre_col))
            debit = float (parse(sheet, row, deb_col))
        except:
            credit=float(parse(sheet,row,cre_col).replace(',',""))
            debit = float (parse(sheet, row, deb_col).replace(',',""))
        status = parse(sheet, row, stat_col)
        if refine('cashback', desc):  # cashback is common on most of the parsed data denoting profit
              # second most common data
            if refine('ADSL', desc):
                command_execute('cashback','NTC',desc,'adsl','Topup',credit,status)
            elif refine('prepaid', desc):
                command_execute('cashback','NTC',desc,'prepaid','Topup',credit,status)
            elif refine('postpaid', desc):
                command_execute('cashback','NTC',desc,'postpaid','Topup',credit,status)
            elif refine('landline',desc):
                command_execute('cashback','NTC',desc,'landline','Topup',credit,status)
            elif refine('NT Recharge Card',desc):
                command_execute('cashback','NTC',desc,'recharge_card','Recharge Card',credit,status)
            elif refine('Ncell', desc):
                command_execute('cashback','NCELL',desc,'prepaid','Topup',credit,status)              
            elif refine('eSewa', desc) and refine('simtv',desc):
                command_execute('cashback','SIMTV',desc,'simtv','Topup',credit,status)
            elif refine('eSewa', desc):  # Greedy Sewa cash back is assumed to be cashback of dish home recharge card
                command_execute('cashback','DISHHOME',desc,'recharge_card','Topup',credit,status)
            elif refine('subisu', desc):
                command_execute('cashback','SUBISU',desc,'subisu','Topup',credit,status)
            else: 
                pass
        elif refine('sim commission',desc):
            command_execute('cashback','SIM',desc,'sim commission','Transfer',credit,status)

        elif refine('topup',desc):
            if refine('prepaid',desc):
                command_execute('payment','NTC',desc,'prepaid','Topup',debit,status)
            elif refine('postpaid',desc):
                command_execute('payment','NTC',desc,'postpaid','Topup',debit,status)
            elif refine('adsl',desc):
                command_execute('payment','NTC',desc,'adsl','Topup',debit,status)
            elif refine('landline',desc):
                command_execute('payment','NTC',desc,'landline','Topup',debit,status)
            elif refine('7190*',desc):
                command_execute('payment','DISHHOME',desc,'dishhome','Topup',debit,status)
            elif refine('1000*',desc):
                command_execute('payment','SIMTV',desc,'simtv','Topup',debit,status)
            else: pass
        elif refine('payment',desc):
            if refine('980*',desc) or refine('981*',desc):
                command_execute('payment','NCELL',desc,'ncell','Topup',debit,status)
            elif refine('subisu',desc):
                command_execute('payment','SUBISU',desc,'subisu','Payment',debit,status)
            else:
                pass
        elif refine('Bought recharge',desc):
            if refine('NTGSM',desc):
                command_execute('payment','NTC',desc,'ntcgsm','Recharge Card',debit,status)
            elif refine('DHOME',desc):
                command_execute('payment','DISHHOME',desc,'dishhome','Recharge Card',debit,status)
            else:
                pass
        else:
            pass
        row+=1

def command_execute(table,service_provider,service,service_name,service_type,amount,status):
    if table == 'payment':
        db.session.add(Payment(service_provider,service,service_name,service_type,float(amount),status))
    else:
        db.session.add(Cashback(service_provider,service,service_name,service_type,float(amount),status))
    
# Commit the changes
db.session.commit()
