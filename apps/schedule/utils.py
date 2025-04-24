from datetime import timedelta,datetime
from django.utils import timezone
from ..booking.models import AppointmentBooking

def generate_time_slots(start_time,end_time,break_time_starts,break_time_ends,duration,schedule_date):
    present_date = timezone.now()
    start_time_24hr = datetime.combine(present_date, start_time)
    end_time_24hr = datetime.combine(present_date, end_time)
    break_time_starts_24hr = None
    break_time_ends_24hr = None
    if break_time_starts and break_time_ends:
        break_time_starts_24hr = datetime.combine(datetime.today(), break_time_starts)
        break_time_ends_24hr = datetime.combine(datetime.today(), break_time_ends)
    appointments = AppointmentBooking.objects.filter(selected_date=schedule_date).values('start_time_slot', 'end_time_slot')
    appointment_slots = [(appointment['start_time_slot'], appointment['end_time_slot']) for appointment in appointments]
    time_slots = []
    next_time_slot = start_time_24hr
    next_time_slot_time = next_time_slot.time()
    if not any(start <= next_time_slot_time < end for start, end in appointment_slots):
        time_slots.append(start_time_24hr.strftime("%I:%M%p"))
    if break_time_starts_24hr and break_time_ends_24hr:
        while True:
            next_time_slot = next_time_slot + timedelta(minutes=(duration+10))
            if next_time_slot>=start_time_24hr and next_time_slot+timedelta(minutes=duration)<=end_time_24hr:
                # Convert `next_time_slot` to time
                next_time_slot_time = next_time_slot.time()
                # Check if the time slot conflicts with any appointment slot
                if not any(start <= next_time_slot_time < end for start, end in appointment_slots):
                    if next_time_slot<= break_time_starts_24hr:
                        if next_time_slot+timedelta(minutes=duration) > break_time_starts_24hr:
                            time_slots.append(break_time_ends_24hr.strftime("%I:%M%p"))
                            next_time_slot = break_time_ends_24hr
                            continue
                        else:
                            time_slots.append(next_time_slot.strftime("%I:%M%p"))
                    else:
                        
                        time_slots.append(next_time_slot.strftime("%I:%M%p"))
            else:
                break;
    else:
        while True:
            next_time_slot = next_time_slot + timedelta(minutes=(duration+10))
            if next_time_slot>=start_time_24hr and next_time_slot+timedelta(minutes=duration)<=end_time_24hr:
                # Convert `next_time_slot` to time
                next_time_slot_time = next_time_slot.time()
                # Check if the time slot conflicts with any appointment slot
                if not any(start <= next_time_slot_time < end for start, end in appointment_slots):
                    time_slots.append(next_time_slot.strftime("%I:%M%p"))
                
            else:
                break;

    return time_slots