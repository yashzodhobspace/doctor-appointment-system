from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .service import GetDoctors,CreateDoctors,GetPatient,CreatePatient,CreateSlot\
    ,GetSlot,CreateAppointment\
    ,GetAppointment
# Create your views here.

class DoctorView(APIView):
    def get(self,request):
        data = GetDoctors()
        return Response(data)
    
    def post(self,request):
        CreateDoctors(request.data)
        return Response({'msg':'Doctor Created'})

class PatientView(APIView):
    def get(self,request):
        data = GetPatient()
        return Response(data)

    def post(self,request):
        CreatePatient(request.data)
        return Response({'msg':"patient created"})

class SlotView(APIView):
    def get(self,request):
        data = GetSlot()
        return Response(data)

    def post(self,request):
        data = CreateSlot(request.data)
        return Response(data)
        # return Response({"msg":"slot created"})

class AppointmentView(APIView):
    def get(self,request):
        data = GetAppointment()
        return Response(data)

    def post(self,request):
        data = CreateAppointment(request.data)

        return Response(data)
