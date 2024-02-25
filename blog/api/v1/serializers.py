from rest_framework import serializers
from blog.models import Articles, Category
from django.contrib.auth import get_user_model

class ArticlesSerializer(serializers.ModelSerializer):
    
    snippet    = serializers.ReadOnlyField(source ="get_snippet")
    relative_url = serializers.ReadOnlyField(source ="get_absolute_api_url")
    absolute_url = serializers.SerializerMethodField()
    absolute_url2 = serializers.HyperlinkedIdentityField(view_name='blog:api-v1:article-detail')#output is same as absolute_url

    # author = serializers.PrimaryKeyRelatedField(read_only=True)
    # author = serializers.SlugRelatedField( #way1
    #     many = False, 
    #     read_only=True,
    #     slug_field= 'username'
    #  )

    # author = serializers.SerializerMethodField()#way2
    # def get_author(self,obj):
    #     return str(obj.author.first_name or obj.author.username )
    
    
    def get_absolute_url(self, obj):
        request = self.context.get('request')
        # return request.build_absolute_uri(obj.slug)   #all the slugs   will be added to the end of the url
        return request.build_absolute_uri(obj.pk)       #all the  IDs    will be added to the end of the url
    
    def to_representation(self, instance):
        data    = super(ArticlesSerializer, self).to_representation(instance)
        request = self.context.get('request')
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
        data['author'] = instance.author.first_name or instance.author.username #way3 best
        # print(request.__dict__)
        
        ''' we can also use a diffrent serializer for detail-view instead'''
        if request.parser_context.get('kwargs').get('pk'): # if it is a detail view. 
            data.pop("snippet", None)
            data.pop("object_url", None)
        else:
            data.pop("description", None)
        
        return data

    def get_fields(self):
        ''' or we can define 2 serialzer and then use  "def get_serializer_class(self) in the views " '''
        fields = super().get_fields()  
        request = self.context.get("request", None)
        if request and request.user and not request.user.is_superuser:
            fields["author"].read_only = True
        return fields

    def save(self, **kwargs):
        request = self.context.get('request')
        if not request.user.is_superuser :
            kwargs["author"] = request.user
        return super().save(**kwargs)

    class Meta:
        model = Articles
        
        fields = ( "__all__")
        

class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "title"]
