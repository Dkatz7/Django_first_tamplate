from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Events
from .serializer import EventSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from .serializer import UserInformationSerializer
from .models import PrivetInformation
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status



def index(req):
    return JsonResponse('hello', safe=False)

@api_view(['GET'])
def events(req):
    all_events = EventSerializer(Events.objects.all(), many=True).data
    return JsonResponse(all_events, safe= False)


#### login ####
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        # ...
 
        return token
 
 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

###### register ######
@api_view(['POST'])
def register(req):
    user = User.objects.create_user(
                username=req.data['username'],
                email=req.data['email'],
                password=req.data['password']
            )
    user.is_active = True
    user.is_staff = True
    user.save()
    return Response("new user born")



####### full CRUD for user's information #########
@permission_classes(IsAuthenticated)
@api_view(['GET','POST','DELETE','PUT','PATCH'])
def info(req,id=-1):
    
    if req.method =='GET':
        user= req.user
        if id > -1:
            try:
                temp_task=user.privetinformation_set.get(id=id)
                return Response (UserInformationSerializer(temp_task,many=False).data)
            except PrivetInformation.DoesNotExist:
                return Response ("not found")
        all_tasks=UserInformationSerializer(user.privetinformation_set.all(),many=True).data
        return Response ( all_tasks)

    if req.method =='POST':
        tsk_serializer = UserInformationSerializer(data=req.data)
        if tsk_serializer.is_valid():
            tsk_serializer.save()
            return Response ("post...")
        else:
            return Response (tsk_serializer.errors)

    if req.method =='DELETE':
        user= req.user
        try:  
            temp_task=user.privetinformation_set.get(id=id)
        except PrivetInformation.DoesNotExist:
            return Response ("not found")    
        temp_task.delete()
        return Response ("del...")

    if req.method =='PUT':
        user=req.user
        user_id = req.data.get('user')
        if user_id:
            user_id = int(user_id)
            user = User.objects.get(id=user_id)
            try:
                temp_task=user.privetinformation_set.get(id=id)
            except PrivetInformation.DoesNotExist:
                return Response ("not found")
            ser = UserInformationSerializer(data=req.data)
            if ser.is_valid():
                ser.update(temp_task, req.data)
                temp_task.user = req.user
                temp_task.save()
                return Response(ser.data)
            else:
                return Response(ser.errors)
        else:
            return Response("user field is missing")

#####################*END CRUD ##################


############# Image uploade / Get images ###############


# //////////// image upload / display
# return all images to client (without serialize)
@api_view(['GET'])
def getImages(req):
    res=[] #create an empty list
    for img in PrivetInformation.objects.all(): #run on every row in the table...
        res.append({"firstname":img.firstname,
                "lastname":img.lastname,
                "email":img.email,
               "image":str( img.avatar)
                }) #append row by to row to res list
    return Response(res) #return array as json response


# upload image method (with serialize)
class APIViews(APIView):
    parser_class=(MultiPartParser,FormParser)
    def post(self,request,*args,**kwargs):
        api_serializer=UserInformationSerializer(data=request.data)
       
        if api_serializer.is_valid():
            api_serializer.save()
            return Response(api_serializer.data,status=status.HTTP_201_CREATED)
        else:
            print('error',api_serializer.errors)
            return Response(api_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# //////////// end      image upload / display
