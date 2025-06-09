from rest_framework.response import Response


def handle_image_upload(viewset_instance, request):
    instance = viewset_instance.get_object()
    serializer = viewset_instance.get_serializer(
        instance, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
