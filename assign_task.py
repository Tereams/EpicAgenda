import datetime
from datetime import timedelta

nine_thirty = datetime.time(9, 30)
ten_thirty = datetime.time(22, 30)


def assign_task(task_item, date_item):
    todo_list=date_item['todo']
    todo_date=date_item['date']

    start_time=datetime.datetime.combine(todo_date, nine_thirty)

    end_time=datetime.datetime.combine(todo_date, ten_thirty)
    # check if the todo_list has an end time
    if len(todo_list)==0:
        todo_list.append({'time':(end_time,end_time)})
    elif todo_list[-1]['time'][1]!=end_time:
        todo_list.append({'time':(end_time,end_time)})

    # compute time difference between start time and start time of the first task
    # iterate all the time pieces
    for todo_i in range(len(todo_list)):
        # compute time difference
        head_time=todo_list[todo_i]['time'][0]
        time_diff = head_time - start_time
        hours_diff = time_diff.total_seconds() / 3600
        
        # hours_diff can't be negative
        assert int(hours_diff) >=0
        #if time piece is enough
        if hours_diff >= task_item['time_cost']:
            # 分配任务：为任务创建具体日期属性，加入当天的日程
            time_delta = datetime.timedelta(hours=task_item['time_cost'])
            task_item['time']=(start_time,start_time+time_delta)
            todo_list.insert(todo_i,task_item)
            date_item['todo']=todo_list
            return 1

        elif hours_diff>0: # not enough time
            # try to divide the task (longer than two hours)
            if task_item['time_cost']>2:
                #将原任务的时间进行分割，然后后半部分重新放回队首
                task_item['time_cost']-=hours_diff
                #将分割后的前半部分任务加入todo
                todo_item={'content':'测试日程1','time':(start_time,head_time),'ddl':task_item['ddl'], 'priority':task_item['priority']}
                todo_list.insert(todo_i,task_item)
                date_item['todo']=todo_list               
                return 0
            # not dividable: go to next slot
            else:
                start_time= todo_list[todo_i]['time'][1]
        # no time piece in between: go to next slot
        else:
            start_time= todo_list[todo_i]['time'][1]
    return -1

def assign(task_list, date_list):
    # the earliest of start date is today. 
    start_date= max(datetime.date(2024, 9, 11),datetime.date.today())
    # 循环task_list，按照优先级为每一个任务分配一个时间
    ti=0
    while ti < len(task_list):
        #date_list not empty, compare last date with the given date
        if len(date_list)>0 and date_list[-1]['date']>=start_date:
            # if existed todo date is later than start,
            # then the start date should be included in the date_list
            # (We assume there will be tasks every day)
            for di in range(len(date_list)):
                # find the start date
                if date_list[di]['date']<start_date:
                    continue
                # assign task to the start date
                success=assign_task(task_list[ti],date_list[di])
                # task assigned successfully, turn to the next task
                if success > 0:
                    ti+=1
                    break
                # success == 0, task been divided, do nothing
                # success <0, task cannot be assigned turn to the next day
                if success < 0:
                    di+=1
            else:
                #if existed date cannot assign a task, create a new date
                new_date_item={'date':date_list[-1]['date']+timedelta(days=1),'todo':[]}
                assign_task(task_list[ti],new_date_item)
                date_list.append(new_date_item)
                ti+=1
        # if target date not in date list or existed date cannot assign
        else:
            new_date_item={'date':start_date,'todo':[]}
            assign_task(task_list[ti],new_date_item)
            date_list.append(new_date_item)
            ti+=1            


if __name__=='__main__':
    today = datetime.date.today()  # 获取今天的日期
    # start_time_everyday = datetime.datetime.combine(today, nine_thirty)  # 组合日期和时间

    specific_date1 = datetime.datetime(2024, 9, 12, 10, 30, 45)
    specific_date2 = datetime.datetime(2024, 9, 15, 10, 30, 45)
    # specific_date3 = datetime.datetime(2024, 9, 18, 10, 30, 45)
    ts=datetime.datetime(2024, 9, 12, 9, 30, 00)
    te=datetime.datetime(2024, 9, 12, 10, 30, 00)

    # print(specific_date)  # 输出 2024-09-12 10:30:45


    task_item1={'content':'测试任务1','time_cost':2,'ddl':specific_date1, 'priority':1}
    task_item2={'content':'测试任务2','time_cost':4,'ddl':specific_date2, 'priority':2}
    # task_item3={'content':'测试任务3','time_cost':1,'ddl':specific_date3, 'priority':3}

    task_list=[]
    task_list.append(task_item1)
    task_list.append(task_item2)
    # task_list.append(task_item3)

    #想办法制造一个时间量，每天的九点半

    todo_list=[]
    todo_item1={'content':'测试日程1','time':(ts,te),'ddl':specific_date1, 'priority':1}
    todo_list.append(todo_item1)
    date_list=[]
    specific_date = datetime.date(2024, 9, 12)
    date_item={'date':specific_date,'todo':todo_list}
    date_list.append(date_item)

    assign(task_list,date_list)

    