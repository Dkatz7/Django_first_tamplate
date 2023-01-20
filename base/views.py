from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from django.contrib.auth.models import User

from .models import Events
from .serializer import EventSerializer
from .serializer import UserInformationSerializer
from .models import PrivetInformation



def index(req):
    return Response('hello', safe=False)

@api_view(['GET'])
def events(req):
    all_events = EventSerializer(Events.objects.all(), many=True).data
    return Response(all_events, safe= False)


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

@permission_classes([IsAuthenticated])
class PrivetInformationView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request):
        """
        Handle GET requests to return a list of MyModel objects
        """
        user=request.user
        my_model = user.privetinformation_set.all()
        serializer = UserInformationSerializer(my_model, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        """
        Handle POST requests to create a new Task object
        """
        # usr =request.user
        # print(usr)
        serializer = UserInformationSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def put(self, request, id):
        """
        Handle PUT requests to update an existing Task object
        """
        user=request.user
        my_model = user.privetinformation_set.all()
        serializer = UserInformationSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk):
        """
        Handle DELETE requests to delete a Task object
        """
        my_model = PrivetInformation.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#####################*END CRUD ##################




############# Image uploade / Get images ###############


# //////////// image upload / display
# return all images to client (without serialize)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getImages(request):
    res=[] #create an empty list
    user=request.user
    for img in user.privetinformation_set.all(): #run on every row in the table...
        res.append({"firstname":img.firstname,
                "lastname":img.lastname,
                "email":img.email,
               "image":str( img.avatar)
                }) #append row by to row to res list
    return Response(res) #return array as json response


# upload image method (with serialize)


@permission_classes([IsAuthenticated])
class APIViews(APIView):
    parser_class=(MultiPartParser,FormParser)
    def post(self,request,*args,**kwargs):
        api_serializer=UserInformationSerializer(data=request.data, context={'user'==request.user})
       
        if api_serializer.is_valid():
            api_serializer.save()
            return Response(api_serializer.data,status=status.HTTP_201_CREATED)
        else:
            print('error',api_serializer.errors)
            return Response(api_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# //////////// end      image upload / display
