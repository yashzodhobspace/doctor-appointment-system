from ast import Str
from .models import doctor,patient,slot,Appointment
from rest_framework import serializers
from datetime import datetime
import pytz

utc=pytz.UTC

class DoctorSerializers(serializers.Serializer):
        name = serializers.CharField(max_length=50)
        speciality = serializers.CharField(max_length=50)

def GetDoctors():
    doctors = doctor.objects.all()
    serializer = DoctorSerializers(doctors,many=True)
    return serializer.data

def CreateDoctors(data):
    serializer = DoctorSerializers(data)
    data = serializer.data
    new = doctor(
        name=data['name'],
        speciality=data['speciality'])
    new.save()
    return new




class PatientSerializers(serializers.Serializer):
    name =serializers.CharField(max_length=50)

def GetPatient():
    patients = patient.objects.all()
    serializer = PatientSerializers(patients,many=True)
    return serializer.data

def CreatePatient(data):
    serializer = PatientSerializers(data)
    data = serializer.data
    new = patient(
        name=data['name']
    )
    new.save()
    return new


class SlotSerializers(serializers.Serializer):
    doctor_id=serializers.IntegerField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    available = serializers.BooleanField()

def StrToDate(date):
    return datetime.strptime(date, '%d/%m/%Y %H:%M:%S')

def GetSlot():
    slots = slot.objects.filter(available=True).values('doctor_id','start_time','end_time','available')
    serializer = SlotSerializers(slots,many=True)
    return(serializer.data)


def CreateSlot(data):
    serializer = SlotSerializers(data)
    data = serializer.data
    doc = doctor.objects.filter(id=data['doctor_id'])
    doc = doc[0]
    slots = slot.objects.filter(doctor_id=data['doctor_id']).values('start_time','end_time')

    start_time = utc.localize(StrToDate(data['start_time']))
    end_time = utc.localize(StrToDate(data['end_time']))

    if start_time>end_time:
        return {"msg":"start time should be greater than end time."}

    for s in slots:
        start_time_s = s['start_time']
        end_time_s = s['end_time']
        print(start_time.tzinfo,start_time_s.tzinfo,"*********************************************")
        if start_time_s<=start_time<=end_time_s or start_time_s<=end_time<=end_time_s:
            return {"msg":"slot time not available for doctor"}

    new = slot(
        doctor = doc,
        start_time = StrToDate(data['start_time']),
        end_time = StrToDate(data['end_time']),
        available = data['available']
    )
    new.save()
    # return new


class AppointmentSeralizer(serializers.Serializer):
    # doc_id=serializers.IntegerField()
    slot_id=serializers.IntegerField()
    pat_id=serializers.IntegerField()
    status=serializers.CharField(max_length=1)

def GetAppointment():
    appointments = Appointment.objects.all().values("pat_id","slot_id","status")
    serializer = AppointmentSeralizer(appointments,many=True)
    return serializer.data

def CreateAppointment(data):
    serializers=AppointmentSeralizer(data)
    data=serializers.data
    slt = slot.objects.filter(id=data['slot_id'])
    slt = slt[0]
    if slt.available==False:
        return {"msg":"Slot not available."}
    pat = patient.objects.filter(id=data['pat_id'])
    pat = pat[0]


    new = Appointment(
        slot = slt,
        pat=pat,
        status=data['status']
    )
    new.save()
    slt.available = False
    slt.save()
    return {"msg":"Appointment created"}
    