
from rest_framework import serializers
from restfiles.models import RestImageModel


class RestImageModelSerializer(serializers.ModelSerializer):   
    def create(self, validated_data):        
        criado_por = self.context.get('criado_por',None)
        if criado_por:
            validated_data.update({
                'criado_por':criado_por
            })
            
        instance = RestImageModel.objects.create(**validated_data)       
        return instance

    
    class Meta:
        model = RestImageModel
        fields = RestImageModel.SERIALIZABLES
        if RestImageModel.READ_ONLY_FIELDS:
            read_only_fields =RestImageModel.READ_ONLY_FIELDS
