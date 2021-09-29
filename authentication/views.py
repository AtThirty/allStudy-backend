from rest_framework import generics, status
from rest_framework.decorators import api_view
from .serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    SetNewPasswordSerializer,
    LogoutSerializer,
)
from rest_framework.response import Response
from .models import User


class RegisterView(generics.GenericAPIView):
    serializer_class=RegisterSerializer

    def post(self, request):
        user=request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data=serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)
        

class LoginAPIView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success':True, 'message':'logout complete'}, status=status.HTTP_204_NO_CONTENT)
        

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class=SetNewPasswordSerializer
    
    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':'Password reset success'}, status=status.HTTP_200_OK)

@api_view(('GET',))
def AccountSearchAPI(request, *args, **kwargs):
    context = {}

    search_query = request.GET.get("q")
    if len(search_query) > 0:
        search_results = User.objects.filter(username__startswith=search_query).distinct()
        accounts = []
        for account in search_results:
            accounts.append((account.username, -1))
        context['accounts'] = accounts
    return Response(context, status=status.HTTP_200_OK)


@api_view(('GET',))
def AccountView(request, **kwargs):
    context = {}
    from_user = kwargs["username1"]
    to_user = kwargs["username2"]
    
    try:
        user_data = User.objects.get(username=to_user)
    except:
        return Response({"message": "does't exist"}, status=status.HTTP_400_BAD_REQUEST)

    is_self = True
    # -1 -> 친구X // 0 -> 친추보낸상태 // 1 -> 친구인상태
    friend_status = -1
    friend_request = []

    if from_user != to_user:
        is_self = False
    else:
        friend_request = ["friend1", "friend2"]

    context['username'] = user_data.username
    context['profile'] = user_data.profile_image.url
    context['is_self'] = is_self
    context['friend_status'] = friend_status
    context['friend_request'] = friend_request

    return Response(context, status=status.HTTP_200_OK)

