from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from QA.models import Question
from QA.serializers import QuestionSerializer, AnswerSerializer


class QuestionView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    queryset = Question.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(self, request)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def get_queryset(self, pk=None):
        return Question.objects.get(id=pk)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(pk=kwargs['id']))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(pk=kwargs['id']), data=request.data, partial=True, )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerView(generics.ListCreateAPIView):
    serializer_class = AnswerSerializer
    # permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    queryset = Question.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(self, request)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
    # permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def get_queryset(self, pk=None):
        return Question.objects.get(id=pk)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(pk=kwargs['id']))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(pk=kwargs['id']), data=request.data, partial=True, )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
