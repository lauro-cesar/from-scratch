
from rest_framework import serializers
from accounts.models import AccountProfileModel

class AccountProfileModelSerializer(serializers.ModelSerializer):   
    def create(self, validated_data):        
        criado_por = self.context.get('criado_por',None)
        if criado_por:
            validated_data.update({
                'criado_por':criado_por
            })
            
        instance = AccountProfileModel.objects.create(**validated_data)       
        return instance

    class Meta:
        model = AccountProfileModel
        fields = AccountProfileModel.SERIALIZABLES
        if AccountProfileModel.READ_ONLY_FIELDS:
            read_only_fields =AccountProfileModel.READ_ONLY_FIELDS
