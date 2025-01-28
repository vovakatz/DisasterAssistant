from app.models.sample import SampleResponse

class SampleService:
    def get_sample_data(self):
        return SampleResponse(message="Hello, World!")