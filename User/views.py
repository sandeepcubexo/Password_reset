from .serializer import RegisterSerializer,  AuthenticationSerializer,UserSerializer
from rest_framework.decorators import APIView, api_view
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response


class Login(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = AuthenticationSerializer

class userGetViewSet(APIView):
    serializer_class = UserSerializer#extra
    def get(self, request):
        try:
            print(self.request.user)
            user = User.objects.get(id=self.request.user.id)
        except User.DoesNotExist:
            return Response({'error': " Invalid user ID"})
        ser = userGetSerializer(user, many=False)
        return Response(ser.data)

@api_view(['GET', 'POST'])
def Registerapi(request):
    user_serializer = RegisterSerializer(data=request.data)
    if user_serializer.is_valid():
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializer import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)