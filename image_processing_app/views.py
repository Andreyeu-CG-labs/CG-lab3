from PIL import Image
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from image_processing_app.forms import ImageProcessingFrom, ChooseImageFrom
from image_processing_app.image_processing.image_processing import \
    update_image, update_histograms


class ImageProcessingView(FormView):
    template_name = 'image_processing.html'
    form_class = ImageProcessingFrom

    def form_valid(self, form):
        context = {'form': form}
        update_image(form.cleaned_data)
        update_histograms()
        return render(self.request, 'image_processing.html', context=context)


class ChooseImageView(FormView):
    template_name = 'choose_image.html'
    form_class = ChooseImageFrom
    success_url = reverse_lazy('image-processing')

    def form_valid(self, form):
        image = Image.open(form.cleaned_data['image'].file)
        image.save('image_processing_app/static/image.png')
        image.save('image_processing_app/static/current_image.png')
        update_histograms()
        return super().form_valid(form)
