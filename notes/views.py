from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.cache import cache
from .models import Note
from .serializers import NoteSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user account.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': serializer.data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Authenticate user and return their auth token.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'username': user.username,
            'token': token.key
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def notes_list(request):
    cache_key = f"user_{request.user.id}_notes"

    if request.method == 'GET':
        search = request.GET.get('search')
        
        # Search queries bypass general list caching to ensure fresh filters
        if search:
            notes = Note.objects.filter(user=request.user, title__icontains=search).order_by('-created_at')
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data)
        
        # Check Redis Cache
        cached_notes = cache.get(cache_key)
        if cached_notes is not None:
            return Response(cached_notes)

        # Cache Miss: Query Database
        notes = Note.objects.filter(user=request.user).order_by('-created_at')
        serializer = NoteSerializer(notes, many=True)
        
        # Store serialized data in Redis Cache for 1 Hour
        cache.set(cache_key, serializer.data, timeout=3600)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Bind note owner
            
            # Cache Invalidation: Delete old cache since list state has changed
            cache.delete(cache_key)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def note_detail(request, pk):
    cache_key = f"user_{request.user.id}_notes"

    try:
        # Secure endpoint: ensure user only interacts with their own note
        note = Note.objects.get(pk=pk, user=request.user)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Cache Invalidation: Clear notes cache list to reflect update
            cache.delete(cache_key)
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        note.delete()
        
        # Cache Invalidation: Clear notes cache list to reflect deletion
        cache.delete(cache_key)
        
        return Response(status=status.HTTP_204_NO_CONTENT)