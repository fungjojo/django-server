import statistics
from requests import Response


class CertMixin:
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=statistics.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # That's where we can stick our logic!
        print("???? perform create")
        serializer.save()

    def gen_cert():
        print("???? perform gen cert")
    # def get_success_headers(self, data):
        # ... # irrelevant for the example, so skipping