from rest_framework import serializers
from blog.models import Articles, Category
from django.contrib.auth import get_user_model

class ArticlesSerializer(serializers.ModelSerializer):
    
    snippet    = serializers.ReadOnlyField(source ="get_snippet")
    object_url = serializers.SerializerMethodField()
    # author = serializers.PrimaryKeyRelatedField(read_only=True)
    
    # author = serializers.SlugRelatedField(
    #     many = False, 
    #     read_only=True,
    #     slug_field= 'username'
    #  )
    # author = serializers.SerializerMethodField()
    # def get_author(self,obj):
    #     return str(obj.author.first_name or obj.author.username )
    
    
    def get_object_url(self, obj):
        request = self.context.get('request')
        # return request.build_absolute_uri(obj.slug)   #all the slugs   will be added to the end of the url
        return request.build_absolute_uri(obj.pk)       #all the  IDs    will be added to the end of the url
    
    def to_representation(self, instance):
        request = self.context.get('request')
        data    = super(ArticlesSerializer, self).to_representation(instance)
        # data['categories'] =       [i.title  for i in instance.categories.all()]    #first way
        # data.update({"categories": [i.title  for i in instance.categories.all()]})   #second way
        
        '''third way: serilize the "instance.categories" based on the "CategoriesSerializer" 
             many   : this is a ManytoMany field
            .data   : we will get a json object and .data gives us its data
        '''
        data['categories'] = CategoriesSerializer(instance.categories.all(), 
                                                  many=True,
                                                  context = {"request":request} #included extra context
                                                                                #(EX: we get request in "to_rep... in the CategoriesSerializer but it will failed. now we send it and it won't fail anymore")
                                                  
                                                  ).data
        data['author'] = instance.author.first_name or instance.author.username
        # print(request.__dict__)
        
        ''' we can also use a diffrent serializer for detail-view instead'''
        if request.parser_context.get('kwargs').get('pk'): # if it is a detail view. 
            data.pop("snippet", None)
            data.pop("object_url", None)
        else:
            data.pop("description", None)
        
        return data


    def save(self, **kwargs):
        request = self.context.get('request')
        if not request.user.is_superuser :
            kwargs["author"] = request.user
        return super().save(**kwargs)

    def get_fields(self):
        ''' or we can define 2 serialzer and then use  "def get_serializer_class(self) in the views " '''
        fields = super().get_fields()  
        request = self.context.get("request", None)
        if request and request.user and not request.user.is_superuser:
            fields["author"].read_only = True
        return fields

    class Meta:
        model = Articles
        
        fields = ( "__all__"
                )
        

class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "title"]
