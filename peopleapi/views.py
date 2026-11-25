import io
import json
from django.shortcuts import render

from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from .models import Person
from .serializers import PersonSerializer, PersonModelSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.shortcuts import get_object_or_404
# django restframework api views se
from rest_framework.decorators import api_view
from rest_framework.response import Response

# CLASSBASED VIEWS
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin,UpdateModelMixin,ListModelMixin,RetrieveModelMixin,DestroyModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.throttling import ScopedRateThrottle, UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


# here in all functions, we replaced the 'PersonSerializer' to 'PersonModelSerializer' .
#  here all we use django core views for our rest api. but django restframework have it's own apiviews like functin based views, classbased view..
def singleobj(request):
    data = Person.objects.get(id=18)
    # print('data :',data)
    serializer = PersonModelSerializer(data) 
    # print('serializer :',serializer.data)
    # JSONRenderer() is a DRF class that converts Python data(serialized data) into JSON format.,
    # json_data = JSONRenderer().render(serializer.data)
    # json_data: The data you want to send as a response.
    # content_type='application/json': Tells the browser that the response contains JSON data.
    # return HttpResponse(json_data, content_type='application/json')
    return JsonResponse(serializer.data)
  

@csrf_exempt #@api_view(['GET','POST'])
def multipleobj(request):
    if request.method == 'POST':
      # {{
      # json = request.body #json data send by the user with the request ,#"json" contains JSON data in bytes format.
      # stream = io.BytesIO(json) #io.BytesIO() converts bytes data into a file-like object.It allows Python to read the data as if it were reading a file. #"stream" behaves like a file containing JSON data.
      # parsed_data = JSONParser().parse(stream) #.parse() reads the JSON data from the stream.It converts JSON data into Python data (usually a dictionary or list).    
      # }instead of the above codes we can use below single code " parsed_data =  json.loads(request.body)"}
      parsed_data =  json.loads(request.body) #json.loads() – Converts JSON string/bytes into a Python object.
      # print('parsed_data : ',parsed_data)
      # print(type(parsed_data))
      serializer = PersonModelSerializer(data = parsed_data) #deserialization
      if serializer.is_valid():
        serializer.save()
        return JsonResponse({"created ": "successfull"}, status = status.HTTP_201_CREATED)
      return JsonResponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST) #errors = JSONRendere().render(serializer.errors)
                                                                                  #return HttpResponse(errors,content_type ="application/json" )    
    data = Person.objects.all()
    # print('data :',data)
    serializer = PersonModelSerializer(data, many=True) #serialization
    #  print('serializer :',serializer.data)
    # JSONRenderer() is a DRF class that converts Python data(serialized data) into JSON format.,
    # json_data = JSONRenderer().render(serializer.data)# json_data: The data you want to send as a response.
    # return HttpResponse(json_data, content_type='application/json')# content_type='application/json': Tells the browser that the response contains JSON data.
    return JsonResponse(serializer.data, safe=False) #safe=  ==>Used for non-dictionary data .Accepts list, dictionary, etc.

@csrf_exempt
def updatesingleobj(request,id):
    obj_data = get_object_or_404(Person,id=id)
    if request.method == 'PUT':
      parsed_data =  json.loads(request.body)
      serializer = PersonModelSerializer(obj_data,data = parsed_data)
      if serializer.is_valid():
        serializer.save()
        return JsonResponse({"update": "success"})        
      return JsonResponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST)    
   
    if request.method == 'PATCH': #partial updation
      parsed_data =  json.loads(request.body)
      serializer = PersonModelSerializer(obj_data,data = parsed_data,partial = True)
      if serializer.is_valid():
        serializer.save()
        return JsonResponse({"update": "success fully"})        
      return JsonResponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST)        
    serializer = PersonModelSerializer(obj_data)
    return JsonResponse(serializer.data)
  
@api_view(['GET','PUT','PATCH']) #replaced JsonResponse to Response class (ie, provided by drf)
def drfupdatesingleobj(request,id):
    obj_data = get_object_or_404(Person,id=id)
    if request.method == 'PUT':
      # parsed_data =  json.loads(request.body)
      parsed_data = request.data # bez of using @api_view
      serializer = PersonModelSerializer(obj_data,data = parsed_data)
      if serializer.is_valid():
        serializer.save()
        return Response({"update": "success"})        
      return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)    
   
    if request.method == 'PATCH': #partial updation
      # parsed_data =  json.loads(request.body)
      parsed_data = request.data
      serializer = PersonModelSerializer(obj_data,data = parsed_data,partial = True)
      if serializer.is_valid():
        serializer.save()
        return Response({"update": "success fully"})        
      return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)        
    # print(request.accepted_renderer) # content negotiation
    serializer = PersonModelSerializer(obj_data)
    return Response(serializer.data)
  


@api_view(['GET','POST']) #@api_view converts a Django function-based view into a DRF API view
def drfmultipleobj(request):
    if request.method == 'POST':
      parsed_data =  request.data
      serializer = PersonModelSerializer(data = parsed_data) #deserialization
      serializer.is_valid(raise_exception=True) #use "raise_exception=True" by drf, in is_valid()  instead of checking error manually
      serializer.save()
      return Response({"created ": "successfull"}, status = status.HTTP_201_CREATED)
     
    data = Person.objects.all()
    serializer = PersonModelSerializer(data, many=True) #serialization
    return Response(serializer.data) # drf browsable api interface is applicatble for DRF's Response , not for JsonResponse
  
  
# use CBV- APIView -  when we want more control over the code executed for each HTTP methods. 
class MultipleObjAPIView(APIView):
    def get(self,request):
      data = Person.objects.all()
      serializer = PersonModelSerializer(data, many=True) #serialization
      return Response(serializer.data)
    
    def post(self, request):
      parsed_data =  request.data
      serializer = PersonModelSerializer(data = parsed_data) #deserialization
      serializer.is_valid(raise_exception=True) #use "raise_exception=True" by drf, in is_valid()  instead of checking error manually
      serializer.save()
      return Response({"created ": "successfull"}, status = status.HTTP_201_CREATED)
           
class SingleObjAPIView(APIView): 
  def get(self,request,id):
    obj_data = get_object_or_404(Person,id=id)
    serializer = PersonModelSerializer(obj_data)
    return Response(serializer.data)
  
  def put(self,request,id):
    obj_data = get_object_or_404(Person,id=id)
    parsed_data = request.data # bez of using @api_view
    serializer = PersonModelSerializer(obj_data,data = parsed_data)
    if serializer.is_valid():
      serializer.save()
      return Response({"update": "success"})        
    return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)    
       
       
  def patch(self,request,id):
    obj_data = get_object_or_404(Person,id=id)
    parsed_data = request.data
    serializer = PersonModelSerializer(obj_data,data = parsed_data,partial = True)
    if serializer.is_valid():
      serializer.save()
      return Response({"update": "success fully"})        
    return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)        

# GenericAPIView 
class MultipleObjGenericAPIView(CreateModelMixin,ListModelMixin, GenericAPIView):
  queryset = Person.objects.all()
  serializer_class = PersonModelSerializer   
  
  def get(self,request,*args,**kwargs):
    return self.list(request, *args,**kwargs)
    
  def post(self, request):
    return self.create(request)      
      
      
class SingleeObjGenericAPIView(UpdateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericAPIView): 
  queryset = Person.objects.all()
  serializer_class = PersonModelSerializer  
  def get(self,request, *args,**kwargs):
    return self.retrieve(request, *args,**kwargs)
  
  def put(self,request, *args,**kwargs):
    return self.update(request, *args,**kwargs)
       
  def patch(self,request,*args,**kwargs):
    return self.partial_update(request, *args,**kwargs)
  
  def delete(self,request,*args,**kwargs):
    return self.destroy(request,*args,**kwargs)
  

class MultipleObjListCreateAPIView(ListCreateAPIView):
  queryset = Person.objects.all()
  serializer_class = PersonModelSerializer  
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]  
  throttle_classes = [UserRateThrottle]  
  filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
  filterset_fields = ['city','name'] #specifies which model fields users are allowed to filter by.
  search_fields = ['name']
   
  ordering_fields = ['name','city'] #Specifies which model fields users can use for sorting.
  ordering = ['name']#Defines the default ordering when the client doesn't provide an ordering parameter
   
  def get(self,request,*args,**kwargs):
    print(request.user)
    response  = super().get(request,*args,**kwargs)
    return response
  
class SingleeObjRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView): 
  queryset = Person.objects.all()
  serializer_class = PersonModelSerializer  
  throttle_classes = [ScopedRateThrottle]
  throttle_scope = 'person'