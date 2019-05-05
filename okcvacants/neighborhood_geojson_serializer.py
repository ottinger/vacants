from django.contrib.gis.serializers.geojson import Serializer as GeoJSONSerializer


class Serializer(GeoJSONSerializer):
    def get_dump_object(self, obj):
        data = super(Serializer, self).get_dump_object(obj)
        data['properties'].update(property_count=obj.properties.count())
        data['properties'].update(property_density=(obj.properties.count() / (obj.boundary_area / 640)))
        return data
