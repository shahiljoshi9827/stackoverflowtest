from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from QA.models import Question, Answer, QuestionTag, QuestionUserUpVote, QuestionUserDownVote, AnswerUserUpVote, \
    AnswerUserDownVote
from QA.serializers import QuestionSerializer, AnswerSerializer, QuestionTagSerializer


class QuestionView(generics.ListCreateAPIView):
    """
     this view is used to get all questions and create a new question with tag
    """
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
        for tag in request.data['tags']:
            question_tag = QuestionTagSerializer(data={'question': serializer.data['id'], 'tag': tag})
            question_tag.is_valid(raise_exception=True)
            question_tag.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
     this view is used to get question details, update question details
    """
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
    """
        this view is used to get all answers and create a new answer and it will sends notification to question owner
    """

    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    queryset = Answer.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(self, request)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_mail("Posted Answer To Your Question", from_email="", recipient_list=[""], )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        this view is used to get answer details, update answer details
    """
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def get_queryset(self, id=None):
        return Answer.objects.filter(question_id=id)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(id=kwargs['id']), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(id=kwargs['id']), data=request.data, partial=True, )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AcceptAnswerView(generics.RetrieveUpdateDestroyAPIView):
    """
        this view is used to accept answer and it will send email to answer owner
    """
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def get_queryset(self, pk=None, question_id=None):
        print(pk, question_id)
        return Answer.objects.get(question_id=question_id, id=pk)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(pk=kwargs['pk'], question_id=kwargs['question_id']))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(pk=kwargs['pk'], question_id=kwargs['question_id']),
                                           data=request.data, partial=True, )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_mail("Congratulations! Your Answer Accepted", from_email="", recipient_list=[""], )
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionTagView(generics.RetrieveAPIView):
    """
        this view is used to get all questions from tag name
    """
    serializer_class = QuestionTagSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def get_queryset(self, tag=None):
        return QuestionTag.objects.filter(tag__name=tag)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(tag=kwargs['tag']), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionUserView(generics.RetrieveAPIView):
    """
        this view is used to get all questions from logged in user
    """
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def get_queryset(self, user_id=None):
        return Question.objects.filter(user_id=user_id)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(user_id=request.user.id), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionUserUpvoteDownvoteView(generics.CreateAPIView):
    """
        this view is used to upvote or downvote a question
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        if request.data['upvote'] == True:
            question = QuestionUserUpVote.objects.filter(question_id=kwargs['id'], user_id=request.user.id).exists()
            if not question:
                question = QuestionUserUpVote.objects.create(question_id=kwargs['id'], user_id=request.user.id)
                question.save()
        else:
            question = QuestionUserDownVote.objects.filter(question_id=kwargs['id'], user_id=request.user.id).exists()
            if not question:
                question = QuestionUserDownVote.objects.create(question_id=kwargs['id'], user_id=request.user.id)
                question.save()
        count = QuestionUserUpVote.objects.filter(
            question_id=kwargs['id']).count() - QuestionUserDownVote.objects.filter(question_id=kwargs['id']).count()
        return Response({"vote count": count}, status=status.HTTP_200_OK)


class AnswerUserUpvoteDownvoteView(generics.CreateAPIView):
    """
        this view is used to upvote or downvote a answer
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        if request.data['upvote'] == True:
            answer = AnswerUserUpVote.objects.filter(answer_id=kwargs['id'], user_id=request.user.id).exists()
            if not answer:
                answer = AnswerUserUpVote.objects.create(answer_id=kwargs['id'], user_id=request.user.id)
                answer.save()
        else:
            answer = AnswerUserDownVote.objects.filter(answer_id=kwargs['id'], user_id=request.user.id).exists()
            if not answer:
                answer = AnswerUserDownVote.objects.create(answer_id=kwargs['id'], user_id=request.user.id)
                answer.save()
        count = AnswerUserUpVote.objects.filter(
            answer_id=kwargs['id']).count() - AnswerUserDownVote.objects.filter(answer_id=kwargs['id']).count()
        return Response({"vote count": count}, status=status.HTTP_200_OK)
