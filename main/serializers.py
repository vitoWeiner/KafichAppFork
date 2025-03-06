from rest_framework import serializers
from main.models import Pice


class PiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
        model = Pice
        fields = ('pice_sifra','pice_naziv', 'pice_opis', 'pice_kolicina_u_ml', 'pice_sadrzi_alkohol', 'pice_vegansko', 'pice_poj_cijena')

        extra_kwargs = {
            'pice_naziv': {'required': True},
            'pice_kolicina_u_ml': {'required': True},
            'pice_poj_cijena': {'required': True}
        }

    def validate_pice_kolicina_u_ml(self, value):
        if value <= 0:
            raise serializers.ValidationError("Količina mora biti veća od 0 ml.")
        return value

    def validate_pice_poj_cijena(self, value):
        if value < 0:
            raise serializers.ValidationError("Cijena ne može biti negativna.")
        return value




