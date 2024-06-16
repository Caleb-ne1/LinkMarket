from .cart import Cart
from .models import CustomUser
def cart(request):
    return {'cart': Cart(request)}

def display_fullName(request):
    first_name = request.user.first_name
    last_name =  request.user.last_name
    full_name = f"{first_name} {last_name}"
    return {
        'full_name': full_name,
    }