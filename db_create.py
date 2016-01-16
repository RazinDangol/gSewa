from gsewa import db
from models import Payment, Cashback, Info

from parse import * 
import xlrd as x

# Defining the excel cell data info
  # Description column
deb_col = 11  # Debit column
cre_col = 12  # Credit column
bal_col = 13  # Balance Column
stat_col = 14  # Status Column


def doc_open(doc_name):
    workbook = x.open_workbook(doc_name)
    sheet = workbook.sheet_by_index(0)
    return sheet
# insert data

def info(doc_name):
    id_row = 3
    id_col = 10
    sheet = doc_open(doc_name)
    esewa_id = str(parse(sheet, id_row, id_col))
    db.session.add(Info(esewa_id))
    db.session.commit()


def populate(doc_name):
    row = 7
    des_col = 5
    deb_col = 11  # Debit column
    cre_col = 12  # Credit column
    bal_col = 13  # Balance Column
    sheet = doc_open(doc_name)
    while parse(sheet,row,des_col):
        desc=parse(sheet,row,des_col)
        time = parse(sheet,row,1)   
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
                command_execute('cashback','NTC',desc,'adsl','Topup',credit,status,time)
            elif refine('prepaid', desc):
                command_execute('cashback','NTC',desc,'prepaid','Topup',credit,status,time)
            elif refine('postpaid', desc):
                command_execute('cashback','NTC',desc,'postpaid','Topup',credit,status,time)
            elif refine('landline',desc):
                command_execute('cashback','NTC',desc,'landline','Topup',credit,status,time)
            elif refine('NT Recharge Card',desc):
                command_execute('cashback','NTC',desc,'recharge_card','Recharge Card',credit,status,time)
            elif refine('Ncell', desc):
                command_execute('cashback','NCELL',desc,'prepaid','Topup',credit,status,time)              
            elif refine('SIM TV Payment', desc):
                command_execute('cashback','SIMTV',desc,'simtv','Topup',credit,status,time)
            elif refine('Worldlink', desc):
                command_execute('cashback','WORLDLINK',desc,'worldlink','Topup',credit,status,time)
            elif refine('UTL', desc):
                command_execute('cashback','UTL',desc,'utl','recharge_card',credit,status,time)
            elif refine('Vianet', desc):
                command_execute('cashback','VIANET',desc,'vianet','Topup',credit,status,time)    
            elif refine('eSewa', desc):  # Greedy Sewa cash back is assumed to be cashback of dish home recharge card
                command_execute('cashback','DISHHOME',desc,'recharge_card','Topup',credit,status,time)
            elif refine('subisu', desc):
                command_execute('cashback','SUBISU',desc,'subisu','Topup',credit,status,time)
            else: 
                pass
        elif refine('sim commission',desc):
            command_execute('cashback','SIM',desc,'sim commission','Transfer',credit,status,time)

        elif refine('topup',desc):
            if refine('prepaid',desc):
                command_execute('payment','NTC',desc,'prepaid','Topup',debit,status,time)
            elif refine('postpaid',desc):
                command_execute('payment','NTC',desc,'postpaid','Topup',debit,status,time)
            elif refine('adsl',desc):
                command_execute('payment','NTC',desc,'adsl','Topup',debit,status,time)
            elif refine('landline',desc):
                command_execute('payment','NTC',desc,'landline','Topup',debit,status,time)
            elif refine('7190*',desc):
                command_execute('payment','DISHHOME',desc,'dishhome','Topup',debit,status,time)
            elif refine('1000*',desc):
                command_execute('payment','SIMTV',desc,'simtv','Topup',debit,status,time)
            else: pass
        elif refine('payment',desc):
            if refine('980*',desc) or refine('981*',desc):
                command_execute('payment','NCELL',desc,'ncell','Topup',debit,status,time)
            elif refine('subisu',desc):
                command_execute('payment','SUBISU',desc,'subisu','Payment',debit,status,time)
            elif refine('NEA BILL',desc):
                command_execute('payment','NEA',desc,'nea','Payment',debit,status,time)
            else:
                pass
        elif refine('Bought recharge',desc):
            if refine('NTGSM',desc):
                command_execute('payment','NTC',desc,'ntcgsm','Recharge Card',debit,status,time)
            elif refine('DHOME',desc):
                command_execute('payment','DISHHOME',desc,'dishhome','Recharge Card',debit,status,time)
            else:
                pass
        else:
            pass
        row+=1

def command_execute(table,service_provider,service,service_name,service_type,amount,status,time):
    if table == 'payment':
        db.session.add(Payment(service_provider,service,service_name,service_type,float(amount),status,time))
    else:
        db.session.add(Cashback(service_provider,service,service_name,service_type,float(amount),status,time))
    
# Commit the changes
db.session.commit()