from app.models.sample_response import SampleResponse

class SampleService:
    def get_sample_data(self):
        return SampleResponse(message="Hello, World!")