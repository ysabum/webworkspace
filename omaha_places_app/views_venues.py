from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from .models import *

import os
from dotenv import load_dotenv
from urllib.parse import unquote

RESTAURANT_CATEGORY_MAPPING = {
    "restaurant, bar, food, point_of_interest, establishment": "Bar",
    "night_club, bar, restaurant, food, point_of_interest, establishment": "Bar",
    "bar, restaurant, food, point_of_interest, establishment": "Bar",
    "meal_takeaway, bar, restaurant, food, point_of_interest, establishment": "Bar",
    "bakery, bar, store, restaurant, food, point_of_interest, establishment": "Bar",
    "bar, point_of_interest, establishment": "Bar",
    "night_club, bar, point_of_interest, establishment": "Bar",
    "night_club, bar, store, point_of_interest, establishment": "Bar",
    "bowling_alley, bar, point_of_interest, establishment": "Bar",
    "bar, store, restaurant, food, point_of_interest, establishment": "Bar",
    "bar, liquor_store, night_club, point_of_interest, store, establishment": "Bar",
    "bar, restaurant, point_of_interest, food, establishment": "Bar",
    "bar, liquor_store, point_of_interest, store, establishment": "Bar",
    "bar, point_of_interest, store, establishment": "Bar",
    "bar, point_of_interest, food, establishment": "Bar",
    "restaurant, bar, point_of_interest, food, establishment": "Bar",
    "bar, liquor_store, restaurant, point_of_interest, food, store, establishment": "Bar",
    "cafe, bakery, bar, store, food, night_club, point_of_interest, establishment": "Bar",
    
    "restaurant, food, point_of_interest, establishment": "Restaurant",
    "meal_takeaway, restaurant, food, point_of_interest, establishment": "Restaurant",
    "meal_delivery, meal_takeaway, restaurant, food, point_of_interest, establishment": "Restaurant",
    "meal_takeaway, meal_delivery, restaurant, food, point_of_interest, establishment": "Restaurant",
    "store, restaurant, food, point_of_interest, establishment": "Restaurant",
    "restaurant, cafe, food, point_of_interest, establishment": "Restaurant",
    "restaurant, bakery, cafe, store, food, point_of_interest, establishment": "Restaurant",

    "cafe, store, restaurant, food, point_of_interest, establishment": "Cafe",
    "cafe, store, food, point_of_interest, establishment": "Cafe",
    "book_store, cafe, store, food, point_of_interest, establishment": "Cafe",
    "bakery, cafe, store, restaurant, food, point_of_interest, establishment": "Cafe",
    "cafe, meal_takeaway, bakery, store, restaurant, food, point_of_interest, establishment": "Cafe",
    "cafe, bakery, store, restaurant, food, point_of_interest, establishment": "Cafe",
    "book_store, cafe, church, place_of_worship, store, food, point_of_interest, establishment": "Cafe",
    "gas_station, bakery, cafe, liquor_store, store, restaurant, food, point_of_interest, establishment": "Cafe",
    "meal_takeaway, bakery, cafe, store, restaurant, food, point_of_interest, establishment": "Cafe",
    "cafe, food, point_of_interest, establishment": "Cafe",

    "meal_takeaway, bakery, grocery_or_supermarket, store, restaurant, food, point_of_interest, establishment": "Grocery-Bakery",
    "department_store, hardware_store, bakery, grocery_or_supermarket, furniture_store, home_goods_store, clothing_store, electronics_store, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "grocery_or_supermarket, florist, bakery, liquor_store, health, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "grocery_or_supermarket, bakery, supermarket, health, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "bakery, electronics_store, liquor_store, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "bakery, supermarket, grocery_or_supermarket, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "bakery, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "grocery_or_supermarket, department_store, bakery, supermarket, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "bakery, store, restaurant, food, point_of_interest, establishment": "Grocery-Bakery",
    "grocery_or_supermarket, supermarket, bakery, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "grocery_or_supermarket, bakery, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "grocery_or_supermarket, supermarket, bakery, pharmacy, liquor_store, florist, health, store, food, point_of_interest, establishment": "Grocery-Bakery",

    "gas_station, cafe, moving_company, car_repair, store, restaurant, food, point_of_interest, establishment": "Gas-Station",

     "movie_theater, meal_takeaway, restaurant, food, point_of_interest, establishment": "Others",
}

PLACE_CATEGORY_MAPPING = {
    "amusement_park, point_of_interest, clothing_store, store, establishment": "Park",
    "amusement_park, point_of_interest, establishment": "Park",
    "park, point_of_interest, establishment": "Park",
    "park, tourist_attraction, point_of_interest, establishment": "Park",
    "funeral_home, cemetery, park, point_of_interest, establishment": "Park",
    "museum, tourist_attraction, park, point_of_interest, establishment": "Park",
    "store, park, point_of_interest, establishment": "Park",
    "tourist_attraction, amusement_park, point_of_interest, establishment": "Park",
    
    "art_gallery, furniture_store, home_goods_store, point_of_interest, store, establishment": "Store",
    "art_gallery, furniture_store, home_goods_store, store, point_of_interest, establishment": "Store",
    "art_gallery, point_of_interest, store, establishment": "Store",
    "art_gallery, store, point_of_interest, establishment": "Store",
    "book_store, library, point_of_interest, store, establishment": "Store",
    "clothing_store, store, point_of_interest, establishment": "Store",
    "department_store, hardware_store, electronics_store, bakery, furniture_store, home_goods_store, grocery_or_supermarket, clothing_store, store, food, point_of_interest, establishment": "Store",
    "department_store, shoe_store, electronics_store, furniture_store, home_goods_store, clothing_store, store, point_of_interest, establishment": "Store",
    "electronics_store, museum, point_of_interest, store, establishment": "Store",
    "furniture_store, art_gallery, home_goods_store, point_of_interest, store, establishment": "Store",
    "furniture_store, electronics_store, home_goods_store, store, point_of_interest, establishment": "Store",
    "store, point_of_interest, establishment": "Store",
    
    "art_gallery, bar, cafe, restaurant, point_of_interest, food, store, establishment": "Bar",
    "art_gallery, bar, point_of_interest, establishment": "Bar",
    "restaurant, bar, food, point_of_interest, establishment": "Bar",
    
    "art_gallery, museum, point_of_interest, establishment": "Museum-Theater",
    "art_gallery, tourist_attraction, point_of_interest, establishment": "Museum-Theater",
    "movie_theater, meal_takeaway, restaurant, food, point_of_interest, establishment": "Museum-Theater",
    "movie_theater, point_of_interest, establishment": "Museum-Theater",
    "museum, point_of_interest, establishment": "Museum-Theater",
    "museum, tourist_attraction, point_of_interest, establishment": "Museum-Theater",
    "tourist_attraction, art_gallery, point_of_interest, establishment": "Museum-Theater",
    "tourist_attraction, museum, point_of_interest, establishment": "Museum-Theater",
    "art_gallery, restaurant, point_of_interest, food, establishment": "Museum-Theater",
    
    "art_gallery, school, point_of_interest, establishment": "School",
    "school, point_of_interest, establishment": "School",
    "secondary_school, school, point_of_interest, establishment": "School",
    "university, health, point_of_interest, establishment": "School",
    "university, point_of_interest, establishment": "School",
    
    "art_gallery, health, point_of_interest, establishment": "TravelAgent-Health",
    "beauty_salon, art_gallery, gym, health, point_of_interest, establishment": "TravelAgent-Health",
    "hospital, health, point_of_interest, establishment": "TravelAgent-Health",
    "tourist_attraction, travel_agency, point_of_interest, establishment": "TravelAgent-Health",
    
    "casino, lodging, point_of_interest, establishment": "Lodging",
    "lodging, point_of_interest, establishment": "Lodging",
    
    "zoo, point_of_interest, establishment": "Zoo",
    "zoo, tourist_attraction, point_of_interest, establishment": "Zoo",
    "zoo, park, point_of_interest, establishment": "Zoo",
    "zoo, tourist_attraction, park, point_of_interest, establishment": "Zoo",
    
    "mosque, tourist_attraction, place_of_worship, point_of_interest, establishment": "Mosque",
    
    "art_gallery, local_government_office, point_of_interest, establishment": "Others",
    "art_gallery, point_of_interest, establishment": "Others",
    "library, point_of_interest, establishment": "Others",
    "local_government_office, point_of_interest, establishment": "Others",
    "point_of_interest, establishment": "Others",
    "tourist_attraction, point_of_interest, establishment": "Others"
}


class RestaurantsView(ListView):
    '''
    Class-based view to display restaurants.
    '''

    model = Restaurant
    template_name = 'omaha_places_app/home-restaurants.html'
    context_object_name = 'home_restaurants'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant_images = list(Restaurant.objects.exclude(image__isnull = True).exclude(image = 'N/A').values_list('image', flat = True))
        predefined_category = Restaurant.objects.values_list('predefined_category', flat=True).distinct()
        # unique_categories = list(set(categories))
        # unique_categories.sort()

        context['predefined_category'] = predefined_category
        return context


class RestaurantDetailView(TemplateView):
    '''
    Class-based view to display the details of a single restaurant.
    '''

    template_name = 'omaha_places_app/restaurant.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = Restaurant.objects.get(id = self.kwargs['pk'])

        return context


class PlacesView(ListView):
    '''
    Class-based view to display places.
    '''

    model = Place
    template_name = 'omaha_places_app/home-places.html'
    context_object_name = 'home_places'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place_images = list(Place.objects.exclude(image__isnull=True).exclude(image='N/A').values_list('image', flat=True))
        predefined_category = Place.objects.values_list('predefined_category', flat=True).distinct()

        dotenv_path = r'omaha_places_app\cache\googleapi.env'
        load_dotenv(dotenv_path=dotenv_path)
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

        # Ensure the API key is correctly replaced
        if GOOGLE_API_KEY:
            place_images_with_api_key = [
                self.replace_api_key(image, GOOGLE_API_KEY)
                for image in place_images
            ]
        else:
            place_images_with_api_key = place_images

        context['place_images'] = place_images_with_api_key
        context['predefined_category'] = predefined_category
        return context
    
    def replace_api_key(self, image_url, api_key):
        '''
        Replace the placeholder GOOGLE_API_KEY in the image URL with the actual API key.
        '''

        image_url = image_url.replace('GOOGLE_API_KEY', api_key)
        image_url = image_url.replace('maxwidth=400', 'maxwidth=900')
        image_url = unquote(image_url)

        return image_url
    

class PlacesViewAll(ListView):
    '''
    Class-based view to display all places in details
    '''

    model = Place
    template_name = 'omaha_places_app/all-places.html'
    context_object_name = 'all_places'
    paginate_by = 20 # Number of places per page

    def get_context_data(self, **kwargs):
        dotenv_path = r'omaha_places_app\cache\googleapi.env'
        load_dotenv(dotenv_path=dotenv_path)
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
        context = super().get_context_data(**kwargs)
        place_images = list(Place.objects.exclude(image__isnull=True).exclude(image='N/A').values_list('image', flat=True))
        predefined_category = Place.objects.values_list('predefined_category', flat=True).distinct()
        selected_category = self.request.GET.get('category', None)

        if selected_category:
            places = Place.objects.filter(predefined_category=selected_category)
        else:
            places = Place.objects.all()

        predefined_category = Place.objects.values_list('predefined_category', flat=True).distinct()
        
        if GOOGLE_API_KEY:
            place_images_with_api_key = [
                self.replace_api_key(image, GOOGLE_API_KEY)
                for image in place_images
            ]
        else:
            place_images_with_api_key = place_images

        context['predefined_category'] = predefined_category
        context['selected_category'] = selected_category
        context['all_places'] = places
        context['place_images'] = place_images_with_api_key

        return context
    
    def replace_api_key(self, image_url, api_key):
        '''
        Replace the placeholder GOOGLE_API_KEY in the image URL with the actual API key.
        '''

        image_url = image_url.replace('GOOGLE_API_KEY', api_key)
        image_url = image_url.replace('maxwidth=400', 'maxwidth=900')
        image_url = unquote(image_url)

        return image_url

    
class PlaceDetailView(TemplateView):
    '''
    Class-based view to display the details of a single place.
    '''

    template_name = 'omaha_places_app/place.html'

    def get_context_data(self, **kwargs):
        dotenv_path = r'omaha_places_app\cache\googleapi.env'
        load_dotenv(dotenv_path=dotenv_path)
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

        place = Place.objects.get(id=self.kwargs['pk'])
        if place.image and place.image != 'N/A':
            place_image = place.image 
        else:
            place_image = None

        if place_image and GOOGLE_API_KEY:
            place_image = self.replace_api_key(str(place_image), GOOGLE_API_KEY)

        context = super().get_context_data(**kwargs)
        context['place'] = place
        context['place_image'] = place_image

        return context

    def replace_api_key(self, image_url, api_key):
        '''
        Replace the placeholder GOOGLE_API_KEY in the image URL with the actual API key.
        '''
        image_url = image_url.replace('GOOGLE_API_KEY', api_key)
        image_url = image_url.replace('maxwidth=400', 'maxwidth=900')
        image_url = unquote(image_url)

        return image_url
