from django.urls import path
from . import views


urlpatterns = [
  path('singleobj/',views.singleobj),
  path('multipleobj/',views.multipleobj),
  path('updatesingleobj/<int:id>/',views.updatesingleobj),
  path('drfupdatesingleobj/<int:id>/',views.drfupdatesingleobj),
  path('drfmultipleobj/',views.drfmultipleobj),
  path('apiviewmultipleobj/',views.MultipleObjAPIView.as_view()),
  path('apiviewsingleobj/<int:id>/',views.SingleObjAPIView.as_view()),  
  path('genericapiviewmultipleobj/',views.MultipleObjGenericAPIView.as_view()),
  path('genericapiviewsingleobj/<int:pk>/',views.SingleeObjGenericAPIView.as_view()),
  path('listcreatemultipleobj/',views.MultipleObjListCreateAPIView.as_view()),
  path('retrieveupdatedeletesingleobj/<int:pk>/',views.SingleeObjRetrieveUpdateDestroyAPIView.as_view()),
  

]