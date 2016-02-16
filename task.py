from gsewa import app, db ,make_celery
from models import Payment, Cashback, Info, Transfer, Other, Missing
from parse import * 
import xlrd as x
import datetime
from sqlalchemy.sql import func
celery = make_celery(app)


deb_col = 11  # Debit column
cre_col = 12  # Credit column
bal_col = 13  # Balance Column
stat_col = 14  # Status Column

def doc_open(doc_name):
    workbook = x.open_workbook(doc_name)
    sheet = workbook.sheet_by_index(0)
    return sheet
# insert data
db.drop_all()
db.create_all()
def info(doc_name):
    id_row = 3
    id_col = 10
    sheet = doc_open(doc_name)
    esewa_id = str(parse(sheet, id_row, id_col))
    db.session.add(Info(esewa_id))
    db.session.commit()

def command_execute(table,service_provider,service,service_name,service_type,amount,status,date,time):
    if table == 'payment':
        db.session.add(Payment(service_provider,service,service_name,service_type,float(amount),status,date,time))
    elif table =='cashback':
        db.session.add(Cashback(service_provider,service,service_name,service_type,float(amount),status,date,time))
    else:
        pass

@celery.task(bind=True)
def populate(self,doc_name):
    row = 7
    des_col = 5
    deb_col = 11  # Debit column
    cre_col = 12  # Credit column
    bal_col = 13  # Balance Column
    db.drop_all()
    db.create_all()
    info(doc_name)
    self.update_state(state='PROGRESS')
    sheet = doc_open(doc_name)
    while parse(sheet,row,des_col):
        self.update_state(state='PROGRESS')
        desc=parse(sheet,row,des_col)
        datetime = parse(sheet,row,1).split(' ')
        date = datetime[0]
        time = datetime[1]
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
                command_execute('cashback','NTC',desc,'adsl','Topup',credit,status,date,time)
            elif refine('prepaid', desc):
                command_execute('cashback','NTC',desc,'prepaid','Topup',credit,status,date,time)
            elif refine('postpaid', desc):
                command_execute('cashback','NTC',desc,'postpaid','Topup',credit,status,date,time)
            elif refine('landline',desc):
                command_execute('cashback','NTC',desc,'landline','Topup',credit,status,date,time)
            elif refine('NT Recharge Card',desc):
                command_execute('cashback','NTC',desc,'recharge card','Recharge Card',credit,status,date,time)
            elif refine('Ncell', desc):
                command_execute('cashback','NCELL',desc,'prepaid','Topup',credit,status,date,time)              
            elif refine('SIM TV Payment', desc):
                command_execute('cashback','SIMTV',desc,'simtv','Topup',credit,status,date,time)
            elif refine('Worldlink', desc):
                command_execute('cashback','WORLDLINK',desc,'worldlink','Topup',credit,status,date,time)
            elif refine('UTL', desc):
                command_execute('cashback','UTL',desc,'utl','recharge card',credit,status,date,time)
            elif refine('Vianet', desc):
                command_execute('cashback','VIANET',desc,'vianet','Topup',credit,status,date,time)    
            elif refine('eSewa', desc):  # Greedy Sewa cash back is assumed to be cashback of dish home recharge card
                command_execute('cashback','DISHHOME',desc,'recharge card','Topup',credit,status,date,time)
            elif refine('SUBISU', desc):
                command_execute('cashback','SUBISU',desc,'subisu','Topup',credit,status,date,time)
            else: 
                command_execute('other','other',desc,'unknown','Topup',credit,status,date,time)
        elif refine('sim commission',desc):
            command_execute('cashback','SIM',desc,'sim commission','Transfer',credit,status,date,time)
        elif refine('WEBSURFER.COM',desc):
            command_execute('payment','WEBSURFER',desc,'websurfer','Payment',debit,status,date,time)
        elif refine('Cash Back',desc):
            command_execute('cashback','WEBSURFER',desc,'websurfer','Payment',credit,status,date,time)

        elif refine('topup',desc):
            if refine('prepaid',desc):
                command_execute('payment','NTC',desc,'prepaid','Topup',debit,status,date,time)
            elif refine('postpaid',desc):
                command_execute('payment','NTC',desc,'postpaid','Topup',debit,status,date,time)
            elif refine('adsl',desc):
                command_execute('payment','NTC',desc,'adsl','Topup',debit,status,date,time)
            elif refine('landline',desc):
                command_execute('payment','NTC',desc,'landline','Topup',debit,status,date,time)
            elif refine('7190*',desc):
                command_execute('payment','DISHHOME',desc,'topup','Topup',debit,status,date,time)
            elif refine('1000*',desc):
                command_execute('payment','SIMTV',desc,'simtv','Topup',debit,status,date,time)
            else:
                command_execute('other','other',desc,'unknown','Topup',debit,status,date,time)
        elif refine('payment',desc):
            if refine('980*',desc) or refine('981*',desc):
                command_execute('payment','NCELL',desc,'ncell','Topup',debit,status,date,time)
            elif refine('subisu',desc):
                command_execute('payment','SUBISU',desc,'subisu','Payment',debit,status,date,time)
            elif refine('NEA BILL',desc):
                command_execute('payment','NEA',desc,'nea','Payment',debit,status,date,time)
            else:
                command_execute('other','other',desc,'unknown','Payment',debit,status,date,time)
        elif refine('Bought recharge',desc):
            if refine('NTGSM',desc):
                command_execute('payment','NTC',desc,'ntcgsm','Recharge Card',debit,status,date,time)
            elif refine('DHOME',desc):
                command_execute('payment','DISHHOME',desc,'recharge card','Recharge Card',debit,status,date,time)
            elif refine('NTCDMA',desc):
                command_execute('payment','NTC',desc,'ntrecharge','Recharge Card',debit,status,date,time)
            else:
                command_execute('other','other',desc,'unknown','Recharge Card',debit,status,date,time)
        elif refine('Money Transfer',desc):
            db.session.add(Transfer('BANK',desc,'received','Transfer',float(credit),status,date,time,desc.replace('Money Transferred from ','')))
        elif refine('Balance Transfer',desc):
            if refine('to',desc):
                db.session.add(Transfer('PEER',desc,'transferred','Transfer',float(debit),status,date,time,desc.replace('Balance Transferred to ','')))
            
            else:
                db.session.add(Transfer('PEER',desc,'received','Transfer',float(credit),status,date,time,desc.replace('Balance Transferred by ','')))
                
        else:
            # saving unknown transaction description to file
            f = open('unknown.lst','r')
            lines = f.readlines()
            f.close()

            with open('unknown.lst','a+') as f:
                if desc+'\n' not in lines:
                    f.write(desc+'\n')
                    lines.append(desc)
                else:
                    f.flush()  

            if float(credit) != 0:
                db.session.add(Other('other',desc,' Unknown Cashback','cashback',float(credit),status,date,time))
            else:
                db.session.add(Other('other',desc,' Unknown Payment','payment',float(debit),status,date,time))

        row+=1
    db.session.commit()
    return {'result':'Task Completed'}


@celery.task()
def missing_task():
    successful=[]
    missing=[]
    '''
    service_providers=[]
    payment_check = db.session.query(func.count(Payment.amount),Payment.service_provider).filter(Payment.status=='COMPLETE').group_by(Payment.service_provider)
 
    for payment in payment_check:
        cashback_check = db.session.query(func.count(Cashback.amount),Cashback.service_provider).filter_by(service_provider=payment.service_provider).group_by(Cashback.service_provider).first()
        c = [cashback for cashback in cashback_check]
        if payment[0] != c[0]:
            service_providers.append(payment.service_provider)
    print(service_providers)
    '''
    payment = db.session.query(Payment)
    for i in payment: 
        if i.status != 'COMPLETE' or i.service_provider=='NEA':
            continue
        payment_time = i.time.split(':')
        payment_date = i.date
        p_time = datetime.timedelta(hours=int(payment_time[0]),minutes=int(payment_time[1]),seconds=int(payment_time[2]))
        cashback_times = db.session.query(Cashback.time).filter_by(date=payment_date)
        for j in cashback_times:
            cashback_time = j.time.split(':')
            c_time = datetime.timedelta(hours=int(cashback_time[0]),minutes=int(cashback_time[1]),seconds=int(cashback_time[2]))
            if (c_time - p_time).seconds >= 0 and (c_time - p_time).seconds < 35:
                successful.append(i.date + ' ' +i.time)
                break
            else:
                pass
        missing.append(i.date + ' ' +i.time)
    m = [val for val in missing if val not in successful]
    print(m)
    for i in m:
        d = i.split(' ')
        q = db.session.query(Payment.service_provider,Payment.service,Payment.service_name,Payment.service_type,Payment.amount,Payment.status,Payment.date,Payment.time).filter_by(date=d[0],time=d[1]).first()
        db.session.add(Missing(q.service_provider,q.service,q.service_name,q.service_type,q.amount,q.status,q.date,q.time))
    print('Successful:',len(successful))

