from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .models import Category, Relations
from .serializers import CategorySerializer


def addTree(data, is_child, parent):
    cat = Category.objects.create(name=data['name'])
    if is_child:
        Relations.objects.create(parent=parent, child=cat)
    if 'children' in data:
        for c in data['children']:
            addTree(c, True, cat)


class HomeView(APIView):
    def get(self, request, format=None):
        message = 'Welcome ' \
                  'All Categories @ http://127.0.0.1:8000/category/ ' \
                  'All Category Relations @ http://127.0.0.1:8000/category/<id>/'
        return Response(message)


class CategoryView(APIView):
    def get(self, request, format=None):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        addTree(data, False, -1)
        return Response('Success', status=status.HTTP_201_CREATED)


class CategoryDetailView(APIView):
    def get(self, request, pk, format=None):
        category = Category.objects.get(pk=pk)
        ct_s = CategorySerializer(category)
        data = ct_s.data
        with connection.cursor() as cursor:
            # Parent Categories
            cursor.execute("SELECT DISTINCT c.* FROM category_category as c WHERE c.id in"
                           "(SELECT r.parent_id FROM category_relations as r WHERE r.child_id = %s)"
                           , [category.pk])
            columns = [col[0] for col in cursor.description]
            parent = [dict(zip(columns, row)) for row in cursor.fetchall()]
            pt_s = CategorySerializer(parent, many=True)
            data['parent'] = pt_s.data
            # Siblings Categories
            if parent:
                cursor.execute("SELECT c.* FROM category_category as c WHERE c.id in "
                               "(SELECT r.child_id FROM category_relations as r "
                               "WHERE r.parent_id = %s and r.child_id <> %s)", [parent[0]['id'], category.pk])
                columns = [col[0] for col in cursor.description]
                siblings = [dict(zip(columns, row)) for row in cursor.fetchall()]
                sb_s = CategorySerializer(siblings, many=True)
                data['siblings'] = sb_s.data
            else:
                data['siblings'] = []
            # Child Categories
            cursor.execute("SELECT c.* FROM category_category as c WHERE c.id in "
                           "(SELECT r.child_id FROM category_relations as r "
                           "WHERE r.parent_id = %s)", [category.pk])
            columns = [col[0] for col in cursor.description]
            children = [dict(zip(columns, row)) for row in cursor.fetchall()]
            ch_s = CategorySerializer(children, many=True)
            data['children'] = ch_s.data

        return Response(data)
